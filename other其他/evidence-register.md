# 实测与照片证据登记表 / Measurement and Photograph Evidence Register

本表用于把“待补”变成可执行任务。文件名、方法和验收标准已经预先定义；完成后在结果栏写入真实值并链接原始照片、日志或视频。不得补写不存在的测试。

This register converts “pending” items into executable tasks. Filenames, methods and acceptance criteria are predefined; after completion, enter the actual result and link the original photograph, log or video. Never backfill a test that did not occur.

## A. 机械与车辆照片 / Mechanical and Vehicle Photographs

| ID | 证据 / Evidence | 建议文件名 / Suggested Filename | 方法与画面要求 / Method and Framing | 状态/结果 / Status or Result |
|---|---|---|---|---|
| M-01 | 车辆前视 / Vehicle front | `v-photos车辆照片/vehicle-front.jpg` | 白/灰背景，车体居中，完整边界，无透视裁切 / Neutral background, centred, complete outline | 待拍 / Pending |
| M-02 | 车辆后视 / Vehicle rear | `vehicle-rear.jpg` | 同M-01 / Same as M-01 | 待拍 / Pending |
| M-03 | 车辆左视 / Vehicle left | `vehicle-left.jpg` | 镜头与车体中高处平行 / Camera parallel at mid-height | 待拍 / Pending |
| M-04 | 车辆右视 / Vehicle right | `vehicle-right.jpg` | 与左视相同焦距和距离 / Same focal length and distance as left | 待拍 / Pending |
| M-05 | 车辆俯视 / Vehicle top | `vehicle-top.jpg` | 相机垂直，清晰显示设备布局与线束 / Camera perpendicular; layout and wiring visible | 待拍 / Pending |
| M-06 | 车辆底视 / Vehicle bottom | `vehicle-bottom.jpg` | 安全支撑车辆，显示传动、转向和底盘 / Safely support vehicle; show drivetrain and steering | 待拍 / Pending |
| M-07 | 尺寸测量 / Dimensions | `measurement-dimensions.jpg` | 同一画面或组图显示长宽高和量具 / Show L/W/H and measuring tool | 待测 / Pending |
| M-08 | 整车质量 / Assembled mass | `measurement-mass.jpg` | 电子秤归零，显示整车与读数 / Tared scale, full vehicle and reading | 待测 / Pending |
| M-09 | 转向极限 / Steering limits | `steering-limits.jpg` | 左/中/右俯视组图，标角度 / Left/centre/right top views with angles | 待测 / Pending |
| M-10 | 转弯半径 / Turning radius | `turning-radius-test.jpg` | 标出轨迹圆、起点和卷尺 / Mark path circle, start and tape | 待测 / Pending |
| M-11 | 摄像头支架图 / Camera mount drawing | `camera-mount.*` | CAD + 关键尺寸 + 材料 + 固定方式 / CAD, dimensions, material and mounting | 待设计归档 / Pending |

## B. 团队证据 / Team Evidence

| ID | 证据 / Evidence | 文件名 / Filename | 状态 / Status |
|---|---|---|---|
| T-01 | 全员正式团队照 / Official all-member photo | `team-official.jpg` | 已有 / Present |
| T-02 | 全员趣味团队照 / Informal all-member photo | `team-funny.jpg` | 待拍 / Pending |
| T-03 | 黄鸣博正式照片 / Huang Mingbo portrait | `t-photos团队照片/黄鸣博.jpg` | 已有 / Present |
| T-04 | 制作过程原始照片 / Development process originals | `making-process-01...11` | 已有 / Present |

## C. 电气与动力 / Electrical and Power

| ID | 项目 / Item | 记录内容 / Required Record | 方法 / Method | 状态/结果 / Status or Result |
|---|---|---|---|---|
| E-01 | 电池 / Battery | 型号、电压、容量、最大放电、插头、照片 / Model, V, capacity, max discharge, connector, photo | 读取实物标签，不凭记忆 / Read physical label | 待核 / Pending |
| E-02 | 电机驱动器 / Motor driver | 型号、接口、逻辑电平、连续/峰值电流、照片 / Model, interface, logic, current, photo | 对照板上丝印和说明书 / Board markings and datasheet | 待核 / Pending |
| E-03 | 舵机 / Servo | 型号、电压、堵转电流、扭矩、死区 / Model, voltage, stall current, torque, deadband | 标签+电流测试 / Label + current test | 待核 / Pending |
| E-04 | Orange Pi稳压 / Regulator | 型号、输入、5 V输出、连续/峰值、效率 / Model, input, 5 V output, current, efficiency | 标签+负载测试 / Label + load test | 待核 / Pending |
| E-05 | 保护 / Protection | 总开关、保险规格、线径 / Main switch, fuse and wire gauge | 根据实测峰值和线材额定值选择 / Select from measured peak and wire rating | 待核 / Pending |
| E-06 | 静止功耗 / Idle power | 电池U/I、Orange Pi 5 V / Battery V/I, Orange Pi 5 V | 稳态30 s，记录均值/最小 / 30 s mean/min | 待测 / Pending |
| E-07 | 视觉功耗 / Vision power | 摄像头+视觉运行U/I / Camera + vision V/I | 稳态60 s / 60 s steady | 待测 / Pending |
| E-08 | 电机启动 / Motor start | 峰值电流、电池最低电压、5 V最低值 / Peak current, battery and 5 V minima | 最大记录率，5次 / Highest log rate, five trials | 待测 / Pending |
| E-09 | 最大转向 / Full steering | 舵机峰值、是否抖动/嗡鸣 / Servo peak, jitter/buzz | 架空，左右各5次 / Lifted, five each side | 待测 / Pending |
| E-10 | GPIO/PWM映射 / GPIO/PWM mapping | 物理排针、gpiochip/line、PWM chip/channel、overlay / Header, gpiochip/line, PWM chip/channel and overlay | 排针图+设备树+枚举三方核对 / Header + device tree + enumeration | 待冻结 / Pending freeze |
| E-11 | 3.3 V逻辑 / 3.3 V logic | 驱动器阈值、有效电平、空载波形 / Driver threshold, active level and unloaded waveform | 资料核对+示波器 / Documentation + oscilloscope | 待核 / Pending |

