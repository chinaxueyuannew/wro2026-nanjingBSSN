# 工程研发日志 / Engineering Log

本日志只记录已有成果和明确计划，不为未知日期虚构事件。 / This log records existing results and explicit plans only; unknown dates are never invented.

## 阶段1：建立仓库 / Stage 1: Repository Setup

采用官方模板建立照片、视频、原理图、代码、模型和技术材料目录，并重写首页导航与缺口清单。 / Adopted the official template for photos, video, schematics, code, models and technical materials, then rebuilt landing-page navigation and the gap list.

## 阶段2：历史巡墙基线 / Stage 2: Historical Wall-Following Baseline

早期Arduino使用前/右超声波、舵机和PWM/DIR，实现30 cm右墙P控制。它缺少启动状态、速度闭环、转弯和异常停车，当前不使用。 / The early Arduino used front/right ultrasonic sensors, servo and PWM/DIR for 30 cm right-wall P control. It lacked start state, speed loop, turning and fault stop and is not currently used.

## 阶段3–4：底盘资料与参考程序 / Stages 3–4: Chassis Data and Reference Programs

确认阿克曼四驱结构及AT8236、DRV8701和ESP32示例，提取尺寸和编码器参考，并按驱动器分开代码。新增PI/PD、状态机和安全结构的参考程序，但当前只作历史资料。 / Confirmed the four-wheel-drive Ackermann structure and AT8236, DRV8701 and ESP32 examples, extracted dimensional/encoder references and separated code by driver. Added reference PI/PD, state-machine and safety structures, retained only as history.

## 阶段5：Orange Pi视觉平台 / Stage 5: Orange Pi Vision Platform

确认Orange Pi Zero 3W 4GB/A733。当时建立“Orange Pi视觉决策+Arduino执行安全”试验架构，记录USB摄像头、有线串口、独立5 V/3 A、散热和无线关闭。该双控制器方案后来被阶段13的Orange Pi GPIO/PWM直控方案替代。传统CPU/OpenCV仍为基线，NPU尚未验证。 / Confirmed Orange Pi Zero 3W 4GB/A733. At that stage, the team established an experimental “Orange Pi vision decisions + Arduino execution safety” architecture and documented USB camera, wired serial, independent 5 V/3 A, cooling and wireless shutdown. Stage 13 later replaced that two-controller design with direct Orange Pi GPIO/PWM control. CPU/OpenCV remains the baseline; NPU is unverified.

## 阶段6：视觉原型 / Stage 6: Vision Prototype

加入 `bev_road.py` 和 `bev_segmentation.py`，完成语法检查及默认停车、阈值、制动和退出停车修正。当时原型仍包含串口输出；现行阶段13已改为同进程GPIO/PWM输出。透视、HSV和实车验证仍待完成。 / Added both Python programs, completed syntax checks and corrected default stop, thresholds, braking and exit stop. The prototype still contained serial output at that stage; current Stage 13 replaces it with in-process GPIO/PWM output. Perspective, HSV and vehicle validation remain pending.

## 阶段7–8：照片与赛事证据 / Stages 7–8: Photos and Competition Evidence

整理11张制作过程照片，并加入三名成员照、正式团队照、北京站冠军照和比赛车辆照片。趣味团队照和车辆六视图待补。 / Indexed 11 process photos and added all three member portraits, the official team photograph, Beijing championship photograph and competition-vehicle photograph. The informal team photograph and six vehicle views are pending.

## 阶段9：视觉唯一感知 / Stage 9: Vision-Only Perception

确认只使用USB摄像头进行环境感知，不安装超声波、不读取编码器。当时版本仍由Arduino执行视觉目标；现行阶段13已取消Arduino。 / Confirmed the USB camera as the only environmental sensor, with no ultrasonic sensors or encoder readings. At that stage the Arduino still executed vision targets; current Stage 13 removes the Arduino.

## 阶段10：团队资料 / Stage 10: Team Profile

加入队旗、双语校名、三名队员、教练、职责和成员照片，并从首页直接链接。 / Added flag, bilingual school name, three members, coach, roles and portraits, linked from the landing page.

## 阶段11：上一版规则复核与串口安全闭环 / Stage 11: Previous-Version Rule Audit and Serial Safety Closure

上一版方案依据2026规则附录C和技术文档评分表重新核对五个评分维度，建立评分证据地图、实测/照片登记表和提交拆分建议。审计发现当时视觉程序已发送 `steer,speed`，但仓库没有匹配的UNO执行端，而且旧程序引脚与候选接线不一致。为消除当时的复现断点，新增PWM/DIR串口执行候选：D2舵机、D6 PWM、D7 DIR、D8物理按钮，上电默认停车，畸形命令不刷新看门狗，250 ms无合法命令进入故障，恢复必须重新按键并收到新命令。该候选已被阶段13的Orange Pi GPIO/PWM直控替代，现仅作版本演进证据。

The previous-version design was re-audited against 2026 Appendix C and the engineering-documentation score sheet, producing a scoring-evidence map, a measurement/photograph register and a commit-grouping recommendation. The audit found that the vision program transmitted `steer,speed` but lacked a matching UNO executor, while historical sketch pins contradicted candidate wiring. A D2/D6/D7/D8 PWM/DIR serial executor was added to close that reproduction break. Stage 13 superseded it with direct Orange Pi GPIO/PWM control, so it now serves only as version-evolution evidence.

