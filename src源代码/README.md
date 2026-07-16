# 程序目录、运行方法与验证状态

本目录同时保存 Arduino/ESP32 底层控制程序和 Orange Pi/Python 视觉程序。代码“已经进入仓库”不等于“已经通过实车比赛验证”；每个版本的功能边界如下。

## 1. 文件入口

| 程序 | 运行平台 | 主要用途 | 当前状态 |
|---|---|---|---|
| [`main1.0/main1.0.ino`](main1.0/main1.0.ino) | Arduino UNO + PWM/DIR驱动 | 团队原始右侧巡墙P控制 | 基线代码；无启动状态和前方停车 |
| [`UNO_AT8236_OpenChallenge/`](UNO_AT8236_OpenChallenge/UNO_AT8236_OpenChallenge.ino) | Arduino UNO + AT8236 | 双PWM、编码器速度PI、双超声波和开放赛道状态机 | 已做静态检查，待实车验证 |
| [`UNO_DRV8701_OpenChallenge/`](UNO_DRV8701_OpenChallenge/UNO_DRV8701_OpenChallenge.ino) | Arduino UNO + DRV8701/MD02 Pro | PWM+DIR、编码器速度PI、双超声波和状态机 | 已做静态检查，待实车验证 |
| [`ESP32_AT8236_OpenChallenge/`](ESP32_AT8236_OpenChallenge/ESP32_AT8236_OpenChallenge.ino) | ESP32 + AT8236 | ESP32底层控制试验版 | 启动时关闭Wi-Fi/蓝牙，待实车验证 |
| [`bev_road.py`](bev_road.py) | Python/OpenCV | 录像道路区域预处理与连通域可视化 | Python语法通过；算法实验工具 |
| [`bev_segmentation.py`](bev_segmentation.py) | Orange Pi/Python/OpenCV | 红绿信标、道路密度、CW/CCW策略、串口控制和避障恢复 | Python语法通过；待板端与实车验证 |
| [`requirements.txt`](requirements.txt) | Python环境 | 桌面开发依赖参考 | 已提供 |
| [`serial_config.example.json`](serial_config.example.json) | Orange Pi串口配置 | 串口设备和波特率示例 | 复制后按实机修改 |

AT8236 与 DRV8701 的电机接口不同，不得混用程序和接线。最终比赛只应指定一个底层程序为正式版本，其余保留为开发记录。

## 2. `bev_road.py` 道路预处理工具

该程序用于离线观察视频中的道路区域，不直接控制车辆。处理步骤为：

1. 把输入画面归一化到 320×240；
2. 在 HLS 空间进行亮度百分位拉伸；
3. 把整幅画面映射到 512×512 工作画布；
4. 用扩张Sobel边缘和HSV饱和度抑制生成候选道路掩膜；
5. 屏蔽画面远端、近端和边框区域；
6. 标出连通域面积并显示调试窗口。

当前四个透视源点仍是整幅图像四角，因此这一版主要完成尺寸归一化和实验性映射，**尚未使用实车相机标定点形成严格鸟瞰变换**。正式BEV需要根据赛道地面四点重新标定。

```bash
python bev_road.py --video-in "../video视频/测试录像.mp4" --far-mask-ratio 0.5
```

按 `Q` 退出。该程序需要图形桌面环境显示多个 OpenCV 调试窗口。

## 3. `bev_segmentation.py` 视觉控制原型

视觉主程序包含以下模块：

- 摄像头或录像输入，默认设备索引为 `0`；
- 320×240采集归一化与512×512处理画布；
- 底部区域动态参考色和颜色差异图；
- 红色双HSV区间、绿色HSV区间及轮廓筛选；
- 顺时针 `CW` 与逆时针 `CCW` 两套道路侧边和信标策略；
- 信标转向与道路密度转向的直接加权叠加；
- `NORMAL → BRAKING → PAUSED → REVERSING → POST_REVERSE_PAUSE` 恢复状态机；
- 20 Hz左右的有线串口命令输出；
- 道路区域、信标、目标曲线、减速区和转向分量仪表板。

本轮检查已经把启动目标速度改为 `0`、修正减速/避障阈值顺序、让 `BRAKING` 阶段先发送停止而不是立即倒车，并在视频源丢失或程序退出时发送停止命令。这些改动降低误启动风险，但不能代替 Arduino 上的物理启动按钮、命令超时和独立紧急停车。

### 运行环境

桌面开发环境可使用：

```bash
python -m pip install -r requirements.txt
```

Orange Pi Linux 可优先安装系统提供的 `python3-opencv`、`python3-numpy` 和 `python3-serial`，避免架构不匹配的二进制包。最终比赛镜像必须记录操作系统、内核、Python、OpenCV和PySerial版本。

把示例配置复制为 `serial_config.json`，再按实机修改：

```json
{
  "port": "/dev/ttyACM0",
  "baudrate": 115200
}
```

运行摄像头：

```bash
python bev_segmentation.py --video-in 0 --mode cw
```

运行录像：

```bash
python bev_segmentation.py --video-in "test.mp4" --mode ccw
```

鼠标滚轮调整目标速度，右键把目标速度和当前速度归零；初始目标速度为零。正式比赛不能依赖桌面鼠标作为启动或急停装置，必须由车辆上的独立按钮和底层安全状态机实现。

### 当前串口协议

Python每约50 ms发送一行：

`steer,speed\n`

其中转向和速度均限制在 `-100...100`。底层可回传单独一行 `CW` 或 `CCW` 切换策略。该协议目前没有序号、时间戳、CRC和确认应答，属于联调原型。最终比赛协议必须增加命令超时：Orange Pi、摄像头或串口异常时，Arduino应在实测确定的安全时间内停车，不能继续执行最后一条命令。

## 4. 上车前必须确认

1. 根据实物驱动板选择唯一对应的 Arduino 程序。
2. 抬起车轮确认电机正方向、编码器正方向和舵机左右方向。
3. 实测舵机安全极限后修改转向中位及左右限位。
4. 核对 `CPR=12`、减速比 `1:8.864`、轮径 `47 mm` 与实物标签。
5. 摄像头完成分辨率/FPS枚举、广角标定和固定支架复位测试。
6. 实测CW/CCW模式、红绿柱通过侧以及串口正负号。
7. 拔掉摄像头、停止Python进程、断开串口，确认底层均能停车。
8. 连续运行至少30分钟，记录帧率、端到端延迟、Orange Pi温度和5 V最低电压。
9. 比赛时关闭Orange Pi和ESP32的Wi-Fi、蓝牙及热点。

## 5. 仍未完成的比赛级项目

- Python与Arduino之间带序号、时间戳、CRC和确认的正式协议；
- Arduino端通信看门狗与物理启动按钮联动；
- 真实相机内参与地面透视标定；
- 红绿识别率、边缘误差和多光照测试数据；
- 停车区、圈数、方向初始化和最终停车策略；
- Orange Pi无桌面自动启动服务与崩溃自动恢复；
- 与YouTube演示视频对应的唯一代码提交号和参数记录。

详细架构见 [`../other其他/software-architecture.md`](../other其他/software-architecture.md)，视觉硬件与测试要求见 [`../other其他/camera-vision.md`](../other其他/camera-vision.md) 和 [`../other其他/processor-orange-pi.md`](../other其他/processor-orange-pi.md)。
