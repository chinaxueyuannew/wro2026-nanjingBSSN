# 测试流程与记录 / Test Procedure and Records

**范围：** 摄像头标定、视觉识别、视觉转向、串口超时和故障停车；不包含超声波或编码器测试。

**Scope:** Camera calibration, visual perception, vision steering, serial timeout and fault stopping; ultrasonic and encoder tests are excluded.

每次记录日期、提交号、电池、场地、参数和结果，失败记录也保留。

Record date, commit, battery, field, parameters and result for every test, including failures.

## 1. 静态与抬轮 / Static and Lifted-Wheel

- 核对极性、共地、紧固件、轮胎、拉杆和线束 / Check polarity, common ground, fasteners, tyres, links and wiring.
- 确认舵机中位、转向符号和电机方向 / Confirm servo centre, steering sign and motor direction.
- 遮挡、冻结或停止视觉，确认目标归零和Arduino超时停车 / Obstruct, freeze or stop vision and confirm zero target and Arduino timeout stop.
- 测试总开关和启动按钮 / Test main switch and start button.

## 2. 摄像头与视觉输入 / Camera and Vision Input

固定高度、俯仰、焦距后，记录UVC模式、内参、畸变、ROI、HSV、曝光和白平衡。

After fixing height, pitch and focus, record UVC mode, intrinsics, distortion, ROI, HSV, exposure and white balance.

| 日期 / Date | 提交 / Commit | 分辨率/FPS / Resolution/FPS | 高度/角度 / Height/Angle | 重投影误差 / Reprojection Error | 延迟 / Latency | 结论 / Result |
|---|---|---|---|---:|---:|---|
| 待测 / TBD | 待填 / TBD | 待测 / TBD | 待测 / TBD | 待测 / TBD | 待测 / TBD | |

## 3. UNO视觉命令与安全状态 / UNO Vision Commands and Safety State

测试前抬起驱动轮，使用115200 baud串口逐行发送下表输入。每项至少重复5次；用串口时间戳、逻辑分析仪或高速录像记录从最后合法命令到电机PWM归零的时间。任何结果都必须写入“实际结果”，不得只勾选通过。

Lift the drive wheels before testing and send each line below at 115200 baud. Repeat every item at least five times. Use serial timestamps, a logic analyser or high-speed video to measure the time from the last valid command to zero motor PWM. Enter the actual result; a pass tick alone is insufficient.

| ID | 前置状态 / Precondition | 输入/动作 / Input or Action | 预期 / Expected | 实际结果 / Actual Result |
|---|---|---|---|---|
| U-01 | 刚上电 / Just powered | 连续发送 `0,30`，不按D8 / Send `0,30`, do not press D8 | `WAIT_START`，电机始终0 / Motor remains zero | 待测 / TBD |
| U-02 | `WAIT_START` | 按D8但不发送新命令 / Press D8, send no fresh line | 250 ms后 `COMMS_FAILSAFE` / Fail-safe after 250 ms | 待测 / TBD |
| U-03 | D8刚按下 / Just armed | `0,0` | 舵机中位、电机0 / Centre, motor zero | 待测 / TBD |
| U-04 | 已启动 / Armed | `-100,100` 与 `100,-100` | 输出不超过舵机/PWM限幅 / Output stays within limits | 待测 / TBD |
| U-05 | 已启动 / Armed | `101,0`, `0,-101`, `abc,20`, `20`, `1,2,3` | 全部忽略，不刷新看门狗 / Ignore all; watchdog not refreshed | 待测 / TBD |
| U-06 | 正在运动 / Moving | 停止发送 / Stop transmission | 250 ms目标内PWM归零、舵机回中 / Zero PWM and centre at 250 ms target | 待测 / TBD |
| U-07 | `COMMS_FAILSAFE` | 恢复发送但不按D8 / Resume lines without D8 | 不自动运动 / No automatic motion | 待测 / TBD |
| U-08 | `COMMS_FAILSAFE` | 按D8后发送新合法命令 / D8 then fresh valid line | 重新进入受限执行 / Resume limited execution | 待测 / TBD |
| U-09 | 正在运动 / Moving | 按D8 / Press D8 | 立即回到 `WAIT_START` 并停车 / Return to wait and stop | 待测 / TBD |
| U-10 | 已启动 / Armed | 发送超长行后发送 `0,0` / Overlong line, then `0,0` | 超长行丢弃；下一完整行正常 / Overflow discarded; next line works | 待测 / TBD |

## 4. 视觉控制 / Vision Control

从低速测试道路权重、信标权重、最大转向、减速阈值和恢复时间。记录回合、横向偏差、碰撞、通过侧正确率、丢帧和蛇形。

Starting at low speed, test road weight, beacon weight, maximum steering, slowdown threshold and recovery time. Record laps, lateral deviation, collisions, passing-side accuracy, frame loss and oscillation.

