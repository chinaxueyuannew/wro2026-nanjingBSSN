# Orange Pi Zero 3W 4GB 车载计算与控制平台 / Onboard Computing and Control Platform

> 当前版本由Orange Pi同时完成视觉、决策和GPIO/PWM执行；Arduino属于上一版本且不安装。 / In the current version, the Orange Pi performs vision, decisions and GPIO/PWM execution; Arduino belongs to the previous version and is not installed.

## 1. 角色 / Role

Orange Pi接收USB摄像头画面，运行OpenCV视觉、方向判断、红绿障碍策略、恢复逻辑和安全状态机，并直接通过GPIO/PWM控制物理按钮输入、转向舵机和PWM/DIR电机驱动器。比赛运行不依赖互联网、云服务、手机或无线遥控。

The Orange Pi receives USB-camera frames, runs OpenCV vision, direction detection, red-green obstacle strategy, recovery logic and the safety state machine, and directly controls the physical button input, steering servo and PWM/DIR motor driver through GPIO/PWM. Competition operation does not depend on the Internet, cloud services, a phone or wireless remote control.

## 2. 已记录配置 / Recorded Configuration

团队当前使用 **Orange Pi Zero 3W 4GB**。采购信息记录全志A733八核平台、4 GB内存、USB、Wi-Fi 6、蓝牙5.4、Mini HDMI 2.0和PCIe 3.0等信息。比赛真正使用的能力是USB主机、Linux/OpenCV、本地存储、GPIO和PWM；无线功能必须关闭。处理器宣传参数不能替代最终实机枚举与压力测试。

The team currently uses an **Orange Pi Zero 3W 4GB**. Purchase records note an Allwinner A733 octa-core platform, 4 GB memory, USB, Wi-Fi 6, Bluetooth 5.4, Mini HDMI 2.0 and PCIe 3.0. Competition-relevant capabilities are USB host, Linux/OpenCV, local storage, GPIO and PWM; wireless functions must be disabled. Advertised processor specifications do not replace final hardware enumeration and stress testing.

## 3. 选择理由与取舍 / Selection Rationale and Trade-offs

| 选择 / Choice | 优点 / Benefit | 代价 / Cost | 缓解 / Mitigation |
|---|---|---|---|
| Linux SBC处理视觉 / Linux SBC for vision | OpenCV生态、调试工具、USB摄像头支持 / OpenCV ecosystem, diagnostics and USB-camera support | 启动和调度不如微控制器确定 / Less deterministic startup and scheduling than an MCU | 固定镜像、禁用无关服务、离线启动测试 / Freeze image, disable services, test offline startup |
| 同板GPIO/PWM执行 / Same-board GPIO/PWM execution | 减少控制器、线束、协议和板间延迟 / Fewer controllers, wires, protocols and inter-board latency | 视觉与执行共享故障域 / Vision and execution share a fault domain | 默认停车、物理按钮、进程看门狗、故障注入与硬件失效保护评估 / Stopped default, physical button, process watchdog, fault injection and hardware-fail-safe assessment |
| USB单摄像头 / Single USB camera | 同时获得边界、颜色和方向信息 / Borders, colour and direction in one sensor | 光照、畸变、遮挡和掉帧敏感 / Sensitive to lighting, distortion, occlusion and frame drops | 标定、固定安装、低置信度减速、帧超时 / Calibration, rigid mount, low-confidence slowdown, frame timeout |

## 4. GPIO/PWM资源冻结 / GPIO/PWM Resource Freeze

Orange Pi的物理排针号、SoC管脚名、设备树功能、libgpiod line号以及PWM chip/channel并不等价。当前仓库故意把实际映射设为 `-1`，避免在未确认的板卡或镜像上误动作。

Orange Pi physical-header numbers, SoC pin names, device-tree functions, libgpiod line numbers and PWM chip/channels are not interchangeable. The repository intentionally sets real mappings to `-1` to prevent unintended motion on an unverified board or image.

最终冻结表 / Final freeze table:

| 功能 / Function | 物理排针 / Header Pin | gpiochip/line或PWM chip/channel | 复用/overlay | 有效电平 / Active Level | 证据 / Evidence |
|---|---|---|---|---|---|
| 电机方向 / Motor direction | 待填 / Pending | 待填 / Pending | 待填 / Pending | 待填 / Pending | gpioinfo + 示波器 / gpioinfo + scope |
| 电机速度PWM / Motor-speed PWM | 待填 / Pending | 待填 / Pending | 待填 / Pending | 高有效待核 / Verify active high | sysfs + scope |
| 舵机PWM / Steering PWM | 待填 / Pending | 待填 / Pending | 待填 / Pending | 正脉冲 / Positive pulse | sysfs + scope |
| 启动/停止按钮 / Start-stop button | 待填 / Pending | 待填 / Pending | GPIO input | 外部上拉、按下为低 / External pull-up, active low | gpioinfo + multimeter |

冻结命令 / Freeze commands:

```bash
uname -a
cat /etc/os-release
gpiodetect
gpioinfo
ls -l /dev/gpiochip*
find /sys/class/pwm -maxdepth 3 -type f -o -type l
```

每次更换镜像、内核、设备树、排针或overlay后必须重新核验。不能把其他Orange Pi型号或不同镜像中的管脚号直接复制到本车。

Reverify after any image, kernel, device-tree, header or overlay change. Never copy pin numbers from another Orange Pi model or a different image directly into this vehicle.

## 5. 直接控制实现 / Direct-Control Implementation

`orange_pi_gpio.py`使用python-periphery访问字符设备GPIO与内核PWM。硬件访问延迟导入，因此 `enabled=false` 的DRY_RUN不需要打开硬件设备。现行职责如下：