## D. 视觉与软件 / Vision and Software

| ID | 证据 / Evidence | 必须记录 / Required Record | 验收方法 / Acceptance Method | 状态/结果 / Status or Result |
|---|---|---|---|---|
| S-01 | UVC枚举 / UVC enumeration | 设备名、VID:PID、模式、FPS / Device, VID:PID, modes, FPS | 保存系统命令输出 / Save command output | 待板端 / Pending |
| S-02 | 相机标定 / Camera calibration | 矩阵、畸变、图像数、重投影误差 / Matrix, distortion, image count, reprojection error | 棋盘格，多姿态 / Checkerboard, varied poses | 待测 / Pending |
| S-03 | 安装位姿 / Installation pose | 高度、俯仰、横向偏置、ROI / Height, pitch, lateral offset, ROI | 量具+照片 / Measurement + photo | 待测 / Pending |
| S-04 | 颜色识别 / Colour recognition | 红/绿TP、FN、FP、召回、误检 / Red/green TP, FN, FP, recall, false positives | 分层样本集 / Stratified dataset | 待测 / Pending |
| S-05 | 延迟 / Latency | 均值、P95、最大端到端延迟 / Mean, P95, max end-to-end latency | 时间戳或高速录像 / Timestamps or high-speed video | 待测 / Pending |
| S-06 | 稳定性 / Stability | 30 min FPS、温度、掉帧、断连、5 V / 30 min FPS, temperature, drops, disconnects, 5 V | 固定版本连续运行 / Fixed-version endurance | 待测 / Pending |
| S-07 | GPIO/PWM边界输出 / GPIO/PWM boundary output | `-100/0/+100`及越界值对应占空比、DIR和舵机脉宽 / Duty, DIR and steering pulses for boundary/out-of-range values | G-04抬轮波形 / Lifted G-04 waveforms | 程序已实现，待硬件测 / Implemented; hardware test pending |
| S-08 | 250 ms控制更新看门狗 / 250 ms control-update watchdog | 五次实际停车时间、均值、最大值 / Five stop times, mean and maximum | 停止控制更新，示波/日志/视频 / Stop control updates; trace/log/video | 待测 / Pending |
| S-09 | 故障后恢复 / Post-fault recovery | 不自动运动；重新按键后才恢复 / No automatic motion; recover only after button re-arm | G-05/G-06故障注入 / G-05/G-06 fault injection | 待测 / Pending |
| S-10 | CW/CCW与障碍 / CW/CCW and obstacles | 通过侧、碰撞、失败、时间 / Passing side, contacts, failures, time | 两方向、红绿组合 / Both directions and colour combinations | 待测 / Pending |
| S-11 | 连续回合 / Consecutive laps | 至少10回合逐回合记录 / At least ten per-run records | 冻结提交与参数 / Frozen commit and parameters | 待测 / Pending |
| S-12 | 停车与圈数 / Parking and lap count | 状态机、成功率、边界场景 / State machine, success rate, edge cases | 独立功能+完整赛程 / Unit and full-run tests | 尚未完成 / Not implemented |
| S-13 | 进程退出清理 / Process-exit cleanup | 异常、Ctrl+C和正常退出均PWM归零/禁用 / PWM zero/disabled on exception, Ctrl+C and normal exit | G-09波形与日志 / G-09 waveform and log | 待测 / Pending |
| S-14 | 单板冻结边界 / Single-board freeze boundary | 主循环、看门狗线程、用户态进程、GPIO/PWM异常的输出状态 / Output state for loop, watchdog, process and GPIO/PWM faults | 抬轮、限流、可立即断电故障注入 / Lifted, current-limited fault injection | 待测 / Pending |

## E. 可复现性与提交 / Reproducibility and Submission

| ID | 项目 / Item | 通过条件 / Pass Condition | 状态 / Status |
|---|---|---|---|
| R-01 | README | ≥5000字符且首页可找到全部核心证据 / ≥5,000 characters and all evidence discoverable | 已达到篇幅，持续核对链接 / Length met; links checked continuously |
| R-02 | 有效提交 / Meaningful commits | 主分支至少3条不同工程主题的明确提交 / At least three clear main-branch engineering commits | 由队伍完成 / Team action required |
| R-03 | 冻结版本 / Frozen versions | OS、内核、设备树、Python、OpenCV、NumPy、python-periphery、GPIO配置和镜像SHA-256 / OS, kernel, device tree, Python, OpenCV, NumPy, python-periphery, GPIO config and image SHA-256 | 待板端 / Pending |
| R-04 | 陌生人复现 / Independent reproduction | 未参与编程者仅看仓库完成GPIO/PWM枚举、DRY_RUN、架空启动与超时停车 / Non-programmer completes GPIO/PWM enumeration, DRY_RUN, lifted start and timeout using repo only | 待做 / Pending |
| R-05 | 视频映射 / Video mapping | 日期、硬件、提交、参数、成功回合与YouTube一致 / Date, hardware, commit, parameters and laps match YouTube | 待补元数据 / Metadata pending |
| R-06 | 截止快照 / Deadline snapshot | 公共链接、提交SHA、截图、PDF和规则版本归档 / Public link, SHA, screenshot, PDF and rule version archived | 提交前 / Before submission |