| 日期 / Date | 提交 / Commit | 速度 / Speed | 最大转向 / Max Steering | 权重 / Weights | 回合 / Laps | 碰撞 / Collisions | 失效 / Failures | 结论 / Result |
|---|---|---:|---:|---|---:|---:|---:|---|
| 待测 / TBD | 待填 / TBD | 低 / Low | 待测 / TBD | 待测 / TBD | | | | |

## 5. 机械与动力 / Mechanical and Power

| 项目 / Item | 方法 / Method | 当前结果 / Current Result |
|---|---|---|
| 整车质量 / Mass | 电子秤 / Scale | 底盘0.7 kg，装车待测 / Chassis 0.7 kg; assembled TBD |
| 长宽高 / Size | 卡尺或钢尺 / Caliper or ruler | 底盘260×140×85 mm，装车待测 / Chassis value; assembled TBD |
| 轮径/轴距/轮距 / Wheel/wheelbase/track | 测量 / Measurement | 47/174/123 mm，待复核 / To verify |
| 最大转角 / Maximum angle | 抬轮逐度 / Lifted-wheel steps | 待测 / TBD |
| 转弯半径 / Turning radius | 地面轨迹 / Ground path | 标称475 mm，待测 / Rated 475 mm; TBD |
| 速度 / Speed | 固定距离 / Fixed distance | 待测 / TBD |
| 电流 / Current | 功率计 / Power meter | 待测 / TBD |
| 最低电压 / Minimum voltage | 带载记录 / Loaded logging | 待测 / TBD |

### 动力工况记录 / Power-Condition Record

| 日期 / Date | 提交 / Commit | 工况 / Condition | 电池电压均值/最低 / Battery Mean/Min | 电池电流均值/峰值 / Battery Mean/Peak | 5 V最低 / 5 V Min | 温度 / Temperature | 结论 / Result |
|---|---|---|---:|---:|---:|---:|---|
| 待测 / TBD | 待填 / TBD | 静止 / Idle | | | | | |
| 待测 / TBD | 待填 / TBD | 视觉运行 / Vision | | | | | |
| 待测 / TBD | 待填 / TBD | 直行 / Straight | | | | | |
| 待测 / TBD | 待填 / TBD | 电机启动 / Motor start | | | | | |
| 待测 / TBD | 待填 / TBD | 最大转向 / Full steering | | | | | |

## 6. 故障注入 / Fault Injection

- 低电压：检查复位和舵机抖动 / Low voltage: check resets and servo jitter.
- 阴影、反光、打滑和广角边缘：检查恢复 / Shadows, reflections, slip and wide-angle edges: check recovery.
- 松动或拔掉摄像头：确认安全停车 / Loosen or unplug camera: confirm safe stop.
- 停视觉或断串口：确认旧命令不持续 / Stop vision or serial: confirm stale commands do not persist.
- Orange Pi 5 V跌落：记录重启且不得自动恢复运动 / Orange Pi 5 V drop: log restart and prevent automatic motion recovery.

## 7. 稳定性与识别 / Stability and Recognition

固定镜像、提交、摄像头模式和温度，连续运行至少30分钟，记录FPS、延迟、温度、5 V最低电压和断连。

Fix image, commit, camera mode and temperature; run at least 30 minutes and record FPS, latency, temperature, minimum 5 V and disconnections.

红绿数据覆盖不同距离、中心/边缘、明暗、反光和同时出现，分别记录召回、颜色误判和空场误检。

Red-green data must cover distances, centre/edge, bright/dark, reflections and simultaneous colours; record recall, colour errors and empty-track false positives.

| 数据集 / Dataset | 样本数 / Samples | TP | FN | FP | 召回率 / Recall | 空场误检率 / Empty-Track FP Rate | 备注 / Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| 红色障碍 / Red obstacles | 待采 / TBD | | | | | | |
| 绿色障碍 / Green obstacles | 待采 / TBD | | | | | | |
| 红绿同时 / Both colours | 待采 / TBD | | | | | | |
| 无障碍 / Empty track | 待采 / TBD | | | | | | |

## 8. 最终通过门槛 / Final Pass Criteria

- 连续10个完整回合无人工干预 / Ten consecutive full laps without intervention.
- 零碰撞、零违规 / Zero collisions and rule violations.
- 冻帧、断相机或低置信度进入安全状态 / Safe state on frozen frames, camera loss or low confidence.
- Orange Pi、摄像头或串口失效时按时停车 / Timely stop on Orange Pi, camera or serial failure.
- 离线冷启动且无线关闭 / Offline cold start with wireless disabled.
- 参数、提交和视频一致 / Parameters, commit and video match.
- 照片、接线、CAD和实车一致 / Photographs, wiring, CAD and vehicle match.
