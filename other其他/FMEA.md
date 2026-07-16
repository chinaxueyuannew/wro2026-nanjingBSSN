# 故障模式与风险分析 / Failure Mode and Effects Analysis (FMEA)

摄像头是唯一环境感知源，所以摄像头、视觉进程和串口故障是最高优先级风险。

The camera is the only environmental sensor, so camera, vision-process and serial-link failures are highest-priority risks.

严重度S、发生度O、可探测度D均为1–5，`RPN=S×O×D`。分值是初评，测试后更新。

Severity S, occurrence O and detectability D use 1–5 scales, with `RPN=S×O×D`. Scores are initial estimates and must be updated after testing.

| 故障 / Failure | 影响 / Effect | 原因 / Cause | S | O | D | RPN | 现有与后续措施 / Current and Further Controls |
|---|---|---|---:|---:|---:|---:|---|
| 上电运动 / Motion at power-up | 损坏或违规 / Damage or violation | 无启动状态 / No start state | 5 | 2 | 2 | 20 | `WAIT_START`，实测按钮 / test button |
| 舵机顶死 / Servo stall | 过流或拉杆损坏 / Overcurrent or link damage | 限位错误 / Wrong limits | 4 | 3 | 2 | 24 | 软件限位+实测余量 / Limits + measured margin |
| 电机启动复位 / Motor-start reset | 失控或停赛 / Loss or stop | 压降/共地 / Voltage drop/ground | 5 | 3 | 3 | 45 | 分支供电、测峰值、去耦 / Separate supply, peak test, decoupling |
| 转向接反 / Reversed steering | 撞墙 / Wall impact | 安装方向 / Installation | 5 | 2 | 2 | 20 | 抬轮和赛前方向检查 / Lifted and pre-run checks |
| 驱动器程序错误 / Wrong driver code | 短路或无制动 / Short or no brake | AT8236/DRV混用 / Mixed driver | 5 | 2 | 2 | 20 | 分目录并贴型号 / Separate folders and label |
| 线束卷入 / Wiring entanglement | 机械损坏 / Mechanical damage | 固定不足 / Poor securing | 5 | 2 | 3 | 30 | 扎带和全行程观察 / Ties and full-travel inspection |
| 电量下降 / Battery drop | 速度转向变化 / Motion changes | 无反馈 / No feedback | 4 | 4 | 3 | 48 | 限速、电压记录、多电量测试 / Limits, voltage logs, battery-level tests |
| 无线未关闭 / Wireless enabled | 违规 / Violation | 默认服务 / Default services | 5 | 2 | 3 | 30 | `rfkill`、`ip link`与代码复核 / `rfkill`, `ip link` and code review |
| 广角畸变 / Wide-angle distortion | 位置误差 / Position error | 160°镜头 / Lens | 4 | 4 | 3 | 48 | 标定、去畸变、边缘验证 / Calibration, undistortion, edge validation |
| 红绿误判 / Colour error | 绕行错误 / Wrong avoidance | 光照/反光 / Lighting/reflection | 5 | 3 | 3 | 45 | 多光照数据和置信度门槛 / Multi-light data and confidence gate |
| 丢帧或USB断开 / Frame or USB loss | 感知失效 / Perception loss | 松线/负载 / Loose cable/load | 5 | 2 | 4 | 40 | 帧看门狗+底层超时 / Frame watchdog + low-level timeout |
| 画面冻结 / Frozen image | 过期命令 / Stale command | 采集卡死 / Capture stall | 5 | 2 | 4 | 40 | 时间戳、重复帧检测、停车 / Timestamp, duplicate detection, stop |
| Orange Pi启动失败 / Boot failure | 无高层命令 / No high-level command | 存储/欠压 / Storage/undervoltage | 5 | 2 | 3 | 30 | Arduino保持停车、镜像备份、自检 / Arduino stop, backup, self-test |
| 过热 / Overheating | 延迟掉帧 / Latency and drops | 散热不足 / Poor cooling | 4 | 3 | 3 | 36 | 风扇和30分钟压力测试 / Fan and 30-minute stress test |
| 5 V压降 / 5 V drop | 重启/USB断开 / Reset/USB loss | 稳压或线损 / Regulator/cable | 5 | 3 | 3 | 45 | 独立5 V/3 A并测压降 / Independent 5 V/3 A and drop test |
| 串口超时或损坏 / Serial timeout/corruption | 旧命令持续 / Stale motion | 卡顿/松线/错帧 / Stall/loose/error | 5 | 3 | 3 | 45 | 当前：严格ASCII解析、范围检查、250 ms停车和重新启动；后续：序号/时间戳/CRC / Current: strict ASCII parsing, range checks, 250 ms stop and re-arm; future: sequence/timestamp/CRC |
| NPU工具链不稳 / NPU toolchain instability | 部署失败 / Deployment failure | 新软件支持 / New support | 3 | 3 | 3 | 27 | 冻结镜像并保留CPU基线 / Freeze image and retain CPU baseline |

## 高优先级验证 / High-Priority Validation

优先测试启动安全、视觉/串口失效停车、电源复位、转向、驱动器、线束和无线关闭。分别保存遮挡、USB断开、画面冻结、视觉退出和串口断开的证据。

Prioritise start safety, vision/serial failure stop, power reset, steering, driver, wiring and wireless shutdown. Preserve separate evidence for obstruction, USB loss, frozen frames, vision exit and serial disconnection.
