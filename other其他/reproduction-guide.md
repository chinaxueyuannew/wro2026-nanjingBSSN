# 完整复现指南 / Complete Reproduction Guide

> 目标：未参与开发的队员仅凭仓库，在不口头询问原开发者的情况下恢复当前纯视觉、Orange Pi GPIO/PWM直控车辆。 / Goal: a member who did not develop the system can restore the current vision-only, direct Orange Pi GPIO/PWM vehicle using only this repository and no verbal help.

## 1. 当前配置边界 / Current Configuration Boundary

- 安装：阿克曼四驱底盘、Orange Pi Zero 3W 4GB、USB彩色摄像头、PWM/DIR电机驱动器、转向舵机、物理启动/停止按钮和独立供电分支。 / Installed: four-wheel-drive Ackermann chassis, Orange Pi Zero 3W 4GB, USB colour camera, PWM/DIR motor driver, steering servo, physical start/stop button and separate power branches.
- 不安装：Arduino、超声波和编码器信号。 / Not installed: Arduino, ultrasonic sensors or encoder signals.
- 当前控制：Orange Pi直接输出GPIO/PWM；无板间串口。 / Current control: direct Orange Pi GPIO/PWM output; no inter-board serial link.
- 历史目录中的Arduino/ESP32程序只用于研发追溯。 / Arduino/ESP32 programs in historical folders are for development traceability only.

## 2. 所需工具 / Required Tools

- 带电流限制的台式电源或已核验电池、保险和总开关 / Current-limited bench supply or verified battery, fuse and main switch.
- 万用表、示波器或逻辑分析仪 / Multimeter, oscilloscope or logic analyser.
- 直尺、卡尺、电子秤和地面画圆工具 / Ruler, callipers, scale and ground-circle tools.
- Orange Pi系统镜像、读卡器、USB键盘/屏幕或有线调试方式 / Orange Pi image, card reader and local keyboard/display or wired debugging.
- Python 3、OpenCV、NumPy、python-periphery和libgpiod工具 / Python 3, OpenCV, NumPy, python-periphery and libgpiod tools.
- 摄像头标定板、稳定支架和充足光照 / Camera calibration board, rigid mount and suitable lighting.

## 3. 机械装配 / Mechanical Assembly

1. 依据 [`../models模型/README.md`](../models模型/README.md)核对轴距、轮距、轮径、转向连杆和传动。 / Use the mechanical guide to verify wheelbase, track, wheel diameter, steering links and drivetrain.
2. 固定Orange Pi和摄像头，确保视野无遮挡、线束不进入转向或传动机构。 / Mount the Orange Pi and camera; keep the view clear and wiring away from steering and drivetrain parts.
3. 固定电源、驱动器、舵机支路和总开关，重物尽量低且靠近车体中心。 / Secure the power system, driver, servo branch and main switch; keep heavy parts low and near the centre.
4. 在完整比赛配置下记录最终长、宽、高、质量、重心趋势和六视图。 / Record final dimensions, mass, centre-of-gravity trend and six views in complete competition configuration.

## 4. GPIO/PWM映射冻结 / GPIO/PWM Mapping Freeze

实际映射不能从名称猜测，必须在最终比赛镜像上完成：

Do not guess mappings from names; complete the following on the final competition image:

```bash
uname -a
cat /etc/os-release
gpiodetect
gpioinfo
ls -l /dev/gpiochip*
find /sys/class/pwm -maxdepth 3 -type f -o -type l
```

1. 在排针图、SoC手册、设备树和枚举输出之间建立物理针脚 → gpiochip/line、PWM chip/channel的对照表。 / Build a physical-header-to-gpiochip/line and PWM chip/channel table from the header map, SoC documentation, device tree and enumeration output.
2. 检查PWM通道没有被风扇、显示或其他overlay占用。 / Confirm PWM channels are not owned by a fan, display or another overlay.
3. 确认电机驱动器输入兼容3.3 V，物理按钮使用外部上拉，所有控制地相连。 / Confirm driver inputs accept 3.3 V, the physical button uses an external pull-up and all control grounds are common.
4. 把 [`../src源代码/gpio_config.example.json`](../src源代码/gpio_config.example.json) 复制为本地 `gpio_config.json`，填写映射但保持 `enabled=false`。 / Copy the example to local `gpio_config.json`, enter mappings but keep `enabled=false`.
5. 由程序和电子队员共同核对并签字，再允许启用。 / Programming and electronics members cross-check and sign before enabling.

## 5. 配电与接线 / Power Distribution and Wiring

按照 [`../schemes原理图/wiring.md`](../schemes原理图/wiring.md) 和 [`../schemes原理图/system-wiring.png`](../schemes原理图/system-wiring.png) 连接：

Wire according to the wiring guide and formal diagram:

1. 电池经保险和总开关进入配电。 / Battery enters distribution through a fuse and main switch.
2. 电机驱动器使用动力支路；Orange Pi使用独立稳压5 V/3 A支路；舵机使用独立4.5–7 V支路。 / Use a motor-power branch, an independent regulated 5 V/3 A Orange Pi branch and a separate 4.5–7 V servo branch.
3. USB摄像头直接接Orange Pi。 / Connect the USB camera directly to the Orange Pi.
4. Orange Pi的方向GPIO与电机PWM接驱动器，舵机PWM接舵机，按钮GPIO接常开按钮与外部上拉。 / Connect Orange Pi direction GPIO and motor PWM to the driver, steering PWM to the servo, and button GPIO to the normally-open button with external pull-up.
5. 控制共地；电机大电流回流短且与USB/信号线分开。 / Use a common control ground; keep high-current motor returns short and separated from USB/signal wiring.
6. 负载不得由Orange Pi排针供电。 / Do not power actuator loads from the Orange Pi header.

