# 测试流程与结果记录 / Test Procedure and Results

> 范围：纯视觉识别、Orange Pi GPIO/PWM执行、故障停车和整车性能；当前车辆不包含Arduino、串口、超声波或编码器。 / Scope: vision-only perception, Orange Pi GPIO/PWM execution, fault stopping and full-vehicle performance; the current vehicle has no Arduino, serial link, ultrasonic sensor or encoder.

所有测试必须填写日期、软件提交号、系统镜像、内核、配置文件哈希、执行人、环境、至少五次重复值和原始证据路径。“通过”不能代替实测数值。

Every test must record date, software commit, system image, kernel, configuration hash, operator, environment, at least five repeated values and raw-evidence paths. “Pass” cannot replace measurements.

## 1. 测试安全前提 / Test Safety Preconditions

1. 先断开电机动力，核对3.3 V逻辑、共地、极性和电源分支。 / Disconnect motor power first; verify 3.3 V logic, common ground, polarity and power branches.
2. 首次输出测试抬起驱动轮，并使车辆不会碰到人员或物品。 / Lift the driven wheels for initial output tests and restrain the vehicle.
3. 旁站人员掌握总电源并能立即断电。 / A spotter controls the main power and can disconnect it immediately.
4. 初次运行保持 `enabled=false`；冻结映射和波形后才启用。 / Keep `enabled=false` initially; enable only after mapping and waveform sign-off.
5. 每次变更引脚、设备树、驱动器、舵机或电源后重新执行G-01至G-10。 / Repeat G-01 through G-10 after any pin, device-tree, driver, servo or power change.

## 2. GPIO/PWM安全验收 / GPIO/PWM Safety Acceptance

| ID | 操作 / Action | 预期结果 / Expected Result | 实际结果 / Actual Result | 证据 / Evidence | 结论 / Result |
|---|---|---|---|---|---|
| G-01 | `enabled=false`运行程序 / Run with `enabled=false` | `DRY_RUN`；不打开GPIO/PWM，不运动 / `DRY_RUN`; no GPIO/PWM opened and no motion | 待测 / Pending | 日志 + 枚举前后对比 / Log + enumeration diff | 待测 / Pending |
| G-02 | `enabled=true`后上电，不按按钮 / Power up without pressing the button | `WAIT_START`；电机0、舵机中位 / `WAIT_START`; zero motor, centred steering | 待测 / Pending | 波形 + 视频 / Waveform + video | 待测 / Pending |
| G-03 | 按钮授权但不给新控制更新 / Arm without a fresh control update | 不运动，250 ms后失效 / No motion; fail-safe after 250 ms | 待测 / Pending | 日志 + 波形 / Log + waveform | 待测 / Pending |
| G-04 | 输入 `-100, 0, +100`及越界值 / Apply boundary and out-of-range values | 限幅正确；脉宽/占空比符合配置 / Values bounded; pulse/duty match configuration | 待测 / Pending | 示波器/逻辑分析仪 / Oscilloscope/logic analyser | 待测 / Pending |
| G-05 | 运动时停止控制更新 / Stop updates while moving | 最后更新后约250 ms电机PWM归零 / Motor PWM zero about 250 ms after last update | 待测 / Pending | 五次延迟值 / Five latency values | 待测 / Pending |
| G-06 | G-05后恢复目标但不按按钮 / Resume targets after G-05 without button | 不自动恢复，保持停车 / No automatic recovery; remains stopped | 待测 / Pending | 日志 + 视频 / Log + video | 待测 / Pending |
| G-07 | 运动中按物理按钮 / Press physical button while moving | 立即停车并回到 `WAIT_START` / Immediate stop and `WAIT_START` | 待测 / Pending | 延迟 + 视频 / Latency + video | 待测 / Pending |
| G-08 | 拔摄像头、冻结帧或停止视觉 / Disconnect camera, freeze frames or stop vision | 请求速度0，输出层停车 / Zero request and stopped output | 待测 / Pending | 日志 + 波形 / Log + waveform | 待测 / Pending |
| G-09 | 注入异常、Ctrl+C和正常退出 / Inject exception, Ctrl+C and normal exit | PWM归零/禁用，舵机中位，资源释放 / PWM zero/disabled, steering centred, resources released | 待测 / Pending | 三类日志 + 波形 / Three logs + waveforms | 待测 / Pending |
| G-10 | 五次上电和五次正反向切换 / Five power cycles and five direction changes | 不出现上电运动；方向改变前PWM先归零 / No power-on motion; PWM zero before direction change | 待测 / Pending | 连续视频 + 波形 / Continuous video + waveform | 待测 / Pending |

### G-05原始延迟 / G-05 Raw Latencies

| 重复 / Trial | 最后更新时刻 / Last Update | PWM归零时刻 / PWM Zero | 延迟ms / Latency ms | 判定 / Result |
|---|---:|---:|---:|---|
| 1 | 待测 / Pending | 待测 / Pending | 待测 / Pending | 待测 / Pending |
| 2 | 待测 / Pending | 待测 / Pending | 待测 / Pending | 待测 / Pending |
| 3 | 待测 / Pending | 待测 / Pending | 待测 / Pending | 待测 / Pending |
| 4 | 待测 / Pending | 待测 / Pending | 待测 / Pending | 待测 / Pending |
| 5 | 待测 / Pending | 待测 / Pending | 待测 / Pending | 待测 / Pending |

