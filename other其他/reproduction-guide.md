# 完整复现指南 / Complete Reproduction Guide

**当前配置：** 只安装USB摄像头视觉链路，不安装超声波或编码器反馈。

**Current configuration:** Install only the USB-camera vision chain, with no ultrasonic sensors or encoder feedback.

## 1. 所需资料与工具 / Required Materials and Tools

- 本仓库、层板DXF、最终BOM和接线图 / This repository, plate DXF, final BOM and wiring diagram.
- Arduino IDE和USB线 / Arduino IDE and USB cable.
- Orange Pi Zero 3W 4GB、已验证镜像、microSD和读卡器 / Orange Pi, verified image, microSD and reader.
- 5 V/3 A稳压、OTG集线器和风扇 / 5 V/3 A regulator, OTG hub and fan.
- 万用表、尺、卡尺、电子秤和日志工具 / Multimeter, ruler, caliper, scale and logging tools.

## 2. 机械装配 / Mechanical Assembly

1. 检查差速器、传动轴、轮胎和拉杆 / Check differentials, shaft, tyres and links.
2. 用DXF核对孔位并固定层板 / Verify holes with the DXF and mount the plates.
3. 电池低位居中，板卡使用绝缘垫柱 / Keep battery low/central and use insulating standoffs.
4. 固定摄像头最终高度和角度 / Fix final camera height and angle.
5. 全转向检查线束不接触运动件 / Check wiring clearance through full steering travel.

## 3. 电气装配 / Electrical Assembly

1. 确认AT8236或DRV8701/MD02 Pro / Identify AT8236 or DRV8701/MD02 Pro.
2. 断电按[接线说明](../schemes原理图/wiring.md)连接 / Wire with power off using the [wiring guide](../schemes原理图/wiring.md).
3. 舵机棕GND、红4.5–7 V、黄信号 / Servo: brown GND, red 4.5–7 V, yellow signal.
4. 电机、舵机和Orange Pi使用合适独立支路 / Use suitable independent branches for motor, servo and Orange Pi.
5. 全部共地，上电前检查极性和电压 / Use common ground and check polarity/voltage before power-up.

## 4. 软件安装 / Software Installation

1. 安装Arduino IDE、Arduino AVR Boards `1.8.8`和标准Servo库 `1.3.0` / Install Arduino IDE, Arduino AVR Boards `1.8.8` and the standard Servo library `1.3.0`.
2. 打开并编译 [`VisionSerialExecutor.ino`](../src源代码/VisionSerialExecutor/VisionSerialExecutor.ino)；历史超声波/编码器程序不用于当前比赛车辆 / Open and build [`VisionSerialExecutor.ino`](../src源代码/VisionSerialExecutor/VisionSerialExecutor.ino); historical sensor sketches are not current competition code.
3. 核实实物为PWM/DIR接口，再按D2舵机、D6 PWM、D7 DIR、D8常开按钮到GND接线；若为双PWM，先修改并重新审核程序与图纸 / Verify a PWM/DIR interface, then wire D2 servo, D6 PWM, D7 DIR and a normally-open D8-to-GND button. For dual PWM, revise and re-review the sketch and drawing first.
4. 以Arduino UNO目标编译上传并匹配115200 baud；仓库记录的基线编译占用为5544 bytes程序空间和277 bytes全局变量；架空执行U-01至U-10 / Build and upload for the Arduino UNO target and match 115200 baud; the recorded baseline build uses 5,544 bytes of program storage and 277 bytes of global-variable memory; perform U-01 through U-10 with wheels lifted.
5. 写入冻结且有校验值的Orange Pi镜像 / Flash a frozen checksummed Orange Pi image.
6. 安装并记录OpenCV、NumPy、PySerial，保存系统和UVC枚举 / Install and record dependencies; save system and UVC enumeration.
7. 先用录像运行视觉，填写串口配置，再设置本地自动启动 / Test vision with recordings, set serial configuration, then configure local autostart.
8. 关闭Wi-Fi/蓝牙并保存证据 / Disable Wi-Fi/Bluetooth and preserve evidence.
9. 制作系统盘备份 / Back up the system disk.

## 5. 首次启动 / First Start

1. 抬轮，只给控制系统上电 / Lift wheels and power the control system only.
2. 确认 `WAIT_START`、电机停止和舵机中位 / Confirm `WAIT_START`, stopped motor and centred servo.
3. 启动Orange Pi，确认摄像头、视觉和串口自检且目标速度为0 / Start Orange Pi and confirm camera, vision and serial self-tests with zero target speed.
4. 拔摄像头确认Arduino保持停车 / Unplug the camera and confirm the Arduino remains stopped.
5. 按启动按钮，低速确认电机、舵机和命令符号 / Press start and verify motor, servo and command signs at low speed.
6. 完成标定和30分钟稳定性测试 / Complete calibration and a 30-minute stability test.

## 6. 复现验收 / Reproduction Acceptance

未参与编程的队员应仅依据仓库找到程序、恢复系统盘、核对接线、上传Arduino、解释状态机、低速启动并读取日志。任何需要口头提示的步骤都应写入文档。

A member not involved in programming should use only the repository to locate programs, restore the system disk, check wiring, upload Arduino code, explain the state machine, start at low speed and read logs. Any step requiring verbal help must be added to the documentation.

## 7. 尚缺资料 / Remaining Material

- 六视图和摄像头尺寸 / Six views and camera dimensions.
- 准确型号与规格书 / Exact models and datasheets.
- 最终实物型号、电源预算与接线照片 / Final physical models, power budget and wiring photographs.
- 最终镜像、自动启动和恢复说明 / Final image, autostart and recovery instructions.
- 实际OTG集线器型号 / Actual OTG hub model.
- 舵机、速度和转弯实测 / Measured servo, speed and turning data.
- 最终比赛参数、提交号和对应视频 / Final competition parameters, commit and matching video.