## 6. 软件恢复 / Software Restoration

```bash
cd src源代码
python3 -m pip install -r requirements.txt
python3 -m py_compile bev_road.py bev_segmentation.py orange_pi_gpio.py
cp gpio_config.example.json gpio_config.json
```

记录OS、内核、Python、OpenCV、NumPy和python-periphery版本，并保存 `gpio_config.json` 哈希但不要提交含本机映射的文件，除非团队决定公开最终映射。

Record OS, kernel, Python, OpenCV, NumPy and python-periphery versions, and save the `gpio_config.json` hash. Do not commit the machine-specific mapping unless the team decides to publish the final mapping.

先保持 `enabled=false`：

Keep `enabled=false` first:

```bash
python3 bev_segmentation.py --video-in 0 --mode cw --gpio-config gpio_config.json
```

确认界面为 `DRY_RUN`、默认速度0、视频丢失后目标归零。再用录像完成透视、HSV和方向策略调试。

Confirm `DRY_RUN`, zero default speed and zero target after video loss. Then tune perspective, HSV and direction strategy using recordings.

## 7. 首次硬件启用 / First Hardware Enable

1. 断开电机动力，启用配置，只测GPIO输入和PWM空载波形。 / Disconnect motor power, enable the configuration and test only GPIO input and unloaded PWM waveforms.
2. 测量电机PWM频率、舵机50 Hz及最小/中位/最大脉宽。 / Measure motor PWM frequency, steering 50 Hz and minimum/centre/maximum pulse widths.
3. 连接驱动器逻辑但保持动力断开，核实有效电平和方向符号。 / Connect driver logic with motor power still disconnected; verify active levels and direction sign.
4. 抬起驱动轮，使用限流电源和最低输出完成G-01至G-10。 / Lift the driven wheels and perform G-01 through G-10 using a current-limited supply and minimum output.
5. 特别测量250 ms看门狗、物理停止、摄像头断开、异常退出和方向变化前归零。 / Specifically measure the 250 ms watchdog, physical stop, camera loss, exception exit and zero-before-direction-change.
6. 只有程序、电子和教练共同签字后才进行地面低速测试。 / Begin low-speed ground testing only after programming, electronics and coach sign-off.

## 8. 标定与整车验收 / Calibration and Vehicle Acceptance

1. 标定摄像头内参与畸变、安装姿态、ROI和透视点。 / Calibrate camera intrinsics/distortion, mounting pose, ROI and perspective points.
2. 在多光照数据集上标定红绿HSV，报告precision、recall和F1。 / Tune red-green HSV on a multi-lighting dataset and report precision, recall and F1.
3. 标定舵机中位、左右安全脉宽、转向符号、最小转弯半径和速度档位。 / Calibrate steering centre, safe pulse limits, steering sign, minimum turning radius and speed levels.
4. 测量静态、视觉、电机启动和最大转向时的各支路电压电流。 / Measure branch voltage/current at idle, vision processing, motor start and maximum steering.
5. 完成顺/逆时针直线、弯道、障碍、完整回合、停车区、30分钟稳定性和最坏停车距离测试。 / Complete CW/CCW straight, turn, obstacle, full-lap, parking, 30-minute stability and worst-case stopping-distance tests.

## 9. 单板安全边界 / Single-board Safety Boundary

当前视觉与执行在同一Orange Pi。进程看门狗可覆盖控制循环停止，但不能保证覆盖Linux内核或PWM整体冻结。在可立即断电、抬轮和限流条件下完成故障注入，并根据结果决定是否加入独立硬件使能门、驱动器硬件使能失效保护或常闭急停。未完成前不得声称已覆盖所有处理器冻结故障。

Vision and execution share one Orange Pi. The process watchdog covers a stopped control loop but cannot guarantee stopping during a complete Linux-kernel or PWM freeze. Perform fault injection with immediate power removal, lifted wheels and current limiting, then decide on an independent hardware enable gate, driver-enable fail-safe or normally-closed emergency stop. Do not claim full processor-freeze coverage before this is complete.

## 10. 独立复现验收 / Independent Reproduction Acceptance

未参与编程的队员应仅依据仓库完成：定位文件、恢复镜像、枚举GPIO/PWM、核对映射、安装依赖、执行DRY_RUN、解释状态机、完成抬轮G-01至G-10、找到日志并指出上一版本与当前版本边界。记录总用时、卡住步骤和修改建议。只有不需要口头补充且所有关键映射有证据时，才能声明“完全可复现”。

A member who did not write the software must use only the repository to locate files, restore the image, enumerate GPIO/PWM, verify mapping, install dependencies, run DRY_RUN, explain the state machine, complete lifted-wheel G-01 through G-10, locate logs and identify the previous/current version boundary. Record total time, blocked steps and proposed edits. Claim “fully reproducible” only when no verbal additions are needed and every critical mapping has evidence.