`orange_pi_gpio.py` uses python-periphery for character-device GPIO and kernel PWM. Hardware access is imported lazily, so DRY_RUN with `enabled=false` opens no hardware devices. Current responsibilities are:

- GPIO输入去抖并实现物理启动/停止。 / Debounce the GPIO input for physical start/stop.
- GPIO输出电机方向。 / Output motor direction through GPIO.
- PWM输出电机速度和舵机脉宽。 / Output motor speed and steering pulse width through PWM.
- 把逻辑量限制在 `-100...100`，把舵机限制在配置脉宽范围。 / Bound logical values to `-100...100` and steering to configured pulse widths.
- 方向改变前先把电机占空比置零。 / Set motor duty to zero before changing direction.
- 250 ms无新控制更新后停车并要求重新授权。 / Stop and require re-arming after 250 ms without a fresh update.
- 异常、Ctrl+C和退出时清零、禁用并关闭资源。 / Zero, disable and close resources on exceptions, Ctrl+C and exit.

## 6. 电气约束 / Electrical Constraints

1. Orange Pi GPIO仅为逻辑信号，不得给舵机、电机或驱动器动力端供电。 / Orange Pi GPIO is logic-only and must not power the servo, motor or driver power stage.
2. Orange Pi使用独立稳压 **5 V / 3 A** 支路，舵机使用独立4.5–7 V支路，电机使用动力支路。 / Use an independent regulated **5 V / 3 A** Orange Pi branch, a separate 4.5–7 V servo branch and a motor-power branch.
3. 所有控制信号共地；大电流回流短且与USB、GPIO和摄像头线分开。 / All control signals share ground; high-current returns are short and separated from USB, GPIO and camera wiring.
4. 电机驱动器方向/PWM输入必须确认兼容3.3 V；否则使用合适的电平转换或缓冲。 / Confirm motor-driver direction/PWM inputs accept 3.3 V; otherwise use an appropriate level shifter or buffer.
5. 物理按钮使用外部上拉，避免依赖未验证的内部偏置。 / Use an external pull-up for the physical button rather than an unverified internal bias.
6. 最终保险、线径、稳压额定值和散热必须依据实测电流与温升确定。 / Determine fuse, wire gauge, regulator rating and cooling from measured current and temperature rise.

## 7. 启动与运行基线 / Startup and Runtime Baseline

| 项目 / Item | 要求 / Requirement | 证据 / Evidence |
|---|---|---|
| 冷启动 / Cold boot | 无网络、无人机交互，进入停车状态 / No network or user interaction; enter stopped state | 五次冷启动视频与日志 / Five cold-boot videos and logs |
| 摄像头枚举 / Camera enumeration | 固定设备识别策略，避免 `/dev/videoN`漂移 / Stable device identification, not fragile `/dev/videoN` assumptions | UVC枚举 / UVC enumeration |
| 配置 / Configuration | 缺失或非法映射时拒绝启用 / Refuse enable on missing or invalid mapping | G-01日志 / G-01 log |
| 按钮 / Button | 上电不运动，去抖后才授权 / No power-on motion; arm only after debounce | G-02/G-03 |
| 看门狗 / Watchdog | 控制更新年龄超过250 ms停车 / Stop when control age exceeds 250 ms | G-05五次测量 / Five G-05 measurements |
| 退出 / Exit | 电机PWM归零、舵机回中、PWM禁用 / Motor PWM zero, steering centred, PWM disabled | G-09 |
| 稳定性 / Stability | 30分钟无重启、无资源泄漏、温度可接受 / 30 minutes without restart or resource leak; acceptable temperature | R-03日志 / R-03 log |

## 8. 故障域与硬件保护决策 / Fault Domain and Hardware Protection Decision

进程看门狗与控制进程位于同一Linux系统。它能在主控制循环停止更新时独立调用停车，但若内核、PWM驱动、供电或整板冻结，就不一定有机会执行。这是从双控制器架构切换到单板直控后必须公开说明的取舍。

The watchdog and controller share one Linux system. It can call stop independently when the main control loop stops updating, but may not run if the kernel, PWM driver, power or whole board freezes. This trade-off must be stated openly after moving from a two-controller architecture to single-board direct control.

关闭该风险前需完成：

Before closing this risk:

1. 抬轮、限流和可立即断电条件下完成进程挂起、线程停止、设备异常和受控系统失联测试。 / Test process suspension, stopped threads, device errors and controlled system unresponsiveness with lifted wheels, current limiting and immediate power removal.
2. 记录失效时PWM是否保持最后值、归零或禁用。 / Record whether PWM holds the last value, goes to zero or disables on each fault.
3. 依据结果决定是否增加独立硬件使能门、驱动器EN下拉、硬件看门狗或常闭急停。 / Decide on an independent enable gate, driver-EN pull-down, hardware watchdog or normally-closed emergency stop from the results.
4. 在FMEA、接线图、BOM与测试表中同步最终决定。 / Synchronise the final decision in the FMEA, wiring diagram, BOM and test table.

## 9. 上一版本说明 / Previous-Version Note

上一版本由Orange Pi运行视觉，通过115200 baud文本串口向Arduino发送转向和速度，Arduino负责D2/D6/D7/D8输出。该架构、配置和程序保留在仓库中用于说明迭代过程，但不应出现在当前装车、当前运行命令或当前验收结果中。

The previous version ran vision on the Orange Pi and sent steering and speed over a 115200-baud text serial link to an Arduino that owned D2/D6/D7/D8 outputs. This architecture, configuration and code remain for iteration history but must not appear in current assembly, run commands or acceptance results.
