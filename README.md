# 南京博颂学校 | 2026 WRO Future Engineers 工程材料 / Engineering Materials

> 本页面所有内容均为中文与英文直接对照。 / All content on this page is presented directly in Chinese and English.

本仓库是 **南京博颂学校 / BONA SONORITY SCHOOL NANJING** 参加 2026 WRO Future Engineers 的公开工程材料，沿用官方 Future Engineers 模板，记录底盘、机电集成、Orange Pi视觉算法、Arduino底层控制、测试、安全分析、团队资料与演示视频。

This public repository documents the 2026 WRO Future Engineers project of **BONA SONORITY SCHOOL NANJING**. It follows the official Future Engineers template and records the chassis, mechatronic integration, Orange Pi vision, Arduino execution control, tests, safety analysis, team materials and demonstration video.

车辆以 **RF-A101HE-109010203 阿克曼四驱底盘**为机械基础，只使用 **USB彩色摄像头**进行环境感知。**Orange Pi Zero 3W 4GB**运行视觉算法和高层策略，并通过有线串口向 **Arduino UNO**发送转向与速度目标；Arduino负责舵机、电机驱动、启动状态和命令超时停车。当前车辆不使用超声波，也不使用编码器闭环。

The vehicle is based on an **RF-A101HE-109010203 four-wheel-drive Ackermann chassis** and uses a **USB colour camera as its only environmental sensor**. An **Orange Pi Zero 3W 4GB** runs perception and high-level strategy and sends wired steering and speed targets to an **Arduino UNO**. The Arduino controls the steering servo, motor driver, start state and command-timeout stop. The current vehicle uses neither ultrasonic sensing nor encoder feedback.

## 演示视频 / Driving Video

### [▶ YouTube：2026 WRO Future Engineers | 南京博颂学校 | Autonomous Driving Demonstration](https://youtu.be/DJcxiJCEFdo)