## 3. 摄像头与视觉 / Camera and Vision

| ID | 测试 / Test | 方法 / Method | 指标 / Metric | 实际 / Actual |
|---|---|---|---|---|
| V-01 | 内参与畸变 / Intrinsics and distortion | 棋盘格覆盖画面各区域 / Checkerboard across the frame | 重投影误差px / Reprojection error px | 待测 / Pending |
| V-02 | 透视与ROI / Perspective and ROI | 已知地面点和赛道边界 / Known ground points and track borders | 边界误差px / Border error px | 待测 / Pending |
| V-03 | 红绿识别 / Red-green detection | 多距离、多角度、多光照标注集 / Labelled set across distance, angle and lighting | Precision, recall, F1 | 待测 / Pending |
| V-04 | 方向与道路 / Direction and road | 顺/逆时针录像及实车 / CW/CCW recordings and vehicle | 正确率 / Accuracy | 待测 / Pending |
| V-05 | 帧率与延迟 / FPS and latency | 30分钟连续运行 / 30-minute continuous run | mean/P95 FPS and latency | 待测 / Pending |
| V-06 | 低置信度策略 / Low-confidence policy | 反光、阴影、遮挡和模糊 / Reflection, shadow, occlusion and blur | 减速/停车正确率 / Correct slow/stop rate | 待测 / Pending |

红绿测试集必须包含原始图、标注、参数、运行脚本和结果CSV。禁止只展示成功样例。

The red-green dataset must include raw images, labels, parameters, run script and result CSV. Showing only successful examples is not acceptable.

## 4. 机械、电气与整车 / Mechanical, Electrical and Full Vehicle

| ID | 项目 / Item | 条件 / Condition | 记录 / Record |
|---|---|---|---|
| H-01 | 最终长宽高、质量 / Final size and mass | 完整比赛配置 / Complete competition configuration | 待测 / Pending |
| H-02 | 舵机中位与机械极限 / Steering centre and limits | 抬轮、低速、保留机械余量 / Lifted wheels, low speed, mechanical margin | 待测 / Pending |
| H-03 | 最小转弯半径 / Minimum turning radius | 顺/逆时针各5次 / Five CW and five CCW runs | 待测 / Pending |
| E-01 | 静态与视觉运行电流 / Idle and vision current | 电池、5 V和舵机支路 / Battery, 5 V and servo branches | 待测 / Pending |
| E-02 | 电机启动压降 / Motor-start voltage sag | 最低与最高测试速度 / Lowest and highest test speed | 待测 / Pending |
| E-03 | 舵机堵转风险 / Servo stall risk | 安全限位附近短时测试 / Brief test near safe limits | 待测 / Pending |
| R-01 | 直线、转弯与障碍 / Straight, turn and obstacle | 两种赛道方向各5回合 / Five laps in both directions | 成功率、时间、碰撞 / Success, time, contacts |
| R-02 | 停车区与圈数 / Parking and lap count | 完整规则流程 / Complete rule flow | 待实现/待测 / Pending implementation/test |
| R-03 | 30分钟稳定性 / 30-minute stability | 比赛速度、摄像头与日志全开 / Competition speed, camera and logging | 重启、掉帧、温度 / Restarts, drops, temperature |

## 5. 单板故障边界测试 / Single-board Fault-Boundary Test

进程看门狗不能证明Linux或PWM整体冻结时一定停车。完成常规测试后，应在抬轮和可立即断电条件下，分别注入：视觉线程停止、主循环停止、看门狗线程停止、用户态进程挂起、GPIO/PWM设备异常以及受控的系统失联。记录哪些故障仍能让输出归零，哪些不能，并据此关闭FMEA中的独立硬件失效保护决策。

A process watchdog does not prove stopping during a complete Linux or PWM freeze. After normal tests, with wheels lifted and immediate power removal available, separately inject a stopped vision thread, stopped main loop, stopped watchdog thread, suspended user process, GPIO/PWM device error and controlled system unresponsiveness. Record which faults still zero outputs and which do not, then use the results to close the independent-hardware-fail-safe decision in the FMEA.

## 6. 测试签字 / Test Sign-off

| 角色 / Role | 姓名 / Name | 日期 / Date | 结论 / Decision | 签字 / Signature |
|---|---|---|---|---|
| 程序 / Programming | 陆昭颖 / Lu Zhaoying | 待填 / Pending | 待填 / Pending | 待填 / Pending |
| 结构 / Mechanical | 张隽泽 / Zhang Junze | 待填 / Pending | 待填 / Pending | 待填 / Pending |
| 电子 / Electronics | 黄鸣博 / Huang Mingbo | 待填 / Pending | 待填 / Pending | 待填 / Pending |
| 教练 / Coach | 薛源 / Xue Yuan | 待填 / Pending | 待填 / Pending | 待填 / Pending |
