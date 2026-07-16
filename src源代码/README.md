# 程序目录、运行方法与验证状态 / Programs, Running Instructions and Validation Status

**当前方案：** `bev_road.py` 和 `bev_segmentation.py` 构成视觉方向，`VisionSerialExecutor.ino` 是当前UNO PWM/DIR安全执行候选；Arduino/ESP32超声波与编码器程序是团队早期自主实验，仅作历史记录。

**Current approach:** `bev_road.py` and `bev_segmentation.py` form the vision path, while `VisionSerialExecutor.ino` is the current UNO PWM/DIR safety-executor candidate. Arduino/ESP32 ultrasonic and encoder programs are earlier team-developed experiments retained only as development history.

代码进入仓库不等于完成实车比赛验证。当前车辆只使用摄像头视觉，不使用超声波或编码器。

Code being present in the repository does not mean it has passed vehicle competition validation. The current vehicle uses camera vision only, with no ultrasonic or encoder sensing.

## 1. 文件入口 / Program Index

| 程序 / Program | 平台 / Platform | 用途 / Purpose | 状态 / Status |
|---|---|---|---|
| [`main1.0.ino`](main1.0/main1.0.ino) | UNO + PWM/DIR | 历史超声波巡墙 / Historical ultrasonic wall following | 当前不使用 / Not used |
| [`UNO_AT8236`](UNO_AT8236_OpenChallenge/UNO_AT8236_OpenChallenge.ino) | UNO + AT8236 | 双PWM、编码器PI、超声波 / Dual PWM, encoder PI, ultrasonic | 团队早期自主实验 / Earlier team-developed experiment |
| [`UNO_DRV8701`](UNO_DRV8701_OpenChallenge/UNO_DRV8701_OpenChallenge.ino) | UNO + DRV8701 | PWM/DIR、编码器PI、超声波 / PWM/DIR, encoder PI, ultrasonic | 团队早期自主实验 / Earlier team-developed experiment |
| [`ESP32_AT8236`](ESP32_AT8236_OpenChallenge/ESP32_AT8236_OpenChallenge.ino) | ESP32 + AT8236 | 底层试验 / Low-level experiment | 当前不使用 / Not used |
| [`bev_road.py`](bev_road.py) | Python/OpenCV | 道路预处理和连通域 / Road preprocessing and components | 语法通过，实验工具 / Syntax passed; experimental |
| [`bev_segmentation.py`](bev_segmentation.py) | Orange Pi/Python | 红绿视觉、方向、串口和恢复 / Red-green vision, direction, serial and recovery | 语法通过，待实车验证 / Syntax passed; vehicle validation pending |
| [`VisionSerialExecutor`](VisionSerialExecutor/VisionSerialExecutor.ino) | Arduino UNO + PWM/DIR | 物理启动、命令解析、限幅和250 ms失效停车 / Physical start, parsing, limits and 250 ms fail-safe | UNO目标编译通过；待上传和实车验证 / UNO-target build passed; upload and vehicle validation pending |
| [`requirements.txt`](requirements.txt) | Python | 依赖参考 / Dependency reference | 已提供 / Included |
| [`serial_config.example.json`](serial_config.example.json) | Orange Pi | 串口示例 / Serial example | 按实机复制修改 / Copy and edit for hardware |

双PWM与PWM/DIR类接口不同，不得混用程序和接线。当前唯一视觉执行候选只处理启动、串口、限幅、舵机、电机和超时停车；驱动器实物接口核实后才能冻结为比赛版本。

Dual-PWM and PWM/DIR interfaces differ; never mix their code or wiring. The current single vision-executor candidate handles only start, serial, limits, servo, motor and timeout stop. It can be frozen as the competition version only after the physical driver interface is verified.

## 2. `bev_road.py` 道路工具 / Road Tool

程序将输入归一化到320×240，进行HLS亮度拉伸，映射到512×512画布，结合Sobel和HSV生成道路候选并显示连通域。当前源点仍为图像四角，不是严格实车BEV。

The program normalises input to 320×240, stretches HLS brightness, maps to a 512×512 canvas, combines Sobel and HSV for road candidates and displays connected components. Current source points remain the image corners and do not form a calibrated vehicle BEV.

```bash
python bev_road.py --video-in "../video视频/测试录像.mp4" --far-mask-ratio 0.5
```

按 `Q` 退出；需要图形桌面。 / Press `Q` to exit; a graphical desktop is required.

## 3. `bev_segmentation.py` 视觉原型 / Vision Prototype

模块包括摄像头/录像输入、320×240归一化、512×512画布、动态参考色、红绿HSV、CW/CCW策略、道路/信标加权转向、恢复状态机、约20 Hz串口和调试仪表板。

Modules include camera/video input, 320×240 normalisation, 512×512 canvas, dynamic reference colour, red-green HSV, CW/CCW strategy, weighted road/beacon steering, recovery state machine, approximately 20 Hz serial output and a debug dashboard.

安全修正包括初始速度为0、正确的减速/避障阈值顺序、制动先停车，以及视频丢失或退出时发送停止。这不能替代Arduino物理启动和命令超时。

Safety corrections include zero initial speed, correct slowdown/avoidance threshold order, stop-before-recovery braking and stop transmission on video loss or exit. These do not replace Arduino physical start and command timeout.

### 环境与运行 / Environment and Running

```bash
python -m pip install -r requirements.txt
python bev_segmentation.py --video-in 0 --mode cw
python bev_segmentation.py --video-in "test.mp4" --mode ccw
```