[![南京博颂学校自动驾驶演示 / Autonomous driving demonstration](https://img.youtube.com/vi/DJcxiJCEFdo/hqdefault.jpg)](https://youtu.be/DJcxiJCEFdo)

视频详情、原片参数与版本记录见 [`video视频/video.md`](video视频/video.md)。

See [`video视频/video.md`](video视频/video.md) for video details, local-file specifications and version records.

## 队伍与赛事成果 / Team and Competition

### 南京博颂学校 / BONA SONORITY SCHOOL NANJING

[![南京博颂学校队旗 / School flag](t-photos团队照片/team-flag.jpg)](t-photos团队照片/team-flag.jpg)

我们围绕视觉无人驾驶阿克曼车辆开展程序、结构和电子系统协作。

We collaborate on programming, mechanical structure and electronics for a vision-based autonomous Ackermann vehicle.

| 姓名 / Name | 分工 / Role |
|---|---|
| 陆昭颖 / Lu Zhaoying | 程序 / Programming |
| 张隽泽 / Zhang Junze | 结构 / Mechanical Structure |
| 黄鸣博 / Huang Mingbo | 电子 / Electronics |
| 薛源 / Xue Yuan | 教练 / Coach |

[查看完整团队介绍 / Read the full team profile](other其他/team-profile.md)

### 成员照片 / Member Portraits

| 陆昭颖 🏳️‍🌈 / Lu Zhaoying | 张隽泽 / Zhang Junze | 黄鸣博 / Huang Mingbo |
|---|---|---|
| <a href="t-photos团队照片/陆昭颖.jpg"><img src="t-photos团队照片/陆昭颖.jpg" alt="陆昭颖，程序 / Lu Zhaoying, Programming" width="280"></a> | <a href="t-photos团队照片/张隽泽.jpg"><img src="t-photos团队照片/张隽泽.jpg" alt="张隽泽，结构 / Zhang Junze, Mechanical Structure" width="280"></a> | <a href="t-photos团队照片/黄鸣博.jpg"><img src="t-photos团队照片/黄鸣博.jpg" alt="黄鸣博，电子 / Huang Mingbo, Electronics" width="280"></a> |

[陆昭颖形象照 / Additional portrait of Lu Zhaoying](t-photos团队照片/陆昭颖形象照.jpg)

### 正式团队照 / Official Team Photograph

[![南京博颂学校WRO未来工程师参赛队 / WRO Future Engineers team](t-photos团队照片/team-official.jpg)](t-photos团队照片/team-official.jpg)

### 2026 WRO中国区选拔赛（北京站）未来工程师无人驾驶冠军 / 2026 WRO China Qualification Tournament (Beijing) Future Engineers Autonomous Driving Champion

[![北京站冠军领奖照片 / Beijing championship award photograph](t-photos团队照片/award-beijing-champion.jpg)](t-photos团队照片/award-beijing-champion.jpg)

### 车辆比赛现场 / Vehicle on the Competition Field

[![车辆比赛现场 / Vehicle on the competition field](v-photos车辆照片/vehicle-competition-run.jpg)](v-photos车辆照片/vehicle-competition-run.jpg)

更多研发记录见[制作过程照片索引](t-photos团队照片/README.md)。车辆标准六视图仍待补充。

See the [development-process photo index](t-photos团队照片/README.md) for more records. The standard six-view vehicle photographs are still pending.

## 快速跳转 / Quick Navigation

- [2026五维评分证据地图 / 2026 rubric evidence map](other其他/scoring-evidence.md) · [可归档工程日志PDF / Archival engineering-log PDF](other其他/engineering-log.pdf) · [实测与照片证据登记 / Evidence register](other其他/evidence-register.md)
- [团队介绍 / Team profile](other其他/team-profile.md) · [系统概述 / System overview](#2-系统概述--system-overview) · [机械设计 / Mechanical design](#3-移动性与机械设计--mobility-and-mechanical-design) · [动力与视觉 / Power and vision](#4-动力与视觉架构--power-and-vision-architecture)
- [源代码 / Source code](src源代码/README.md) · [接线与供电 / Wiring and power](schemes原理图/wiring.md) · [正式PNG接线图 / Formal PNG wiring diagram](schemes原理图/system-wiring.png) · [机械模型 / Mechanical models](models模型/README.md) · [物料表 / BOM](other其他/BOM.md)
- [测试 / Tests](other其他/tests.md) · [工程日志 / Engineering log](other其他/engineering-log.md) · [FMEA](other其他/FMEA.md) · [比赛检查表 / Competition checklist](other其他/competition-checklist.md)
- [团队照片 / Team photos](t-photos团队照片/README.md) · [车辆照片 / Vehicle photos](v-photos车辆照片/README.md) · [视频 / Video](video视频/video.md) · [完整索引 / Complete index](#10-完整文件索引--complete-file-index)

## 当前成果状态 / Current Project Status

| 项目 / Item | 仓库状态 / Repository Status | 验证状态 / Validation Status |
|---|---|---|
| 阿克曼底盘 / Ackermann chassis | 已有机械说明和层板DXF / Mechanical description and plate DXF included | 现有规格记录已整理，最终装车尺寸待测 / Existing specification record documented; final assembled dimensions pending |
| 超声波与编码器代码 / Ultrasonic and encoder code | 团队早期自主实验代码已入库 / Earlier team-developed experimental code included | 当前车辆不使用 / Not used by the current vehicle |
| 道路预处理 / Road preprocessing | `bev_road.py` 已入库 / Included | 透视参数仍需实车标定 / Perspective parameters require vehicle calibration |
| 红绿视觉控制 / Red-green vision control | `bev_segmentation.py` 已入库 / Included | 当前主要方向，仍需板端和实车验证 / Current main approach; board and vehicle validation pending |
| UNO视觉安全执行 / UNO vision safety execution | `VisionSerialExecutor.ino` 已实现并通过UNO目标编译 / Implemented and built for the UNO target | 上电停车、D8启动、解析/限幅和250 ms看门狗已闭环；待实物上传、驱动器和车辆验证 / Power-on stop, D8 start, parsing/limits and 250 ms watchdog are closed in code; physical upload, driver and vehicle validation pending |
| 接线与配电 / Wiring and distribution | PNG/SVG图、引脚、供电和协议已入库 / PNG/SVG, pins, power and protocol included | 准确器件型号、额定值和支路电流待实物核验 / Exact models, ratings and branch currents require physical verification |
| 评分与工程日志 / Rubric and engineering log | 五维证据地图、缺失证据登记、双语PDF已入库 / Five-dimension map, gap register and bilingual PDF included | 实测后需更新PDF和签署 / PDF and sign-off require update after measurements |
| 驾驶演示 / Driving demonstration | YouTube链接和87.07 MiB视频已入库 / YouTube link and 87.07 MiB video included | 拍摄日期、提交号和硬件对应表待补 / Date, commit and hardware mapping pending |
| 团队材料 / Team materials | 队旗、介绍、三名成员照、正式照、冠军照和11张过程照已入库 / Flag, profile, three portraits, official photo, award photo and 11 process photos included | 趣味团队照待补 / Informal team photo pending |
| 车辆照片 / Vehicle photos | 比赛现场照片和六视图规范已入库 / Competition photo and six-view specification included | 标准六视图待补 / Standard six views pending |

![团队制作过程 / Team development process](t-photos团队照片/making-process-01-team-workshop.jpg)

## 1. 仓库导航 / Repository Navigation

| 目录或文件 / Folder or File | 内容 / Contents | 复现用途 / Reproduction Use |
|---|---|---|
| [`README.md`](README.md) | 总体技术说明、视频、状态和导航 / Overall documentation, video, status and navigation | 裁判首页与总体复现 / Landing page and system reproduction |
| [`src源代码/`](src源代码/README.md) | Orange Pi视觉、UNO安全执行候选与历史实验 / Orange Pi vision, UNO safety-executor candidate and historical experiments | 编译、运行和算法审查 / Build, execution and algorithm review |
| [`schemes原理图/`](schemes原理图/wiring.md) | 引脚、串口、供电和接线 / Pins, serial, power and wiring | 电气复现 / Electrical reproduction |
| [`models模型/`](models模型/README.md) | 底盘、尺寸和层板DXF / Chassis, dimensions and plate DXF | 机械复现 / Mechanical reproduction |
| [`other其他/`](other其他/engineering-log.md) | 物料、测试、标定、风险和日志 / BOM, tests, calibration, risk and logs | 工程追溯 / Engineering traceability |
| [`t-photos团队照片/`](t-photos团队照片/README.md) | 团队、赛事和制作过程照片 / Team, competition and development photos | 团队与过程证据 / Team and process evidence |
| [`v-photos车辆照片/`](v-photos车辆照片/README.md) | 比赛照片和六视图规范 / Competition photo and six-view specification | 车辆与布线检查 / Vehicle and wiring inspection |
| [`video视频/`](video视频/video.md) | YouTube链接和本地视频参数 / YouTube link and local video specifications | 驾驶证明与版本追溯 / Driving evidence and version traceability |

### 详细工程文件 / Detailed Engineering Documents

- [物料表与选型依据 / Bill of materials and selection](other其他/BOM.md)
- [2026评分证据地图 / 2026 scoring-evidence map](other其他/scoring-evidence.md)
- [实测与照片证据登记 / Measurement and photograph evidence register](other其他/evidence-register.md)
- [源代码、运行方法与验证状态 / Source code, operation and validation](src源代码/README.md)
- [接线、串口与供电 / Wiring, serial communication and power](schemes原理图/wiring.md)
- [正式PNG接线图 / Formal PNG wiring diagram](schemes原理图/system-wiring.png)
- [机械模型、尺寸与DXF / Mechanical models, dimensions and DXF](models模型/README.md)
- [Orange Pi车载计算平台 / Orange Pi onboard computer](other其他/processor-orange-pi.md)
- [摄像头与视觉方案 / Camera and vision](other其他/camera-vision.md)
- [机械分析 / Mechanical analysis](other其他/mechanical-analysis.md)
- [软件架构 / Software architecture](other其他/software-architecture.md)
- [标定手册 / Calibration guide](other其他/calibration-guide.md)
- [风险分析 / Risk analysis](other其他/FMEA.md)
- [复现指南 / Reproduction guide](other其他/reproduction-guide.md)
- [工程日志Markdown / Engineering log in Markdown](other其他/engineering-log.md) · [可归档PDF / Archival PDF](other其他/engineering-log.pdf)
- [工程日志PDF生成脚本 / Engineering-log PDF build script](other其他/build_engineering_log_pdf.py)
- [团队介绍 / Team profile](other其他/team-profile.md)
- [比赛检查表 / Competition checklist](other其他/competition-checklist.md)
- [测试流程 / Test procedure](other其他/tests.md)
- [版本记录 / Changelog](other其他/CHANGELOG.md)

## 2. 系统概述 / System Overview

车辆采用汽车式阿克曼转向和四轮机械驱动。四根转向拉杆将舵机动作传到左右转向节；前后差速器和中间传动轴驱动车轮。底盘电机带有霍尔编码器接口，但当前车辆不接线、不读取，也不进行闭环速度控制。

The vehicle uses automotive-style Ackermann steering and mechanical four-wheel drive. Four steering links transfer servo motion to the left and right steering knuckles. Front and rear differentials and a longitudinal shaft drive the wheels. The motors provide Hall-encoder interfaces, but the current vehicle does not connect or read them and does not use closed-loop speed control.

底盘规格为 **260 × 140 × 85 mm**；去除防撞棉后主体长度约 **246 mm**。轴距 **174 mm**，轮距 **123 mm**，轮径 **47 mm**，离地间隙 **6 mm**，基础重量约 **0.7 kg**，标称负载 **0.3 kg**，最小转弯半径 **475 mm**。安装全部设备后必须重新实测。

The documented chassis size is **260 × 140 × 85 mm**, or approximately **246 mm** long without the foam bumpers. Wheelbase is **174 mm**, track width **123 mm**, wheel diameter **47 mm**, ground clearance **6 mm**, base mass approximately **0.7 kg**, rated additional load **0.3 kg**, and minimum turning radius **475 mm**. All values must be measured again after final assembly.

```mermaid
flowchart LR
  CAM["USB彩色摄像头 / USB colour camera"] --> OPI["Orange Pi Zero 3W 4GB"]
  OPI -->|"视觉决策 / Vision decisions"| PLAN["转向与速度目标 / Steering and speed targets"]
  PLAN -->|"有线串口 / Wired serial"| MCU["Arduino UNO"]
  MCU -->|"D2"| SERVO["转向舵机 / Steering servo"]
  MCU -->|"D6 PWM + D7 DIR"| DRIVER["电机驱动器 / Motor driver"]
  BUTTON["D8物理启动/停止 / Physical start-stop"] --> MCU
  DRIVER --> MOTOR["四轮驱动 / Four-wheel drive"]
  BAT["车载电源 / Vehicle battery"] --> REG["稳压与配电 / Regulation and distribution"]
  REG --> OPI
  REG --> MCU
  REG --> SERVO
  REG --> DRIVER
```

当前感知输入只有USB摄像头。视觉、串口或Orange Pi失效时，Arduino必须通过命令超时让电机停止。

The USB camera is the only perception input. If vision, serial communication or the Orange Pi fails, the Arduino must stop the motor through a command-timeout watchdog.

## 3. 移动性与机械设计 / Mobility and Mechanical Design

### 3.1 底盘方案 / Chassis Concept

选择阿克曼底盘是因为其运动方式接近真实汽车，直线稳定、转弯轨迹连续且轮胎侧滑较小。代价是转弯半径受轴距和最大转角限制，必须准确标定舵机中位、左右极限和转向连杆。

The Ackermann chassis was selected because its motion resembles a real car, with stable straight-line travel, continuous turning paths and reduced tyre scrub. The trade-off is a turning radius limited by wheelbase and maximum steering angle, so servo centre, left/right limits and steering links require careful calibration.

差速器允许转弯时内外侧车轮以不同速度滚动。最终文档仍需补充实车传动照片、齿数、电机标牌和完整装配尺寸。

The differentials allow inner and outer wheels to rotate at different speeds during a turn. Final documentation still requires drivetrain photographs, gear counts, motor labels and complete assembled dimensions.

### 3.2 转向保护 / Steering Protection

历史程序曾把逻辑转向量 `-100...100` 映射到约 `35...145°`。当前视觉执行候选为降低首次集成风险，暂用更保守的 `45...135°` 和中位 `90°`。两组都不是最终装车结论；必须架空实测左右机械安全极限并留出余量。更换舵机、舵臂孔位或拉杆长度后必须重新标定。

Historical sketches mapped logical steering `-100...100` to approximately `35...145°`. To reduce first-integration risk, the current vision-executor candidate temporarily uses a more conservative `45...135°` with `90°` centre. Neither range is a final assembled-vehicle result; measure both mechanical limits with the wheels lifted and retain margin. Recalibrate after changing the servo, horn position or link length.

### 3.3 速度、扭矩与几何 / Speed, Torque and Geometry

规格图给出47 mm轮径、1:8.864齿轮速比、1692 rpm车轮转速、12 V参考速度3.5 m/s、1.9 A额定电流、22.8 W额定功率和10 kg·cm舵机扭矩。

The catalogue lists a 47 mm wheel diameter, 1:8.864 gear ratio, 1692 rpm wheel speed, 3.5 m/s reference speed at 12 V, 1.9 A rated current, 22.8 W rated power and 10 kg·cm servo torque.

- 理论车速 / Theoretical speed：`v = π × D × n_motor / (60 × i)`
- 轮端扭矩 / Wheel torque：`T_wheel = T_motor × i × η`
- 牵引力 / Traction：`F = T_wheel / (D/2)`
- 阿克曼半径 / Ackermann radius：由轴距、轮距和内轮转角计算，并用地面画圆验证 / calculated from wheelbase, track and inner-wheel angle, then verified by a measured ground circle

1692 rpm按47 mm轮径换算约4.17 m/s，高于3.5 m/s参考值，可能分别是理论空载值和实际参考值，因此两者均保留并要求实测。

At a 47 mm wheel diameter, 1692 rpm converts to approximately 4.17 m/s, above the 3.5 m/s reference. These may represent theoretical no-load and practical reference values respectively, so both are retained and require measurement.

## 4. 动力与视觉架构 / Power and Vision Architecture

### 4.1 控制器与执行器 / Controllers and Actuators

Orange Pi负责摄像头、OpenCV图像处理、赛道判断和红绿障碍策略。Arduino只执行有线命令并控制舵机、电机驱动、启动状态和超时停车。舵机信号接D2，电机驱动接D6 PWM和D7 DIR。

The Orange Pi handles the camera, OpenCV image processing, track interpretation and red/green obstacle strategy. The Arduino only executes wired commands and controls the servo, motor driver, start state and timeout stop. The servo signal uses D2; the motor driver uses D6 PWM and D7 DIR.

舵机、电机和Orange Pi不得直接由UNO的5 V引脚供电。应使用电机动力支路、Orange Pi独立5 V/3 A稳压支路和控制器/舵机支路，并保持共地。

The servo, motor and Orange Pi must not be powered directly from the UNO 5 V pin. Use a motor-power branch, an independent regulated 5 V/3 A Orange Pi branch and a controller/servo branch, with a common ground.

### 4.2 视觉感知 / Vision Perception

车辆只安装一个USB彩色摄像头，不安装超声波，也不读取编码器。团队采购记录中的版本为 **160°广角有畸变、30 FPS彩色、非夜视、480p**，并记录GC0308、HBVCAM、CMOS、30万像素和USB免驱。彩色画面用于区分红绿障碍；广角畸变通过标定、ROI裁剪和现场光照测试处理。

The vehicle uses one USB colour camera, with no ultrasonic sensors and no encoder readings. The team purchase record identifies a **160° distorted wide angle, 30 FPS colour, non-night-vision and 480p** version and records GC0308, HBVCAM, CMOS, 0.3 megapixels and driver-free USB. Colour frames distinguish red and green obstacles; wide-angle distortion is handled through calibration, ROI cropping and on-site lighting tests.

安全措施包括上电默认停车、视觉帧超时、串口命令超时、程序退出发送停止、物理启动/停止控制和最坏停车距离测试。

Safety measures include stopped-by-default power-up, vision-frame timeout, serial-command timeout, stop-on-exit, physical start/stop control and worst-case stopping-distance tests.

### 4.3 动力预算 / Power Budget

总峰值电流应按下式估算，并用实车电流数据替换目录值：

Total peak current should be estimated with the following expression and updated using measured vehicle data:

`I_peak = I_motor_start + I_servo_stall + I_orange_pi_camera + I_controller + safety_margin`

测试应记录静止、视觉运行、直行、最大转向和电机启动时的电池电压与电流。复位、摄像头断连或掉帧时，应检查稳压余量、共地、电机噪声和线束压降。

Tests must record battery voltage and current while idle, running vision, travelling straight, steering fully and starting the motor. If a controller resets or the camera disconnects or drops frames, check regulator margin, common ground, motor noise and wiring voltage drop.

## 5. 软件架构与控制策略 / Software Architecture and Control Strategy

### 5.1 当前程序 / Current Programs

| 层级 / Layer | 程序 / Program | 内容 / Function | 状态 / Status |
|---|---|---|---|
| 历史巡墙基线 / Historical wall-follow baseline | [`main1.0.ino`](src源代码/main1.0/main1.0.ino) | 双超声波P控制 / Dual-ultrasonic P control | 当前不使用 / Not currently used |
| 团队早期实验 / Earlier team experiments | [`UNO_AT8236`](src源代码/UNO_AT8236_OpenChallenge/UNO_AT8236_OpenChallenge.ino), [`UNO_DRV8701`](src源代码/UNO_DRV8701_OpenChallenge/UNO_DRV8701_OpenChallenge.ino) | 编码器PI和双超声波 / Encoder PI and dual ultrasonic | 团队自主开发，当前不使用 / Team-developed; not currently used |
| ESP32试验 / ESP32 experiment | [`ESP32_AT8236`](src源代码/ESP32_AT8236_OpenChallenge/ESP32_AT8236_OpenChallenge.ino) | AT8236控制和关闭无线 / AT8236 control and wireless shutdown | 仅参考 / Reference only |
| 道路工具 / Road tool | [`bev_road.py`](src源代码/bev_road.py) | 亮度、BEV、道路掩膜和连通域 / Brightness, BEV, road mask and components | 需实车标定 / Vehicle calibration required |
| 视觉原型 / Vision prototype | [`bev_segmentation.py`](src源代码/bev_segmentation.py) | 红绿识别、方向策略、串口和恢复 / Red-green detection, direction strategy, serial and recovery | 当前主要方向 / Current main approach |
| UNO安全执行候选 / UNO safety-executor candidate | [`VisionSerialExecutor.ino`](src源代码/VisionSerialExecutor/VisionSerialExecutor.ino) | D8启动/停止、命令校验、D2/D6/D7输出、250 ms超时 / D8 start-stop, validation, D2/D6/D7 output and 250 ms timeout | 代码闭环；待实机验证 / Code chain complete; hardware validation pending |

两份Python文件已通过语法解析。视觉程序默认速度为0，减速阈值低于避障阈值，制动阶段先停车，并在视频源丢失或程序退出时发送停止命令。UNO候选执行程序已与 `steer,speed` 文本协议闭环，并增加物理启动、畸形行过滤、执行限幅和250 ms本地看门狗。该程序已使用Arduino AVR Boards `1.8.8`与Servo `1.3.0`完成UNO目标编译，占用5544 bytes程序空间和277 bytes全局变量；仍需上传实物、核实驱动器电气兼容性并完成整车集成验证。

Both Python files pass syntax parsing. The vision controller defaults to zero speed, keeps the slow-down threshold below the avoidance threshold, stops before braking actions and sends a stop command when the video source is lost or the program exits. The candidate UNO executor closes the `steer,speed` text path and adds physical start, malformed-line rejection, output limits and a 250 ms local watchdog. It builds for the UNO target with Arduino AVR Boards `1.8.8` and Servo `1.3.0`, using 5,544 bytes of program storage and 277 bytes of global-variable memory. Physical upload, driver electrical compatibility and full-vehicle integration tests are still required.

历史Arduino程序中的 `getDistance()`、`move()`、`steer()`、`setup()` 和 `loop()` 仅用于解释早期硬件验证，不代表当前传感器配置。

The `getDistance()`, `move()`, `steer()`, `setup()` and `loop()` functions in historical Arduino programs document early hardware validation only and do not represent the current sensor configuration.

### 5.2 历史巡墙控制 / Historical Wall-Following Control

早期程序使用目标右距30 cm、`KP=2.5`和速度70的P控制。该方案计算量小，但不能识别颜色，也缺少积分和微分作用。它仅作为研发历史保留。

The early program used a 30 cm target right-wall distance, `KP=2.5` and speed 70. It was computationally simple but could not identify colours and had no integral or derivative action. It is retained only as development history.

### 5.3 当前边界与升级 / Current Boundaries and Upgrades

视觉串口当前使用简单的 `steer,speed` 文本行，尚无序号、源时间戳、CRC和确认应答。物理启动和250 ms命令失效停车已在UNO候选程序中实现。透视、HSV、道路密度、红绿通过侧、倒车时间和速度仍需标定；停车区、圈数、方向初始化、无桌面自动启动/恢复和多光照长时间测试仍需完成。

The current visual serial protocol uses a simple `steer,speed` text line without sequence numbers, source timestamps, CRC or acknowledgement. Physical start and a 250 ms command-failure stop are implemented in the candidate UNO sketch. Perspective, HSV, road density, red/green passing side, reversing time and speed still require calibration; parking, lap counting, direction initialisation, headless startup/recovery and long-duration multi-lighting tests remain incomplete.

## 6. 系统思维与工程决策 / System Thinking and Engineering Decisions

1. **阿克曼转向 / Ackermann steering：** 更接近汽车并提高直线稳定性，但需要更精确的机械标定。 / More automotive and stable in straight travel, but requires more precise mechanical calibration.
2. **历史超声波基线 / Historical ultrasonic baseline：** 曾用于验证底盘、舵机和电机方向；当前只保留代码，不作为比赛传感器或安全备份。 / Previously validated chassis, servo and motor direction; retained only as code history, not as a competition sensor or safety backup.
3. **视觉失效停车 / Stop on vision failure：** 无独立距离传感器时，视觉帧、串口或处理器超时必须立即将电机目标置零。 / Without an independent range sensor, a vision-frame, serial or processor timeout must immediately set the motor target to zero.

## 7. 搭建、编译与上传 / Assembly, Build and Upload

1. 按[机械文档](models模型/README.md)固定底盘、Orange Pi、Arduino、电源、摄像头和支架。 / Mount the chassis, Orange Pi, Arduino, power system, camera and brackets according to the [mechanical documentation](models模型/README.md).
2. 按[接线文档](schemes原理图/wiring.md)连接舵机、驱动器、摄像头和串口；不要连接历史超声波或编码器。 / Follow the [wiring guide](schemes原理图/wiring.md) for the servo, driver, camera and serial link; do not connect historical ultrasonic or encoder interfaces.
3. 抬轮上电并确认舵机中位、转向方向、电机方向和物理启动。 / Power on with the wheels lifted and verify servo centre, steering direction, motor direction and physical start control.
4. 编译 [`VisionSerialExecutor.ino`](src源代码/VisionSerialExecutor/VisionSerialExecutor.ino)，核对PWM/DIR接口并确保115200 baud与Orange Pi一致。 / Build [`VisionSerialExecutor.ino`](src源代码/VisionSerialExecutor/VisionSerialExecutor.ino), verify the PWM/DIR interface and match 115200 baud to the Orange Pi.
5. 在Orange Pi安装并冻结Python/OpenCV/PySerial依赖，填写真实串口配置。 / Install and freeze Python/OpenCV/PySerial dependencies on the Orange Pi and enter the actual serial configuration.
6. 先用录像测试视觉，再接摄像头，确认默认速度为0、方向和红绿策略正确。 / Test vision with recordings before connecting the camera; confirm zero default speed, correct direction and correct red/green strategy.
7. 从低速开始测试直行、弯道、障碍、摄像头断开、串口断开、重启和30分钟稳定性。 / Starting at low speed, test straight travel, turns, obstacles, camera loss, serial loss, restart and 30-minute stability.
8. 在[测试记录](other其他/tests.md)中保存日期、提交号、参数和结果。 / Record date, commit, parameters and results in the [test records](other其他/tests.md).

## 8. 测试、风险与版本管理 / Testing, Risk and Version Management

主要风险包括舵机顶死、电机启动压降、视觉误判或掉帧、摄像头/串口断开、转向符号错误、线束松脱、轮胎打滑、上电即行驶和无线通信未关闭。每次上场前应完成静态、抬轮、低速和完整回合测试。

Main risks include servo mechanical stall, motor-start voltage drop, visual misclassification or dropped frames, camera/serial disconnection, reversed steering sign, loose wiring, tyre slip, movement immediately after power-up and wireless communication left enabled. Complete static, lifted-wheel, low-speed and full-lap tests before every run.

后续提交说明应可追溯，例如 `docs: add measured power budget`、`vision: tune obstacle HSV from field data` 和 `hardware: add final wiring diagram`。公开仓库应按规则保持可访问。

Future commit messages should be traceable, for example `docs: add measured power budget`, `vision: tune obstacle HSV from field data` and `hardware: add final wiring diagram`. The public repository must remain accessible as required by the rules.

## 9. 提交前缺口清单 / Pre-Submission Gap Checklist

- [x] 公开YouTube驾驶演示 / Public YouTube driving demonstration.
- [x] Arduino/ESP32参考程序、Orange Pi视觉原型和源码说明 / Arduino/ESP32 references, Orange Pi vision prototype and source documentation.
- [x] DXF、BOM、接线、风险、标定、测试和复现资料 / DXF, BOM, wiring, risk, calibration, test and reproduction materials.
- [x] 2026五维评分地图、缺失证据登记和结构化双语工程日志PDF / 2026 five-dimension map, missing-evidence register and structured bilingual engineering-log PDF.
- [x] 视觉串口UNO安全执行候选与PNG/SVG接线图 / Vision-serial UNO safety-executor candidate and PNG/SVG wiring diagram.
- [x] 正式团队照、冠军照和比赛现场车辆照 / Official team, championship and competition-field vehicle photographs.
- [ ] 补充车辆前、后、左、右、顶、底六视图 / Add front, rear, left, right, top and bottom vehicle views.
- [ ] 补充全员趣味照和黄鸣博个人照 / Add an informal full-team photograph and Huang Mingbo's portrait.
- [ ] 在视频文档填写拍摄日期、提交号和硬件参数 / Add recording date, commit and hardware parameters to the video document.
- [ ] 补充最终CAD/STL、传动参数和摄像头安装尺寸 / Add final CAD/STL, drivetrain data and camera mounting dimensions.
- [ ] 以实物核验PNG电路图中的准确器件型号、额定值、逻辑电平、保险和引脚 / Physically verify exact models, ratings, logic levels, fuse and pins in the PNG diagram.
- [ ] 完成尺寸、质量、速度、电流、转弯半径和完整回合实测 / Measure dimensions, mass, speed, current, turning radius and full-lap time.
- [ ] 验证物理启动、视觉/通信超时停车并关闭无线 / Verify physical start, vision/communication timeout stop and disabled wireless functions.
- [ ] 完成透视、红绿识别、圈数、停车区和停车策略 / Complete perspective, red-green detection, lap counting, parking zone and stopping strategy.

## 10. 完整文件索引 / Complete File Index

### 程序与配置 / Programs and Configuration

| 文件 / File | 内容 / Contents |
|---|---|
| [`src源代码/README.md`](src源代码/README.md) | 运行、依赖、安全和验证状态 / Operation, dependencies, safety and validation status |
| [`main1.0.ino`](src源代码/main1.0/main1.0.ino) | 历史超声波巡墙 / Historical ultrasonic wall following |
| [`UNO_AT8236`](src源代码/UNO_AT8236_OpenChallenge/UNO_AT8236_OpenChallenge.ino) | UNO + AT8236历史参考 / Historical reference |
| [`UNO_DRV8701`](src源代码/UNO_DRV8701_OpenChallenge/UNO_DRV8701_OpenChallenge.ino) | UNO + DRV8701历史参考 / Historical reference |
| [`ESP32_AT8236`](src源代码/ESP32_AT8236_OpenChallenge/ESP32_AT8236_OpenChallenge.ino) | ESP32试验参考 / ESP32 experimental reference |
| [`bev_road.py`](src源代码/bev_road.py) | 道路掩膜和BEV调试 / Road mask and BEV debugging |
| [`bev_segmentation.py`](src源代码/bev_segmentation.py) | 红绿视觉、方向策略、串口和恢复 / Red-green vision, direction strategy, serial and recovery |
| [`VisionSerialExecutor.ino`](src源代码/VisionSerialExecutor/VisionSerialExecutor.ino) | 视觉串口、物理启动、限幅和250 ms失效停车 / Vision serial, physical start, limits and 250 ms fail-safe |
| [`requirements.txt`](src源代码/requirements.txt) | Python依赖 / Python dependencies |
| [`serial_config.example.json`](src源代码/serial_config.example.json) | 串口配置示例 / Serial configuration example |

### 机械、电气与工程文档 / Mechanical, Electrical and Engineering Documents

| 文件 / File | 内容 / Contents |
|---|---|
| [`models模型/README.md`](models模型/README.md) | 底盘、尺寸和模型 / Chassis, dimensions and models |
| [`HSP94182层板.dxf`](models模型/HSP94182层板.dxf) | 二维层板文件 / 2D plate file |
| [`wiring.md`](schemes原理图/wiring.md) | 引脚、串口、供电和接线 / Pins, serial, power and wiring |
| [`system-wiring.png`](schemes原理图/system-wiring.png) / [`SVG`](schemes原理图/system-wiring.svg) | 双语系统接线图与可编辑矢量源 / Bilingual system wiring and editable vector source |
| [`BOM.md`](other其他/BOM.md) | 物料与选型 / Materials and selection |
| [`processor-orange-pi.md`](other其他/processor-orange-pi.md) | Orange Pi规格、职责和验收 / Orange Pi specifications, role and acceptance |
| [`camera-vision.md`](other其他/camera-vision.md) | 摄像头、安装、标定和指标 / Camera, mounting, calibration and metrics |
| [`mechanical-analysis.md`](other其他/mechanical-analysis.md) | 几何、速度和机械分析 / Geometry, speed and mechanical analysis |
| [`software-architecture.md`](other其他/software-architecture.md) | 架构、状态机和数据流 / Architecture, state machine and data flow |
| [`calibration-guide.md`](other其他/calibration-guide.md) | 舵机、摄像头、速度和转向标定 / Servo, camera, speed and steering calibration |
| [`FMEA.md`](other其他/FMEA.md) | 风险与改进 / Risks and improvements |
| [`reproduction-guide.md`](other其他/reproduction-guide.md) | 完整复现流程 / Complete reproduction process |
| [`team-profile.md`](other其他/team-profile.md) | 学校、成员、照片和职责 / School, members, portraits and roles |
| [`engineering-log.md`](other其他/engineering-log.md) | 研发阶段和实验计划 / Development stages and experiment plan |
| [`engineering-log.pdf`](other其他/engineering-log.pdf) | 规则要求的结构化可归档双语工程日志 / Structured archival bilingual engineering log required by the rules |
| [`scoring-evidence.md`](other其他/scoring-evidence.md) | 五维评分要求到证据的映射 / Mapping from the five rubric dimensions to evidence |
| [`evidence-register.md`](other其他/evidence-register.md) | 实测、照片和提交缺口登记 / Measurement, photograph and submission gap register |
| [`commit-plan.md`](other其他/commit-plan.md) | 有意义提交的建议拆分 / Recommended grouping for meaningful commits |
| [`competition-checklist.md`](other其他/competition-checklist.md) | 文件、机械、电气和软件检查 / File, mechanical, electrical and software checks |
| [`tests.md`](other其他/tests.md) | 静态、动力、视觉和故障测试 / Static, power, vision and fault tests |
| [`CHANGELOG.md`](other其他/CHANGELOG.md) | 版本迭代 / Version history |

### 照片与视频 / Photographs and Video

- [YouTube自动驾驶演示 / YouTube autonomous-driving demonstration](https://youtu.be/DJcxiJCEFdo) · [视频资料 / Video documentation](video视频/video.md)
- [学校队旗 / School flag](t-photos团队照片/team-flag.jpg) · [正式团队照 / Official team photo](t-photos团队照片/team-official.jpg) · [冠军照 / Award photo](t-photos团队照片/award-beijing-champion.jpg) · [比赛车辆 / Competition vehicle](v-photos车辆照片/vehicle-competition-run.jpg)
- [制作过程照片 / Development-process photographs](t-photos团队照片/README.md) · [车辆照片要求 / Vehicle photograph requirements](v-photos车辆照片/README.md)

## 信息来源 / Sources

- WRO官方Future Engineers模板 / WRO official Future Engineers template：<https://github.com/world-robot-olympiad-association/wro2022-fe-template>
- 团队底盘资料 / Team chassis reference：<https://pjfcckenlt.feishu.cn/wiki/WlCXwfJRCixkGPkZvTIcfUI6nHg>
- 团队提供的2026比赛规则和技术文档评分要求 / 2026 competition rules and technical-document rubric supplied by the team.
