"""Orange Pi GPIO/PWM vehicle output with stopped-by-default safety.

香橙派GPIO/PWM整车输出层，默认停车并要求物理按钮启动。

The implementation uses Linux GPIO character devices and kernel PWM through
python-periphery. GPIO line numbers and PWM chip/channel numbers are deliberately
not hard-coded because they depend on the frozen Orange Pi image, device-tree
overlay and chosen header pins.

本程序使用python-periphery访问Linux GPIO字符设备和内核PWM。GPIO line编号、PWM
chip/channel与镜像、设备树和实际排针选择有关，因此仓库不编造固定编号。
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class OutputState(str, Enum):
    DRY_RUN = "DRY_RUN"
    WAIT_START = "WAIT_START"
    GPIO_DRIVE = "GPIO_DRIVE"
    CONTROL_FAILSAFE = "CONTROL_FAILSAFE"
    CLOSED = "CLOSED"


class GpioConfigurationError(RuntimeError):
    """Raised when enabled hardware output lacks a complete safe configuration."""


@dataclass(frozen=True)
class GpioConfig:
    enabled: bool
    gpiochip: str
    motor_dir_line: int
    start_line: int
    start_active_low: bool
    motor_direction_inverted: bool
    motor_pwm_chip: int
    motor_pwm_channel: int
    motor_pwm_frequency_hz: float
    motor_max_duty: float
    servo_pwm_chip: int
    servo_pwm_channel: int
    servo_pwm_frequency_hz: float
    servo_left_us: float
    servo_center_us: float
    servo_right_us: float
    watchdog_ms: int
    debounce_ms: int

    @classmethod
    def load(cls, path: Path) -> "GpioConfig":
        if not path.exists():
            return cls.safe_disabled()
        raw = json.loads(path.read_text(encoding="utf-8"))
        cfg = cls(
            enabled=bool(raw.get("enabled", False)),
            gpiochip=str(raw.get("gpiochip", "/dev/gpiochip0")),
            motor_dir_line=int(raw.get("motor_dir_line", -1)),
            start_line=int(raw.get("start_line", -1)),
            start_active_low=bool(raw.get("start_active_low", True)),
            motor_direction_inverted=bool(raw.get("motor_direction_inverted", False)),
            motor_pwm_chip=int(raw.get("motor_pwm_chip", -1)),
            motor_pwm_channel=int(raw.get("motor_pwm_channel", -1)),
            motor_pwm_frequency_hz=float(raw.get("motor_pwm_frequency_hz", 20000)),
            motor_max_duty=float(raw.get("motor_max_duty", 0.65)),
            servo_pwm_chip=int(raw.get("servo_pwm_chip", -1)),
            servo_pwm_channel=int(raw.get("servo_pwm_channel", -1)),
            servo_pwm_frequency_hz=float(raw.get("servo_pwm_frequency_hz", 50)),
            servo_left_us=float(raw.get("servo_left_us", 1100)),
            servo_center_us=float(raw.get("servo_center_us", 1500)),
            servo_right_us=float(raw.get("servo_right_us", 1900)),
            watchdog_ms=int(raw.get("watchdog_ms", 250)),
            debounce_ms=int(raw.get("debounce_ms", 60)),
        )
        cfg.validate()
        return cfg

    @classmethod
    def safe_disabled(cls) -> "GpioConfig":
        return cls(
            enabled=False,
            gpiochip="/dev/gpiochip0",
            motor_dir_line=-1,
            start_line=-1,
            start_active_low=True,
            motor_direction_inverted=False,
            motor_pwm_chip=-1,
            motor_pwm_channel=-1,
            motor_pwm_frequency_hz=20000,
            motor_max_duty=0.65,
            servo_pwm_chip=-1,
            servo_pwm_channel=-1,
            servo_pwm_frequency_hz=50,
            servo_left_us=1100,
            servo_center_us=1500,
            servo_right_us=1900,
            watchdog_ms=250,
            debounce_ms=60,
        )

    def validate(self) -> None:
        if not 0.0 < self.motor_max_duty <= 1.0:
            raise GpioConfigurationError("motor_max_duty must be in (0, 1]")
        if not 100 <= self.watchdog_ms <= 1000:
            raise GpioConfigurationError("watchdog_ms must be in 100..1000")
        if not (
            500 <= self.servo_left_us < self.servo_center_us < self.servo_right_us <= 2500
        ):
            raise GpioConfigurationError(
                "servo pulse order must be 500 <= left < centre < right <= 2500 us"
            )
        if self.enabled:
            required = {
                "motor_dir_line": self.motor_dir_line,
                "start_line": self.start_line,
                "motor_pwm_chip": self.motor_pwm_chip,
                "motor_pwm_channel": self.motor_pwm_channel,
                "servo_pwm_chip": self.servo_pwm_chip,
                "servo_pwm_channel": self.servo_pwm_channel,
            }
            missing = [name for name, value in required.items() if value < 0]
            if missing:
                raise GpioConfigurationError(
                    "enabled=true but these mappings are unset: " + ", ".join(missing)
                )


class OrangePiGpioVehicle:
    """Owns GPIO/PWM resources and enforces local process-level safety."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = GpioConfig.load(config_path)
        self.state = OutputState.DRY_RUN if not self.config.enabled else OutputState.WAIT_START
        self.current_steer = 0
        self.current_speed = 0
        self._lock = threading.RLock()
        self._running = True
        self._last_control_time: Optional[float] = None
        self._motor_dir: Any = None
        self._start_button: Any = None
        self._motor_pwm: Any = None
        self._servo_pwm: Any = None
        self._last_direction: Optional[bool] = None

        if not self.config.enabled:
            print(
                f"GPIO output disabled: copy gpio_config.example.json to {config_path.name}, "
                "verify the physical mapping, then set enabled=true"
            )
            return

        try:
            self._open_hardware()
            self._write_safe_outputs()
            threading.Thread(target=self._button_loop, daemon=True).start()
            threading.Thread(target=self._watchdog_loop, daemon=True).start()
        except Exception:
            self.close()
            raise

    def _open_hardware(self) -> None:
        try:
            from periphery import GPIO, PWM
        except ImportError as exc:
            raise RuntimeError(
                "python-periphery is required for enabled Orange Pi GPIO output"
            ) from exc

        self._motor_dir = GPIO(self.config.gpiochip, self.config.motor_dir_line, "out")
        self._start_button = GPIO(self.config.gpiochip, self.config.start_line, "in")
        self._motor_pwm = PWM(self.config.motor_pwm_chip, self.config.motor_pwm_channel)
        self._servo_pwm = PWM(self.config.servo_pwm_chip, self.config.servo_pwm_channel)

        self._motor_pwm.frequency = self.config.motor_pwm_frequency_hz
        self._motor_pwm.duty_cycle = 0.0
        self._motor_pwm.enable()
        self._motor_dir.write(False)
        self._last_direction = False

        self._servo_pwm.frequency = self.config.servo_pwm_frequency_hz
        self._servo_pwm.duty_cycle = self._servo_duty(0)
        self._servo_pwm.enable()

    def _button_pressed(self) -> bool:
        raw = bool(self._start_button.read())
        return not raw if self.config.start_active_low else raw

    def _button_loop(self) -> None:
        try:
            previous = self._button_pressed()
            stable_since = time.monotonic()
            while self._running:
                current = self._button_pressed()
                now = time.monotonic()
                if current != previous:
                    previous = current
                    stable_since = now
                elif current and (now - stable_since) * 1000 >= self.config.debounce_ms:
                    self._toggle_arm()
                    while self._running and self._button_pressed():
                        time.sleep(0.01)
                    previous = False
                    stable_since = time.monotonic()
                time.sleep(0.01)
        except Exception as exc:
            self._background_fault("button", exc)

    def _toggle_arm(self) -> None:
        with self._lock:
            if self.state == OutputState.GPIO_DRIVE:
                self._enter_state(OutputState.WAIT_START)
            else:
                self._write_safe_outputs()
                self._last_control_time = time.monotonic()
                self.state = OutputState.GPIO_DRIVE
                print("GPIO state: GPIO_DRIVE; waiting for a fresh vision command")

    def _watchdog_loop(self) -> None:
        try:
            limit_s = self.config.watchdog_ms / 1000.0
            while self._running:
                with self._lock:
                    if (
                        self.state == OutputState.GPIO_DRIVE
                        and self._last_control_time is not None
                        and time.monotonic() - self._last_control_time > limit_s
                    ):
                        self._enter_state(OutputState.CONTROL_FAILSAFE)
                        print("GPIO state: CONTROL_FAILSAFE; physical re-arm required")
                time.sleep(min(0.02, limit_s / 4.0))
        except Exception as exc:
            self._background_fault("watchdog", exc)

    def _background_fault(self, source: str, exc: Exception) -> None:
        """Best-effort stop if a GPIO/watchdog worker fails."""
        print(f"GPIO {source} worker failed: {exc!r}; forcing safe outputs")
        with self._lock:
            try:
                self._enter_state(OutputState.CONTROL_FAILSAFE)
            except Exception as stop_exc:
                print(f"GPIO safe-output write also failed: {stop_exc!r}")

    def _enter_state(self, state: OutputState) -> None:
        self._write_safe_outputs()
        self._last_control_time = None
        self.state = state

    def _servo_duty(self, steer: int) -> float:
        steer = max(-100, min(100, int(steer)))
        if steer >= 0:
            pulse_us = self.config.servo_center_us + (
                self.config.servo_right_us - self.config.servo_center_us
            ) * steer / 100.0
        else:
            pulse_us = self.config.servo_center_us + (
                self.config.servo_center_us - self.config.servo_left_us
            ) * steer / 100.0
        return pulse_us * self.config.servo_pwm_frequency_hz / 1_000_000.0

    def _write_safe_outputs(self) -> None:
        self.current_steer = 0
        self.current_speed = 0
        if not self.config.enabled:
            return
        if self._motor_pwm is not None:
            self._motor_pwm.duty_cycle = 0.0
        if self._servo_pwm is not None:
            self._servo_pwm.duty_cycle = self._servo_duty(0)

    def set_control(self, steer: float, speed: float) -> None:
        steer_i = max(-100, min(100, int(round(steer))))
        speed_i = max(-100, min(100, int(round(speed))))
        with self._lock:
            if not self.config.enabled:
                self.current_steer = steer_i
                self.current_speed = speed_i
                return
            if self.state != OutputState.GPIO_DRIVE:
                self._write_safe_outputs()
                return

            direction = speed_i >= 0
            if self.config.motor_direction_inverted:
                direction = not direction

            # Preserve direction at zero speed; stop PWM before a real reversal.
            # 速度为零时保持方向；真正换向前先把PWM清零。
            if speed_i != 0 and direction != self._last_direction:
                self._motor_pwm.duty_cycle = 0.0
                self._motor_dir.write(direction)
                self._last_direction = direction
            self._servo_pwm.duty_cycle = self._servo_duty(steer_i)
            self._motor_pwm.duty_cycle = (
                abs(speed_i) / 100.0 * self.config.motor_max_duty
            )
            self.current_steer = steer_i
            self.current_speed = speed_i
            self._last_control_time = time.monotonic()

    def stop_and_wait(self) -> None:
        with self._lock:
            if self.config.enabled:
                self._enter_state(OutputState.WAIT_START)
            else:
                self.current_steer = 0
                self.current_speed = 0

    def close(self) -> None:
        with self._lock:
            self._running = False
            self._write_safe_outputs()
            self.state = OutputState.CLOSED
            for pwm in (self._motor_pwm, self._servo_pwm):
                if pwm is not None:
                    try:
                        pwm.disable()
                        pwm.close()
                    except Exception:
                        pass
            for gpio in (self._motor_dir, self._start_button):
                if gpio is not None:
                    try:
                        gpio.close()
                    except Exception:
                        pass