Orange Pi优先使用系统 `python3-opencv`、`python3-numpy` 和 `python3-serial`，并冻结OS、内核、Python、OpenCV和PySerial版本。

On Orange Pi, prefer system `python3-opencv`, `python3-numpy` and `python3-serial`, and freeze OS, kernel, Python, OpenCV and PySerial versions.

串口配置 / Serial configuration:

```json
{"port": "/dev/ttyACM0", "baudrate": 115200}
```

当前每约50 ms发送 `steer,speed\n`，范围 `-100...100`。协议尚无序号、时间戳、CRC或确认，Arduino必须独立实现安全超时。

The current program sends `steer,speed\n` approximately every 50 ms in the range `-100...100`. The protocol has no sequence, timestamp, CRC or acknowledgement; the Arduino must independently implement a safe timeout.

## 4. `VisionSerialExecutor.ino` UNO安全执行端 / UNO Safety Executor

当前程序与视觉文本协议直接对应，候选引脚为D2舵机、D6电机PWM、D7方向和D8物理启动/停止按钮。舵机初始安全范围为45–135°、中位90°；电机最大PWM暂限170/255。这些是低速集成初值，不是装车实测结论，必须在架空检查后再调整。

The sketch directly implements the visual text protocol. Candidate pins are D2 for the servo, D6 for motor PWM, D7 for direction and D8 for the physical start/stop button. Initial conservative steering limits are 45–135° with 90° centre, and motor PWM is temporarily limited to 170/255. These are low-speed integration defaults, not assembled-vehicle measurements, and must be adjusted only after lifted-wheel checks.

状态顺序为 `WAIT_START → VISION_DRIVE → COMMS_FAILSAFE`。上电、人工停车或通信故障时电机为0且舵机回中。按键启动后，旧串口消息不会触发运动；只有按键之后的新合法命令才能执行。250 ms看门狗触发后必须重新按键。

The state sequence is `WAIT_START → VISION_DRIVE → COMMS_FAILSAFE`. At power-up, manual stop or communication failure, motor output is zero and steering is centred. Old serial messages cannot trigger motion after arming; only a fresh valid line received after the button press may be executed. A 250 ms watchdog event requires another physical press.

### 编译验证 / Build Verification

2026-07-16使用Arduino AVR Boards `1.8.8`、Arduino UNO目标和标准Servo库 `1.3.0`完成编译。结果为程序存储空间5544 bytes（17%），全局变量277 bytes（13%）。该结果证明目标代码和依赖可编译，不代替烧录、引脚电气和实车测试。

On 2026-07-16, the sketch compiled for Arduino UNO using Arduino AVR Boards `1.8.8` and the standard Servo library `1.3.0`. It used 5,544 bytes of program storage (17%) and 277 bytes of global-variable memory (13%). This confirms target buildability and dependencies, but does not replace upload, pin-electrical or vehicle tests.

### 输入边界 / Input Boundaries

| 输入 / Input | 预期 / Expected Behaviour |
|---|---|
| `0,0` | 中位并停车 / Centre and stop |
| `-100,100`、`100,-100` | 在限幅内执行 / Execute within limits |
| `101,0`、`0,-101` | 忽略，旧合法命令的年龄继续增加 / Ignore; previous valid command continues ageing |
| `abc,20`、`20`、`1,2,3`、空行 / empty line | 忽略 / Ignore |
| 超长行 / Overlong line | 丢弃整行 / Discard entire line |
| 停止发送超过250 ms / No valid line for over 250 ms | PWM=0、舵机回中、进入故障且要求重新按键 / PWM=0, centre, fail-safe and re-arm required |

## 5. 上车前检查 / Pre-Vehicle Checks

1. 编译上传唯一视觉程序，并核对实物是PWM/DIR接口 / Build and upload the single vision sketch; verify a physical PWM/DIR interface.
2. 抬轮确认电机、舵机和命令方向 / Lift wheels and verify motor, servo and command directions.
3. 实测舵机限位 / Measure servo limits.
4. 建立 `speed` 到车速/停车距离映射 / Map `speed` to vehicle speed/stopping distance.
5. 枚举摄像头并完成广角标定 / Enumerate and calibrate the wide-angle camera.
6. 验证CW/CCW和红绿通过侧 / Verify CW/CCW and red-green passing sides.
7. 断摄像头、进程和串口均应停车 / Camera, process and serial loss must stop.
8. 运行30分钟记录FPS、延迟、温度和电压 / Run 30 minutes and log FPS, latency, temperature and voltage.
9. 关闭Wi-Fi、蓝牙和热点 / Disable Wi-Fi, Bluetooth and hotspots.

## 6. 未完成项目 / Incomplete Competition Items

- 上传到实物UNO并完成合法、畸形和超时串口测试 / Upload to the physical UNO and test valid, malformed and timeout serial inputs.
- 核实驱动器PWM/DIR兼容性、逻辑电平和电机方向 / Verify driver PWM/DIR compatibility, logic levels and motor direction.
- 若要提高通信完整性，升级序号、源时间戳、CRC和确认协议 / Add sequence, source timestamp, CRC and acknowledgement if stronger integrity is required.
- 相机内参与地面透视 / Camera intrinsics and ground perspective.
- 多光照识别数据 / Multi-light recognition data.
- 停车区、圈数和最终停车 / Parking zone, lap count and final stop.
- 无桌面自动启动与恢复 / Headless autostart and recovery.
- 视频对应的唯一提交与参数 / Unique commit and parameters matching the video.
