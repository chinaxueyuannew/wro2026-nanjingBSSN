# 物料表与选型依据 / Bill of Materials and Selection Rationale

**当前配置：** USB摄像头是BOM中唯一的环境感知设备；当前不使用超声波或编码器反馈。

**Current configuration:** The USB camera is the only environmental sensor in the BOM; ultrasonic sensing and encoder feedback are not used.

本表区分“资料已确认”和“实物必须复核”的信息。最终装车后，两名队员应交叉确认品牌、型号、电压和数量。

This table separates information confirmed from available material from details that require physical verification. After final assembly, two team members should cross-check brands, models, voltages and quantities.

| 子系统 / Subsystem | 部件 / Component | 当前信息 / Current Information | 数量 / Qty. | 作用 / Purpose | 状态 / Status |
|---|---|---|---:|---|---|
| 机械 / Mechanical | 阿克曼底盘 / Ackermann chassis | 260×140×85 mm基础尺寸记录 / 260×140×85 mm base-size record | 1 | 前轮转向、四驱和差速 / Front steering, four-wheel drive and differentials | 最终装车尺寸待测 / Final assembled size pending |
| 机械 / Mechanical | 二维层板 / 2D plate | `models模型/HSP94182层板.dxf` | 1 set | 主控、摄像头和电源安装 / Controller, camera and power mounting | 文件已入库，实物待核 / File included; hardware pending |
| 计算 / Computing | 视觉计算机 / Vision computer | Orange Pi Zero 3W, Allwinner A733, 4 GB LPDDR5 | 1 | 图像采集、识别和决策 / Image capture, recognition and decisions | SKU确认，实机待验 / SKU confirmed; hardware pending |
| 计算与控制 / Compute and control | 主控与执行控制器 / Main and execution controller | Orange Pi Zero 3W 4GB | 1 | 视觉、策略、GPIO/PWM执行和进程级失效停车 / Vision, strategy, GPIO/PWM execution and process-level fail-safe | 当前架构；GPIO映射待实物冻结 / Current architecture; physical mapping pending |
| 上一版本 / Previous version | Arduino UNO R3 | 不安装于当前车辆 / Not installed on the current vehicle | 0 | 上一版串口执行控制 / Previous serial execution control | 仅保留历史程序 / Historical code only |
| 驱动 / Drive | 电机驱动器 / Motor driver | AT8236 or DRV8701/MD02 Pro | 1 | 放大控制信号并驱动电机 / Amplify control signals and drive motor | 实物二选一 / Select from actual hardware |
| 驱动 / Drive | 带编码器接口电机 / Motor with encoder interface | 6–12 V, 12 CPR, 1:8.864, dual channel | 1 set | 当前只提供四轮动力 / Currently supplies four-wheel drive only | 反馈不使用 / Feedback not used |
| 转向 / Steering | 舵机 / Servo | 4.5–7 V, 10 kg·cm, 400–800 mA | 1 | 前轮转向 / Front-wheel steering | 规格确认，待实测 / Specification confirmed; measurement pending |
| 感知 / Perception | USB摄像头 / USB camera | GC0308/HBVCAM, 160°, distorted, 30 FPS colour, non-night-vision, 480p | 1 | 赛道和红绿障碍视觉 / Track and red-green obstacle vision | SKU确认，待实测 / SKU confirmed; measurement pending |
| 电源 / Power | 电池 / Battery | 团队早期实验使用11.1 V锂电 / Earlier team experiments used 11.1 V lithium | 1 | 整车能量 / Vehicle energy | 最终型号待核 / Final model pending |
| 电源 / Power | 稳压模块 / Regulators | 型号待确认 / Model pending | 一个或多个 / One or more | 稳定供电 / Regulated power | 待核 / Pending |
| 安全 / Safety | 总开关 / Main switch | 型号待确认 / Model pending | 1 | 一次动作上电 / Single-action power-on | 待核 / Pending |
| 安全 / Safety | 启动按钮 / Start button | 常开按钮接GND / Normally-open button to GND | 1 | 独立启动程序 / Independent program start | 程序支持，实物待装 / Software supported; hardware pending |
| 结构 / Structure | 紧固件与支架 / Fasteners and brackets | 建议M3，按实物确认 / M3 suggested; verify physically | 若干 / Several | 固定设备和线束 / Secure devices and wiring | 待核 / Pending |

