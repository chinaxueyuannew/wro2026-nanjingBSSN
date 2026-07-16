# 工程研发日志 / Engineering Log

本日志只记录已有成果和明确计划，不为未知日期虚构事件。 / This log records existing results and explicit plans only; unknown dates are never invented.

## 阶段1：建立仓库 / Stage 1: Repository Setup

采用官方模板建立照片、视频、原理图、代码、模型和技术材料目录，并重写首页导航与缺口清单。 / Adopted the official template for photos, video, schematics, code, models and technical materials, then rebuilt landing-page navigation and the gap list.

## 阶段2：历史巡墙基线 / Stage 2: Historical Wall-Following Baseline

早期Arduino使用前/右超声波、舵机和PWM/DIR，实现30 cm右墙P控制。它缺少启动状态、速度闭环、转弯和异常停车，当前不使用。 / The early Arduino used front/right ultrasonic sensors, servo and PWM/DIR for 30 cm right-wall P control. It lacked start state, speed loop, turning and fault stop and is not currently used.

## 阶段3–4：底盘资料与参考程序 / Stages 3–4: Chassis Data and Reference Programs

确认RF-A101HE阿克曼结构及AT8236、DRV8701和ESP32示例，提取尺寸和编码器参考，并按驱动器分开代码。新增PI/PD、状态机和安全结构的参考程序，但当前只作历史资料。 / Confirmed RF-A101HE Ackermann structure and AT8236, DRV8701 and ESP32 examples, extracted dimensional/encoder references and separated code by driver. Added reference PI/PD, state-machine and safety structures, retained only as history.

## 阶段5：Orange Pi视觉平台 / Stage 5: Orange Pi Vision Platform

确认Orange Pi Zero 3W 4GB/A733，建立“Orange Pi视觉决策+Arduino执行安全”架构，记录USB摄像头、有线串口、独立5 V/3 A、散热和无线关闭。传统CPU/OpenCV为基线，NPU尚未验证。 / Confirmed Orange Pi Zero 3W 4GB/A733 and established “Orange Pi vision decisions + Arduino execution safety”, documenting USB camera, wired serial, independent 5 V/3 A, cooling and wireless shutdown. CPU/OpenCV is the baseline; NPU is unverified.

## 阶段6：视觉原型 / Stage 6: Vision Prototype

加入 `bev_road.py` 和 `bev_segmentation.py`，完成语法检查及默认停车、阈值、制动和退出停车修正。串口可靠性、透视、HSV和实车验证仍待完成。 / Added both Python programs, completed syntax checks and corrected default stop, thresholds, braking and exit stop. Reliable serial, perspective, HSV and vehicle validation remain pending.

## 阶段7–8：照片与赛事证据 / Stages 7–8: Photos and Competition Evidence

整理11张制作过程照片，并加入三名成员照、正式团队照、北京站冠军照和比赛车辆照片。趣味团队照和车辆六视图待补。 / Indexed 11 process photos and added all three member portraits, the official team photograph, Beijing championship photograph and competition-vehicle photograph. The informal team photograph and six vehicle views are pending.

## 阶段9：视觉唯一感知 / Stage 9: Vision-Only Perception

确认当前只使用USB摄像头和Orange Pi；不安装超声波、不读取编码器。Arduino只执行视觉目标并负责启动、限幅和超时停车。 / Confirmed USB camera and Orange Pi as the only perception chain; no ultrasonic sensors or encoder readings. Arduino only executes vision targets and handles start, limits and timeout stop.

## 阶段10：团队资料 / Stage 10: Team Profile

加入队旗、双语校名、三名队员、教练、职责和成员照片，并从首页直接链接。 / Added flag, bilingual school name, three members, coach, roles and portraits, linked from the landing page.

## 阶段11：规则复核与安全闭环 / Stage 11: Rule Audit and Safety Closure

依据2026规则附录C和技术文档评分表重新核对五个评分维度，建立评分证据地图、实测/照片登记表和提交拆分建议。发现视觉程序已发送 `steer,speed`，但仓库没有与之匹配的当前UNO执行端，而且旧程序引脚与首页候选接线不一致。为消除该复现断点，新增PWM/DIR视觉执行候选：D2舵机、D6 PWM、D7 DIR、D8物理按钮，上电默认停车，畸形命令不刷新看门狗，250 ms无合法命令进入故障，恢复必须重新按键并收到新命令。正式PNG/SVG接线图与代码使用同一候选引脚。驱动器接口和全部限位仍须实物验证，不能仅凭文档确认。

The five rubric dimensions were re-audited against 2026 Appendix C and the engineering-documentation score sheet, producing a scoring-evidence map, a measurement/photograph register and a commit-grouping recommendation. The audit found that the vision program already transmitted `steer,speed`, but the repository had no current UNO executor matching that protocol, while historical sketch pins contradicted the landing-page candidate wiring. To close this reproduction break, a PWM/DIR vision-executor candidate was added: D2 servo, D6 PWM, D7 DIR and D8 physical button; stopped by default at power-up; malformed lines do not refresh the watchdog; more than 250 ms without a valid command enters fail-safe; recovery requires re-arm and a fresh command. The formal PNG/SVG wiring diagram uses the same candidate pins. The physical driver interface and every actuator limit still require hardware verification and cannot be confirmed by documentation alone.

## 阶段12：UNO目标编译验证 / Stage 12: UNO-Target Build Verification

使用Arduino AVR Boards `1.8.8`和标准Servo库 `1.3.0`编译 `VisionSerialExecutor.ino`，UNO目标编译通过，占用5544 bytes程序空间（17%）和277 bytes全局变量（13%）。这消除了语法、目标平台和依赖层面的复现风险；烧录实物UNO、U-01至U-10串口测试、驱动器电气兼容性和整车动作仍必须现场验证。

`VisionSerialExecutor.ino` was compiled using Arduino AVR Boards `1.8.8` and the standard Servo library `1.3.0`. The UNO-target build passed, using 5,544 bytes of program storage (17%) and 277 bytes of global-variable memory (13%). This closes syntax, target-platform and dependency reproducibility risks; physical UNO upload, serial tests U-01 through U-10, driver electrical compatibility and vehicle motion still require onsite verification.

## 下一轮实验 / Next Experiments

| 优先级 / Priority | 实验 / Experiment | 目标与证据 / Goal and Evidence |
|---:|---|---|
| 1 | 驱动器与引脚 / Driver and pins | 唯一比赛版本，照片+接线 / One competition version, photo+wiring |
| 2 | 舵机极限 / Servo limits | 无顶死，角度+视频 / No stall, angles+video |
| 3 | 摄像头标定 / Camera calibration | 内参、畸变、ROI、安装角 / Intrinsics, distortion, ROI, angle |
| 4 | 电源负载 / Power load | 无复位，电压电流 / No reset, voltage/current |
| 5 | 速度映射 / Speed mapping | 多电量可预测 / Predictable across battery levels |
| 6 | 视觉转向 / Vision steering | 连续10回合无碰撞 / Ten collision-free laps |
| 7 | CW/CCW弯道 / CW/CCW turns | 四角稳定 / Stable at four corners |
| 8 | 系统验收 / System acceptance | 内存、摄像头、串口枚举 / Memory, camera, serial enumeration |
| 9 | 延迟温度 / Latency and temperature | 30分钟日志 / 30-minute log |
| 10 | 故障安全 / Fault safety | 遮挡/冻结/断连后停车 / Stop after obstruction/freeze/disconnection |

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
