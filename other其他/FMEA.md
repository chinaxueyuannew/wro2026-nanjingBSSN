# 故障模式与风险分析 / Failure Mode and Effects Analysis (FMEA)

摄像头是唯一环境感知源，且当前视觉与GPIO/PWM执行位于同一Orange Pi，因此摄像头/视觉失效、控制更新停止、GPIO/PWM错误和整板冻结是最高优先级风险。

The camera is the only environmental sensor, and vision and GPIO/PWM execution share one Orange Pi. Camera/vision loss, stopped control updates, GPIO/PWM errors and complete-board freezes are therefore highest-priority risks.

严重度S、发生度O、可探测度D均为1–5，`RPN=S×O×D`。以下为设计初评，必须用实测发生率与可探测性更新。 / Severity S, occurrence O and detectability D use 1–5 scales, with `RPN=S×O×D`. These are design-stage estimates and must be updated with measured occurrence and detectability.

| 故障 / Failure | 影响 / Effect | 原因 / Cause | S | O | D | RPN | 现有控制 / Current Controls | 关闭措施 / Closure Action |
|---|---|---|---:|---:|---:|---:|---|---|
| 上电运动 / Motion at power-up | 人身、损坏或违规 / Injury, damage or violation | 输出默认值错误 / Wrong output defaults | 5 | 2 | 2 | 20 | `enabled=false`模板、`WAIT_START`、电机0 / Disabled template, `WAIT_START`, zero motor | G-01/G-02五次上电 / Five G-01/G-02 cycles |
| GPIO/PWM映射错误 / Wrong GPIO/PWM mapping | 误动作、短路或无控制 / Unintended motion, short or no control | 编号体系/设备树混淆 / Numbering or device-tree confusion | 5 | 3 | 4 | 60 | 所有模板映射为 `-1`，非法配置拒绝启用 / Template mappings `-1`; invalid config rejected | 排针/设备树/枚举三方核对并签字 / Three-way mapping check and sign-off |
| 3.3 V逻辑不兼容 / Incompatible 3.3 V logic | 不动作或损坏GPIO / No action or GPIO damage | 驱动器阈值未知 / Unknown driver thresholds | 5 | 2 | 4 | 接线前核验，必要时电平转换 / Verify first; level shift if needed | 数据与示波器实测 / Datasheet and scope measurement |
| 舵机顶死 / Servo stall | 过流或拉杆损坏 / Overcurrent or link damage | 脉宽限位错误 / Wrong pulse limits | 4 | 3 | 2 | 脉宽限幅、上电回中 / Pulse limits, centre at power-up | H-02机械极限与温升 / H-02 limits and temperature |
| 电机启动压降 / Motor-start sag | 重启、USB丢失或失控 / Reset, USB loss or loss of control | 稳压余量/线损 / Regulator margin or cable loss | 5 | 3 | 3 | 分支供电、保险、共地 / Separate branches, fuse, common ground | E-01/E-02峰值与最低电压 / Peak current and minimum voltage |
| 电机方向带载切换 / Direction change under torque | 驱动冲击或损坏 / Driver shock or damage | DIR改变时PWM非零 / Nonzero PWM during DIR change | 5 | 2 | 3 | 代码先归零PWM / Code zeroes PWM first | G-10波形验证 / G-10 waveform verification |
| 转向符号接反 / Reversed steering sign | 撞墙 / Wall impact | 安装/坐标约定错误 / Installation or coordinate error | 5 | 2 | 2 | DRY_RUN、抬轮与低速检查 / DRY_RUN, lifted and low-speed checks | 双向五次转弯 / Five turns each direction |
| 线束卷入或松脱 / Entangled or loose wiring | 机械损坏、信号丢失 / Mechanical damage or signal loss | 固定不足 / Poor securing | 5 | 2 | 3 | 扎带、应力释放、全行程观察 / Ties, strain relief, full-travel inspection | 六视图与赛前检查 / Six views and pre-run checks |
| 电量下降 / Battery depletion | 速度/转向变化或重启 / Motion change or reset | 无在线电量闭环 / No closed-loop battery monitoring | 4 | 4 | 3 | 限速、赛前电压和多电量测试 / Speed limits, pre-run voltage, multi-level tests | 建立可用电压窗口 / Define operating voltage window |
| 无线未关闭 / Wireless enabled | 规则违规或干扰 / Rule violation or interference | 默认服务 / Default services | 5 | 2 | 3 | 30 | `rfkill`、`ip link`、离线启动 / Radio checks and offline boot | 赛前截图与检查表 / Pre-run evidence and checklist |
| 广角畸变 / Wide-angle distortion | 位置误差 / Position error | 160°镜头 / Lens | 4 | 4 | 3 | 48 | 内参标定、去畸变、ROI / Calibration, undistortion, ROI | V-01/V-02误差数据 / Error data |
| 红绿误判 / Colour error | 绕行方向错误 / Wrong avoidance side | 光照、反光或遮挡 / Lighting, reflection or occlusion | 5 | 3 | 3 | 45 | 多光照数据、置信度门槛、减速 / Multi-light data, confidence gate, slowdown | V-03/V-06指标 / Metrics |
| USB断开或丢帧 / USB loss or frame drop | 感知失效 / Perception loss | 松线、欠压或负载 / Loose cable, undervoltage or load | 5 | 3 | 3 | 45 | 帧读取失败请求速度0 / Frame-read failure requests zero | G-08 + V-05连续测试 / G-08 + continuous test |
| 画面冻结 / Frozen image | 旧目标持续 / Stale target persists | 采集阻塞 / Capture stall | 5 | 2 | 4 | 40 | 单调时间、控制更新看门狗 / Monotonic time, control-update watchdog | 重复帧检测与G-08 / Duplicate-frame detection and G-08 |
| 主控制循环停止 / Main control loop stops | 旧输出持续 / Stale output persists | 死锁、异常或资源耗尽 / Deadlock, exception or exhaustion | 5 | 2 | 3 | 30 | 独立进程线程250 ms看门狗 / Separate process thread, 250 ms watchdog | G-05/G-09及30分钟压力 / G-05/G-09 and stress test |
| 看门狗线程停止 / Watchdog thread stops | 无软件失效停车 / No software fail-safe | 同进程故障 / Same-process fault | 5 | 2 | 5 | 50 | 当前仅可由故障注入发现 / Currently detectable only by injection | 评估独立硬件使能 / Evaluate independent hardware enable |
| Linux/PWM/整板冻结 / Linux, PWM or board freeze | PWM可能保持最后值 / PWM may hold last value | 内核、驱动、供电或硬件故障 / Kernel, driver, power or hardware fault | 5 | 2 | 5 | 50 | 总开关与人工旁站 / Main switch and spotter | 故障注入；决定硬件看门狗/EN门/常闭急停 / Inject faults; decide hardware watchdog, EN gate or NC stop |
| Orange Pi启动失败 / Orange Pi boot failure | 无控制 / No control | 存储损坏或欠压 / Storage failure or undervoltage | 5 | 2 | 2 | 20 | 默认无PWM、镜像备份、冷启动自检 / No default PWM, image backup, cold-boot check | 五次离线冷启动 / Five offline cold boots |
| 过热 / Overheating | 延迟、掉帧或重启 / Latency, drops or reset | 散热不足 / Poor cooling | 4 | 3 | 3 | 36 | 温度日志与30分钟测试 / Temperature log and 30-minute test | 固定散热方案与阈值 / Freeze cooling and thresholds |

## 高优先级关闭顺序 / High-Priority Closure Order

1. 冻结并签署真实GPIO/PWM映射和3.3 V接口兼容。 / Freeze and sign real GPIO/PWM mapping and 3.3 V compatibility.
2. 完成G-01至G-10，保留PWM、DIR和按钮波形。 / Complete G-01 through G-10 and retain PWM, DIR and button waveforms.
3. 注入摄像头丢失、画面冻结、主循环停止、进程挂起和PWM设备异常。 / Inject camera loss, frozen frames, stopped main loop, process suspension and PWM-device faults.
4. 依据Linux/PWM冻结结果决定并实现独立硬件失效保护。 / Decide and implement an independent hardware fail-safe from Linux/PWM-freeze results.
5. 完成电源、温度、30分钟稳定性、最坏停车距离和完整回合测试。 / Complete power, thermal, 30-minute stability, worst-case stopping distance and full-lap tests.

风险只有在“措施已实现 + 原始证据可追溯 + 团队签字”后才能从待关闭改为已关闭。 / A risk can be marked closed only after the control is implemented, raw evidence is traceable and the team signs it off.