当前BOM不包含前方或右侧超声波。底盘编码器接口不接线、不读取、不做闭环；相关程序只是历史示例。

The current BOM contains no front or right ultrasonic sensor. Chassis encoder interfaces are not wired, read or used in closed-loop control; related programs are historical examples only.

## 选型逻辑 / Selection Rationale

### 当前Orange Pi GPIO直控 / Current Orange Pi Direct GPIO Control

当前版本由Orange Pi同时完成视觉决策与GPIO/PWM执行。电机方向、启动按钮使用3.3 V GPIO，电机速度和舵机使用内核PWM。优点是减少一块控制器和串口链路；代价是Linux进程和GPIO输出属于同一故障域，必须使用上电默认停车、物理按钮、进程级250 ms看门狗、退出清零和实测最坏停车距离。实际GPIO line与PWM chip/channel必须从冻结镜像和实物排针确认。

The current version performs both vision decisions and GPIO/PWM execution on the Orange Pi. A 3.3 V GPIO controls motor direction and the physical start button, while kernel PWM controls motor speed and steering. This removes one controller and the serial link, but places Linux processing and actuator output in one failure domain. Stopped-by-default startup, a physical button, a 250 ms process-level watchdog, zero-on-exit and measured worst-case stopping distance are therefore required. Actual GPIO lines and PWM chip/channel values must be confirmed from the frozen image and physical header.

### 上一版Arduino UNO / Previous Arduino UNO Version

Arduino UNO串口执行程序属于上一版本，当前车辆不安装、不供电、不接线。程序保留用于说明迭代过程和两级控制方案的取舍，不能在当前接线图或比赛车辆配置中标为执行控制器。

The Arduino UNO serial executor belongs to the previous version and is not installed, powered or wired in the current vehicle. Its code remains as engineering-history evidence and to explain the trade-off of a two-controller architecture; it must not be presented as the current execution controller or wiring.

### ESP32

ESP32代码是团队早期自主实验版本，当前车辆不使用。若未来更换，必须关闭Wi-Fi和蓝牙，并重新验证接线和安全逻辑。

The ESP32 code is an earlier team-developed experimental version and is not used by the current vehicle. If adopted later, Wi-Fi and Bluetooth must be disabled and all wiring and safety logic revalidated.

### Orange Pi Zero 3W 4GB

团队购买的是带字母W的A733八核Zero 3W 4GB版本，不是H618四核Zero 3。它负责Linux、OpenCV、赛道与障碍识别、高层决策以及GPIO/PWM执行。比赛时关闭Wi-Fi 6和Bluetooth 5.4。独立供电按5 V/3 A设计。

The team purchased the A733 octa-core Zero 3W 4GB version with the letter W, not the H618 quad-core Zero 3. It runs Linux, OpenCV, track/obstacle recognition, high-level decisions and GPIO/PWM execution. Wi-Fi 6 and Bluetooth 5.4 must be disabled during competition. Use an independent 5 V/3 A supply.

### USB彩色摄像头 / USB Colour Camera

160°、30 FPS彩色SKU保留红绿信息，适合障碍分类。团队购买记录中的“1920×1080”与30万像素、480p相互矛盾，因此文档以SKU明确的480p为暂定值，并要求用UVC枚举确定实机模式。

The 160°, 30 FPS colour SKU preserves red-green information for obstacle classification. The team purchase record lists both “1920×1080” and conflicting 0.3-megapixel/480p information, so 480p is retained only as a provisional value until UVC enumeration establishes the actual mode.

### AT8236与DRV8701 / AT8236 and DRV8701

AT8236示例用双PWM控制，DRV8701/MD02 Pro示例使用PWM和DIR。程序必须分开维护，最终只有实车驱动器可标为比赛版本。

AT8236 examples use dual-PWM control, while DRV8701/MD02 Pro examples use PWM and DIR. Keep their programs separate; only the driver installed on the vehicle may be marked as the competition version.

## 待补证据 / Evidence Still Required

- 关键部件正反面和标签照片 / Front, rear and label photographs of key components.
- 购买链接或规格书存档 / Archived purchase links or datasheets.
- 实测质量、电压、典型和峰值电流 / Measured mass, voltage, typical current and peak current.
- 车上安装位置 / Installed location on the vehicle.
- 替代件和需要重新标定的参数 / Alternatives and parameters requiring recalibration.