## 阶段12：上一版UNO目标编译验证 / Stage 12: Previous-Version UNO-Target Build Verification

使用Arduino AVR Boards `1.8.8`和标准Servo库 `1.3.0`编译上一版 `VisionSerialExecutor.ino`，UNO目标编译通过，占用5544 bytes程序空间（17%）和277 bytes全局变量（13%）。这只消除了该历史版本的语法、目标平台和依赖风险；当时计划的实物烧录与U系列测试已由阶段13的G-01至G-10取代。

The previous-version `VisionSerialExecutor.ino` was compiled using Arduino AVR Boards `1.8.8` and the standard Servo library `1.3.0`. The UNO-target build passed, using 5,544 bytes of program storage (17%) and 277 bytes of global-variable memory (13%). This closes only that historical version's syntax, target-platform and dependency risks; Stage 13 replaces its planned upload and U-series tests with G-01 through G-10.

该结果只证明上一版程序可以编译。由于当前车辆不安装Arduino，上一版的烧录和U系列测试不再属于现行验收计划。 / This result proves only that the previous-version program builds. Because the current vehicle has no Arduino, previous-version upload and U-series tests are no longer part of current acceptance.

## 阶段13：Orange Pi GPIO/PWM直控 / Stage 13: Direct Orange Pi GPIO/PWM Control

根据最终装车方案，控制链改为“USB摄像头 → Orange Pi视觉与决策 → 同板GPIO/PWM → 舵机和电机驱动器”，并明确当前不安装Arduino、不使用板间串口。新增 `orange_pi_gpio.py` 与默认禁用的 `gpio_config.example.json`，将物理按钮、电机方向、电机PWM、舵机PWM、输出限幅、方向变化前归零、250 ms控制更新看门狗和退出清理集中在一个模块。`bev_segmentation.py`改为直接调用该模块，Python核心文件已通过语法检查。

The final vehicle architecture changes the chain to “USB camera → Orange Pi vision and decisions → same-board GPIO/PWM → steering servo and motor driver”, explicitly with no Arduino or inter-board serial link. `orange_pi_gpio.py` and a disabled-by-default `gpio_config.example.json` were added, centralising the physical button, motor direction, motor PWM, steering PWM, output limits, zero-before-direction-change, 250 ms control-update watchdog and exit cleanup. `bev_segmentation.py` now calls this module directly, and the core Python files pass syntax checks.

为避免虚构，真实GPIO line与PWM chip/channel保持 `-1`，必须依据冻结比赛镜像、设备树、实物排针和枚举结果确认。新接线图、BOM、软件架构、测试G-01至G-10、复现指南、FMEA和评分证据同步到单板直控。文档同时明确残余风险：进程看门狗不能保证Linux内核或PWM整体冻结时停车，必须故障注入并评估独立硬件使能保护。

To avoid invented data, real GPIO lines and PWM chip/channels remain `-1` until confirmed from the frozen competition image, device tree, physical header and enumeration. The wiring diagram, BOM, software architecture, G-01 through G-10 tests, reproduction guide, FMEA and scoring map are synchronised to single-board direct control. The documentation also records the residual risk: a process watchdog cannot guarantee stopping during a complete Linux-kernel or PWM freeze, so fault injection and an independent hardware enable must be assessed.

## 下一轮实验 / Next Experiments

| 优先级 / Priority | 实验 / Experiment | 目标与证据 / Goal and Evidence |
|---:|---|---|
| 1 | GPIO/PWM资源冻结 / GPIO/PWM resource freeze | 排针、gpiochip/line、PWM chip/channel、overlay、照片和签字 / Header, line/channel, overlay, photographs and sign-off |
| 2 | 舵机极限 / Servo limits | 无顶死，角度+视频 / No stall, angles+video |
| 3 | 摄像头标定 / Camera calibration | 内参、畸变、ROI、安装角 / Intrinsics, distortion, ROI, angle |
| 4 | 电源负载 / Power load | 无复位，电压电流 / No reset, voltage/current |
| 5 | 速度映射 / Speed mapping | 多电量可预测 / Predictable across battery levels |
| 6 | 视觉转向 / Vision steering | 连续10回合无碰撞 / Ten collision-free laps |
| 7 | CW/CCW弯道 / CW/CCW turns | 四角稳定 / Stable at four corners |
| 8 | 系统验收 / System acceptance | 内存、摄像头、GPIO/PWM枚举和G-01至G-10 / Memory, camera, GPIO/PWM enumeration and G-01 through G-10 |
| 9 | 延迟温度 / Latency and temperature | 30分钟日志 / 30-minute log |
| 10 | 故障安全 / Fault safety | 遮挡、摄像头断开、进程停止及Linux/PWM冻结边界 / Obstruction, camera loss, process stop and Linux/PWM freeze boundary |

## 单次日志模板 / Single-Test Template

- 日期与实验 / Date and experiment:
- 参与人员 / Participants:
- Git提交 / Commit:
- 硬件与电池 / Hardware and battery:
- 场地与光照 / Field and lighting:
- 目标与参数 / Goal and parameters:
- 过程与数据 / Procedure and data:
- 结果：成功/部分成功/失败 / Result: success/partial/failure:
- 问题与下一步 / Issues and next step:
