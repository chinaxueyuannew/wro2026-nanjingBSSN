# 2026技术文档评分证据地图 / 2026 Engineering-Documentation Evidence Map

> 审核日期：2026-07-16。本文件依据《2026未来工程师无人驾驶赛季规则》附录C和《2026未来工程师—技术文档评审标准》整理。它是裁判快速入口，不替代各技术文件。所有“待实测”内容均不得以推测值替代。  
> Audit date: 2026-07-16. This map follows Appendix C of the 2026 Future Engineers Autonomous Driving rules and the 2026 engineering-documentation rubric. It is a judge-facing index, not a replacement for the technical files. Any item marked “measurement pending” must not be replaced by an assumed value.

## 1. 评分逻辑 / Scoring Logic

技术文档共五个维度，每项为0、2、4或6分，满分30分。6分要求的不只是“有文件”，还要求选型理由、约束、方案取舍、测试、迭代和可复现证据形成闭环。规则还要求结构化工程日志采用PDF或类似可归档格式，并要求GitHub至少包含代码、CAD、接线说明和相关技术材料。

The documentation has five dimensions, each scored 0, 2, 4 or 6, for a maximum of 30. A 6-point result requires more than file presence: selection rationale, constraints, trade-offs, tests, iteration and reproducible evidence must form a closed engineering chain. The rules also require a structured engineering log in PDF or another archival format and a GitHub repository containing code, CAD, wiring information and relevant technical material.

本仓库按“规则要求 → 设计主张 → 证据文件 → 验证状态 → 下一项证据”组织。下表中的“6分目标”表示提交前必须完成的证据包，不是对裁判结果的预判。

This repository is organised as “rule requirement → design claim → evidence file → validation state → next evidence”. A “6-point target” means the evidence package required before submission; it is not a prediction of the judges’ score.

## 2. 五维总览 / Five-Dimension Overview

| 维度 / Dimension | 已有核心证据 / Existing Core Evidence | 当前证据强度 / Current Evidence Strength | 达到6分仍需 / Still Required for a 6-Point Claim |
|---|---|---|---|
| 1. 移动性能与机械设计 / Mobility and mechanical design | [首页机械章节](../README.md#3-移动性与机械设计--mobility-and-mechanical-design)、[机械分析](mechanical-analysis.md)、[模型与DXF](../models模型/README.md)、[测试表](tests.md#4-机械与动力--mechanical-and-power) | 已说明阿克曼、四驱、差速、几何和理论速度；有层板DXF / Ackermann, four-wheel drive, differentials, geometry, theoretical speed and a plate DXF are documented | 最终装车尺寸/质量、舵角、左右转弯半径、速度/扭矩实测、支架图纸、测试前后机械迭代照片 / Final dimensions, mass, steering angles, left/right radius, speed/torque measurements, mount drawings and before/after iteration evidence |
| 2. 动力与传感器架构 / Power and sensor architecture | [接线图](../schemes原理图/wiring.md)、[正式系统图](../schemes原理图/system-wiring.png)、[视觉与摄像头](camera-vision.md)、[标定指南](calibration-guide.md)、[FMEA](FMEA.md) | 已明确纯视觉架构、分支供电、共地、噪声和标定流程 / Vision-only architecture, power branches, common ground, interference and calibration method are documented | 实物驱动器/电池/稳压/舵机型号，支路典型与峰值电流、最低电压、保险规格、相机安装实测、故障注入结果 / Exact hardware models, branch currents, minimum voltage, fuse rating, camera pose and fault-injection results |
| 3. 软件架构与障碍策略 / Software and obstacle strategy | [软件架构](software-architecture.md)、[`bev_segmentation.py`](../src源代码/bev_segmentation.py)、[UNO视觉执行端](../src源代码/VisionSerialExecutor/VisionSerialExecutor.ino)、[测试流程](tests.md) | 已有模块说明、视觉恢复逻辑、Arduino安全状态机和250 ms命令看门狗 / Module documentation, vision recovery logic, Arduino safety state machine and 250 ms watchdog are present | 相机标定参数、停车区与圈数逻辑、边界场景结果、识别率/误检率/延迟/FPS、连续回合数据、最终视频对应提交 / Calibration values, parking/lap logic, edge-case results, recognition metrics, latency/FPS, consecutive-lap data and a video-matched commit |
| 4. 系统思维与工程决策 / Systems thinking and engineering decisions | [工程日志](engineering-log.md)、[可归档PDF](engineering-log.pdf)、[FMEA](FMEA.md)、[BOM与选型](BOM.md)、[变更记录](CHANGELOG.md) | 已有高低层分工、约束、风险、早期方案与当前纯视觉方案的区别 / High/low-level roles, constraints, risks and the transition from early concepts to the vision-only system are documented | 用实测数据完成至少三条“选择X而非Y”的结论，并给出改动前/后数据 / At least three measured “X rather than Y” decisions with before/after data |
| 5. 可复现性与GitHub质量 / Reproducibility and GitHub quality | [README](../README.md)、[复现指南](reproduction-guide.md)、[源代码索引](../src源代码/README.md)、[测试](tests.md)、[版本记录](CHANGELOG.md) | 目录沿用官方模板；README超过5000字符；含代码、DXF、接线、测试与版本说明 / Official-template structure; README exceeds 5,000 characters; code, DXF, wiring, tests and version notes are present | 主分支至少3条内容明确的提交、车辆六视图、趣味团队照、最终CAD、冻结软件版本/镜像校验值、陌生队员复现记录 / At least three meaningful main-branch commits, six vehicle views, informal team photo, final CAD, frozen software/image checksums and an independent reproduction record |

## 3. 维度1：移动性能与机械设计 / Dimension 1: Mobility and Mechanical Design

### 3.1 设计主张 / Design Claim

车辆采用汽车式阿克曼转向、前后差速器和中央传动轴四轮驱动。该方案的目标是减少刚性四轮转向时的轮胎侧滑，提高直线稳定性，并让转向轨迹连续。代价是轴距、轮距、内外轮转角和舵机行程共同限制最小转弯半径，机械间隙与左右不对称会直接转化为路径误差。

The vehicle uses automotive Ackermann steering, front and rear differentials and shaft-driven four-wheel drive. The design aims to reduce tyre scrub, improve straight-line stability and produce continuous turning trajectories. The trade-off is that wheelbase, track width, inner/outer steering angles and servo travel jointly limit turning radius, while mechanical play and left/right asymmetry directly become path errors.

### 3.2 计算与论证入口 / Calculation and Rationale Entry Points

- 底盘规格、理论车速、牵引力与转向关系：[机械分析](mechanical-analysis.md)。 / Chassis data, theoretical speed, traction and steering relationships: [mechanical analysis](mechanical-analysis.md).
- 层板制造文件与机械复现边界：[模型目录](../models模型/README.md)。 / Plate manufacturing file and mechanical reproduction boundaries: [models](../models模型/README.md).
- 规格值与装车实测分开记录：[测试流程](tests.md)。 / Catalogue values and assembled measurements are separated in the [test procedure](tests.md).

### 3.3 满分证据包 / Full-Score Evidence Package

1. 装车完成后测量长、宽、高、总质量、重心大致位置和离地间隙，并拍摄测量过程。 / Measure final length, width, height, mass, approximate centre of gravity and ground clearance, with photographs of the method.
2. 架空逐步增加舵机角度，记录左/中/右安全角，不以舵机嗡鸣作为限位。 / Increase servo angle with wheels lifted and record safe left/centre/right limits; do not use servo buzzing as a limit indicator.
3. 以相同电量、轮胎和地面测量左右最小转弯半径，各做5次，记录均值、范围和异常。 / Measure left and right minimum turning radii five times each with the same battery, tyres and surface; record mean, range and anomalies.
4. 对至少5个速度命令做固定距离计时，记录平均速度、停止距离和电池电压。 / Time a fixed distance for at least five speed commands and record mean speed, stopping distance and battery voltage.
5. 用“问题—修改—结果”展示至少一次机械迭代，例如相机支架刚度、转向连杆对称性或线束干涉。 / Show at least one mechanical iteration as “problem—change—result”, such as camera-mount stiffness, steering-link symmetry or wiring interference.

## 4. 维度2：动力与传感器架构 / Dimension 2: Power and Sensor Architecture

### 4.1 架构主张 / Architecture Claim

当前车辆只以USB彩色摄像头感知赛道和红绿障碍。Orange Pi负责视觉，Arduino负责确定性执行和本地失效停车。选择单摄像头的优势是信息密度高、可同时判断边线、方向和颜色，且机械布置简洁；代价是缺少独立距离冗余，对光照、反光、遮挡、广角畸变、掉帧和计算延迟更加敏感，因此必须通过标定、固定安装、低置信度降速和命令看门狗补偿。

The current vehicle uses a USB colour camera as its only track and red-green obstacle sensor. The Orange Pi handles vision; the Arduino provides deterministic execution and local fail-safe stopping. A single camera offers high information density and can interpret borders, direction and colour with simple mechanical layout. The trade-off is no independent ranging redundancy and greater sensitivity to lighting, reflections, occlusion, wide-angle distortion, dropped frames and computation delay, so calibration, rigid mounting, low-confidence slowdown and a command watchdog are mandatory.

### 4.2 电源边界 / Power Boundaries

- 电机功率、Orange Pi 5 V/3 A和控制/舵机使用规划支路；UNO 5 V不得承担舵机、电机或Orange Pi大电流。 / Motor power, Orange Pi 5 V/3 A and control/servo use planned branches; the UNO 5 V pin must not carry servo, motor or Orange Pi load current.
- 大电流回流与USB/串口分开走线但控制地相连；最终保险、线径和稳压额定值必须由实物数据确定。 / High-current return paths are routed separately from USB/serial while control grounds remain common; final fuse, wire gauge and regulator ratings must follow actual hardware data.
- 正式图纸：[PNG接线图](../schemes原理图/system-wiring.png)与[接线说明](../schemes原理图/wiring.md)。 / Formal drawing: [PNG wiring diagram](../schemes原理图/system-wiring.png) and [wiring guide](../schemes原理图/wiring.md).

### 4.3 满分证据包 / Full-Score Evidence Package

1. 拍摄电池、稳压、驱动器、舵机标签和全车布线，填写准确型号与额定值。 / Photograph labels and full wiring for the battery, regulators, driver and servo; enter exact models and ratings.
2. 分别记录静止、视觉运行、直行、最大转向、电机启动时的电池电压/电流，以及Orange Pi 5 V最低值。 / Record battery voltage/current and minimum Orange Pi 5 V while idle, running vision, driving straight, steering fully and starting the motor.
3. 用 `P=U×I` 计算每支路典型/峰值功率和至少25%的设计余量；根据峰值选择保险和稳压。 / Calculate typical/peak branch power with `P=U×I` and at least 25% design margin; select fuse and regulator from peak values.
4. 标定相机内参、畸变、安装高度/俯仰、ROI、曝光、白平衡和HSV阈值。 / Calibrate intrinsics, distortion, height/pitch, ROI, exposure, white balance and HSV thresholds.
5. 注入强光、阴影、反光、拔相机、断串口和5 V压降故障，记录停车时间和恢复条件。 / Inject bright light, shadows, reflections, camera loss, serial loss and 5 V sag; record stop time and recovery conditions.

## 5. 维度3：软件架构与障碍应对策略 / Dimension 3: Software and Obstacle Strategy

### 5.1 模块与责任 / Modules and Responsibilities

| 层 / Layer | 文件 / File | 责任 / Responsibility | 安全边界 / Safety Boundary |
|---|---|---|---|
| 图像预处理 / Image preprocessing | [`bev_road.py`](../src源代码/bev_road.py) | 亮度、道路候选、实验BEV、连通域 / Brightness, road candidates, experimental BEV and components | 当前不是最终标定BEV / Not yet a final calibrated BEV |
| 视觉与策略 / Vision and strategy | [`bev_segmentation.py`](../src源代码/bev_segmentation.py) | 红绿HSV、道路密度、CW/CCW、恢复、约20 Hz命令 / Red-green HSV, road density, CW/CCW, recovery and ~20 Hz commands | 初始/退出速度为0；参数需实车冻结 / Zero initial/exit speed; parameters require vehicle freeze |
| 安全执行 / Safe execution | [`VisionSerialExecutor.ino`](../src源代码/VisionSerialExecutor/VisionSerialExecutor.ino) | 按钮、解析、限幅、舵机、电机、250 ms超时 / Button, parsing, limits, servo, motor and 250 ms timeout | 上电不动；故障后重新按键且需新命令 / No power-on motion; re-arm and fresh command after fault |

### 5.2 当前串口契约 / Current Serial Contract

- 发送格式：`steer,speed\n`，两项均为十进制整数，范围 `-100...100`。 / Format: `steer,speed\n`; both fields are decimal integers in `-100...100`.
- 发送周期：视觉端约50 ms一次；Arduino只接受完整且范围合法的一行。 / Period: approximately 50 ms from vision; Arduino accepts only a complete in-range line.
- 安全超时：250 ms无合法命令，电机PWM归零、舵机回中并进入 `COMMS_FAILSAFE`。 / Timeout: after 250 ms without a valid line, motor PWM goes to zero, steering centres and the state becomes `COMMS_FAILSAFE`.
- 恢复：必须物理按键重新启动，并在按键后收到新合法命令。 / Recovery: physical re-arm is required, followed by a fresh valid command.
- 协议局限：目前没有序号、源时间戳、CRC和确认；因此不能把该文本协议描述为抗损坏最终协议。 / Limitation: there is no sequence, source timestamp, CRC or acknowledgement, so this text protocol is not claimed to be a corruption-resistant final protocol.

### 5.3 满分证据包 / Full-Score Evidence Package

1. 以流程图/状态机说明道路、红绿障碍、恢复、停车区、圈数和最终停车。 / Document track, red-green obstacles, recovery, parking zone, lap counting and final stop with flow/state diagrams.
2. 冻结全部参数和软件版本，记录命令行、配置文件和镜像SHA-256。 / Freeze all parameters and software versions; record command line, configuration and image SHA-256.
3. 按颜色、距离、中心/边缘、光照和同时出现分组测试，报告召回率、误检率、通过侧正确率。 / Test by colour, distance, centre/edge, lighting and simultaneous objects; report recall, false-positive rate and passing-side accuracy.
4. 报告端到端延迟的均值、95百分位和最大值，以及FPS、掉帧和30分钟稳定性。 / Report mean, 95th-percentile and maximum end-to-end latency, plus FPS, dropped frames and 30-minute stability.
5. 连续完成至少10个完整回合，记录每回合时间、碰撞、人工干预、失败类型和唯一改动。 / Complete at least ten consecutive full laps and record time, contacts, intervention, failure type and the single change between runs.

## 6. 维度4：系统思维与工程决策 / Dimension 4: Systems Thinking and Engineering Decisions

### 6.1 已明确约束 / Defined Constraints

- 规则约束：自动驾驶、启动要求、比赛通信限制、车辆尺寸与工程文件截止时间。 / Rule constraints: autonomy, start requirement, competition communication limits, vehicle dimensions and documentation deadline.
- 感知约束：仅摄像头，无超声波和编码器冗余。 / Sensing constraint: camera only, with no ultrasonic or encoder redundancy.
- 机械约束：260×140×85 mm基础底盘、174 mm轴距、123 mm轮距、475 mm标称最小转弯半径。 / Mechanical constraints: 260×140×85 mm base chassis, 174 mm wheelbase, 123 mm track and 475 mm rated minimum radius.
- 动力约束：电机启动与舵机峰值可能造成压降；Orange Pi需要稳定5 V支路。 / Power constraints: motor start and servo peaks may cause sag; the Orange Pi needs a stable 5 V branch.
- 算力约束：480p/30 FPS输入，CPU/OpenCV为可复现基线，任何NPU优化都必须单独验证。 / Compute constraints: 480p/30 FPS input, CPU/OpenCV as the reproducible baseline; any NPU optimisation requires separate validation.
- 时间约束：必须在截止日期前把实测、照片、提交和PDF归档。 / Schedule constraint: measurements, photographs, commits and PDF must be archived before the deadline.

### 6.2 当前方案取舍 / Current Trade-offs

| 选择 / Choice | 放弃或代价 / Alternative or Cost | 选择理由 / Rationale | 验证状态 / Validation |
|---|---|---|---|
| 阿克曼而非差速转向 / Ackermann rather than skid steering | 机构和标定更复杂 / More mechanics and calibration | 更接近汽车、直线稳定、轮胎侧滑小 / Automotive motion, straight stability, reduced scrub | 理论说明完成；实测待补 / Rationale complete; measurements pending |
| Orange Pi高层 + UNO底层 / Orange Pi high level + UNO low level | 两控制器和串口增加复杂度 / Two controllers and serial add complexity | Linux适合视觉，UNO提供确定性输出和本地看门狗 / Linux suits vision; UNO adds deterministic output and local watchdog | 代码闭环已建立；实车待测 / Code chain present; vehicle test pending |
| 单USB彩色摄像头 / One USB colour camera | 无独立距离冗余，受光照影响 / No range redundancy; lighting sensitivity | 同时获取赛道几何和红绿颜色，布置简单 / Track geometry and colour from one sensor, simple layout | 参数与识别指标待实测 / Parameters and metrics pending |
| 有线串口而非无线控制 / Wired serial rather than wireless control | 需要固定线束 / Requires secured cabling | 延迟稳定、离线可复现、符合比赛通信约束 / Stable latency, offline reproduction and rule alignment | 程序已实现；线束待最终确认 / Implemented; final harness pending |
| 开环速度而非编码器PI / Open-loop speed rather than encoder PI | 电量和负载导致速度变化 / Speed varies with battery and load | 当前车辆明确不读取编码器，降低集成复杂度 / Current vehicle does not read encoders; simpler integration | 必须用速度映射与停车距离补偿 / Requires speed/stopping-distance mapping |

### 6.3 数据驱动结论模板 / Data-Driven Decision Template

每条最终决策必须写成：**约束/问题 → 候选X与Y → 同条件测试 → 量化结果 → 选择 → 新风险与缓解 → 对应提交和证据。** 例如只有在完成同电量对比后，才能写“选择速度上限X而非Y，因为95%停车距离由A降至B且完整回合时间仍满足目标”。

Each final decision must follow: **constraint/problem → candidates X and Y → controlled test → quantified result → selection → new risk and mitigation → matching commit and evidence.** For example, only after a same-battery comparison may the team state, “speed limit X was selected over Y because the 95th-percentile stopping distance fell from A to B while lap time still met the target.”

## 7. 维度5：可复现性与GitHub质量 / Dimension 5: Reproducibility and GitHub Quality

### 7.1 规则核心检查 / Core Rule Checks

| 要求 / Requirement | 仓库位置 / Repository Location | 状态 / Status |
|---|---|---|
| README不少于5000字符 / README at least 5,000 characters | [`README.md`](../README.md) | 已满足篇幅；继续以内容质量为准 / Length satisfied; quality still governs |
| 至少3条有效提交 / At least three meaningful commits | Git历史 / Git history | 主分支提交说明仍需由队伍整理；不要把全部修改压成一次提交 / Main-branch messages still need team action; do not squash all work into one commit |
| 代码 / Code | [`src源代码/`](../src源代码/README.md) | 已有视觉和底层候选程序 / Vision and candidate lower-level code present |
| CAD / CAD | [`models模型/`](../models模型/README.md) | 有层板DXF；最终支架CAD待补 / Plate DXF present; final mount CAD pending |
| 接线 / Wiring | [`schemes原理图/`](../schemes原理图/wiring.md) | 有PNG/SVG图和文字接线；实物型号待核 / PNG/SVG and written wiring present; hardware models pending |
| 测试流程 / Test procedure | [`tests.md`](tests.md) | 流程与表格齐全；真实数据待录入 / Procedure and tables present; actual data pending |
| 版本日志 / Version log | [`CHANGELOG.md`](CHANGELOG.md) | 已有阶段记录；需与提交对应 / Stage log present; map it to commits |
| 结构化可归档日志 / Archival engineering log | [`engineering-log.pdf`](engineering-log.pdf) | 已生成；最终实测后重新生成 / Generated; rebuild after final measurements |
| 车辆六视图 / Six vehicle views | [`v-photos车辆照片/`](../v-photos车辆照片/README.md) | 待拍 / Pending |
| 团队照片与视频 / Team photo and video | [团队照片](../t-photos团队照片/README.md)、[视频](../video视频/video.md) | 正式照和视频已有；趣味团队照待补 / Official photo and video present; informal photo pending |

### 7.2 独立复现验收 / Independent Reproduction Acceptance

由一名未编写程序的队员仅阅读仓库完成：找到接线、核对引脚、编译UNO、安装依赖、复制串口配置、解释状态机、架空启动、触发通信超时并定位日志。记录所用时间、卡住步骤和文档修改。只有当不需要口头补充时，才可声明“完全可复现”。

A member who did not write the software must use only the repository to locate wiring, verify pins, build the UNO sketch, install dependencies, copy serial configuration, explain the state machine, perform a lifted-wheel start, trigger a communication timeout and locate the logs. Record time, blocked steps and resulting documentation edits. “Fully reproducible” may be claimed only when no verbal additions are required.

## 8. 提交前红线 / Pre-Submission Red Lines

- 不把目录规格、商品页面或理论值写成装车实测。 / Do not present catalogue, listing or theoretical values as assembled measurements.
- 不把存在于仓库中的原型写成“比赛验证通过”。 / Do not describe a repository prototype as competition-validated.
- 不把旧超声波/编码器程序描述为当前车辆传感器。 / Do not describe historical ultrasonic/encoder code as current sensing.
- 不在驱动器、电池、稳压器型号未核实前写入确定型号。 / Do not assert driver, battery or regulator models before verification.
- 不保证“满分”；只提交裁判可独立核验的证据。 / Do not guarantee a full score; submit evidence that judges can independently verify.
- 国际赛提交前复核英文内容、公开链接、截止日期快照和至少一年的仓库公开保留要求。 / Before international submission, verify English content, public links, deadline snapshot and the one-year public repository retention requirement.

## 9. 最终签署 / Final Sign-Off

| 负责人 / Owner | 核验内容 / Verification | 日期 / Date | 提交号/证据 / Commit or Evidence | 签名 / Sign-off |
|---|---|---|---|---|
| 陆昭颖 / Lu Zhaoying | 视觉、状态机、参数、软件版本 / Vision, state machine, parameters, software versions | | | |
| 张隽泽 / Zhang Junze | 尺寸、机械图、转向、六视图 / Dimensions, mechanical drawings, steering, six views | | | |
| 黄鸣博 / Huang Mingbo | 型号、接线、电流、电压、保险、安全 / Models, wiring, current, voltage, fuse, safety | | | |
| 薛源 / Xue Yuan | 规则、视频、提交截止与总体验收 / Rules, video, deadline and final acceptance | | | |

