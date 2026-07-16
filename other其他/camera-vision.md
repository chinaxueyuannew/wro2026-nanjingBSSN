# USB摄像头规格、安装与视觉方案 / USB Camera Specifications, Mounting and Vision

## 1. 实际购买版本 / Purchased Version

商品链接 / Product link：<https://item.taobao.com/item.htm?id=632892015154>

商品包含多种视场、帧率、彩色/黑白和夜视组合。订单截图对应以下SKU。

The product includes multiple fields of view, frame rates, colour/monochrome and night-vision combinations. The order screenshot identifies the following SKU.

| 参数 / Parameter | 团队版本 / Team Version | 证据状态 / Evidence Status |
|---|---|---|
| 接口 / Interface | USB有线 / Wired USB | 商品确认 / Product confirmed |
| 驱动 / Driver | UVC免驱 / Driver-free UVC | 页面确认，Linux待验 / Page confirmed; Linux pending |
| 图像 / Image | 彩色 / Colour | SKU确认 / SKU confirmed |
| 帧率 / Frame rate | 30 FPS | SKU确认 / SKU confirmed |
| 清晰度 / Resolution | 480p | SKU确认 / SKU confirmed |
| 视场 / Field of view | 160°广角 / 160° wide angle | SKU确认 / SKU confirmed |
| 镜头 / Lens | 有畸变 / Distorted | SKU明确 / Explicit SKU |
| 夜视 / Night vision | 非夜视 / None | SKU确认 / SKU confirmed |
| 传感器 / Sensor | GC0308 | 商品标题 / Product title |
| 品牌型号 / Brand and recorded model | HBVCAM / HBVCAM-1914S V44 | 团队购买记录 / Team purchase record |
| 类型 / Type | CMOS, 30万像素 / CMOS, 0.3 MP | 团队购买记录 / Team purchase record |
| 页面系统 / Listed systems | Windows, Android, macOS等 / etc. | Linux待验 / Linux pending |

商品页的“最大1920×1080”与30万像素、480p SKU冲突，可能是多SKU共用字段。本项目以480p/30 FPS为标称模式，并以Orange Pi实际UVC枚举为最终依据。

The page's “maximum 1920×1080” conflicts with 0.3 MP and the 480p SKU and may be a shared multi-SKU field. This project uses 480p/30 FPS as the nominal mode and treats actual Orange Pi UVC enumeration as authoritative.

## 2. 车载处理 / Onboard Processing

摄像头连接 **Orange Pi Zero 3W 4GB**。A733 CPU在Linux/OpenCV中完成采集、去畸变、HSV分割和轮廓筛选。当前算法不依赖NPU，只有完成模型转换、延迟和精度验证后才能声称使用3 TOPS NPU。

The camera connects to an **Orange Pi Zero 3W 4GB**. Its A733 CPU runs capture, undistortion, HSV segmentation and contour filtering under Linux/OpenCV. The current algorithm does not depend on the NPU; use of the 3 TOPS NPU may only be claimed after model conversion, latency and accuracy validation.

摄像头和Arduino同时接入时，需要可靠的多端口OTG集线器。视觉结果通过有线USB串口或UART发给Arduino。Orange Pi不直接驱动执行器；Arduino负责输出限幅和命令超时停车。当前没有独立距离传感器。

A reliable multi-port OTG hub is needed when connecting the camera and Arduino simultaneously. Vision results travel to the Arduino through wired USB serial or UART. The Orange Pi does not drive actuators directly; the Arduino limits outputs and stops on command timeout. No independent range sensor is installed.

仓库中的 `bev_road.py` 用于道路掩膜、实验性BEV和连通域，`bev_segmentation.py` 包含红绿HSV、CW/CCW策略、道路密度转向、串口和恢复状态机。目前仅完成语法检查和最低安全修正，仍按原型记录。

In the repository, `bev_road.py` provides road masks, experimental BEV and connected components, while `bev_segmentation.py` includes red-green HSV detection, CW/CCW strategy, road-density steering, serial output and recovery states. Only syntax checks and minimum safety corrections are complete, so it remains a prototype.

## 3. 选择30 FPS彩色的原因 / Why 30 FPS Colour Was Selected

WRO障碍任务需要区分红色和绿色。商品的120 FPS版本为黑白，不能直接保留颜色信息，因此选择30 FPS彩色版本。

The WRO obstacle task requires red-green classification. The product's 120 FPS version is monochrome and cannot directly preserve colour, so the 30 FPS colour version was selected.

车辆以0.35 m/s行驶时，每帧理论位移为： / At 0.35 m/s, theoretical travel per frame is:

`0.35 / 30 ≈ 0.0117 m = 11.7 mm`

实际延迟还包括USB、曝光和处理，应测量端到端延迟并始终处理最新帧。

Actual latency also includes USB transfer, exposure and processing. Measure end-to-end latency and always process the newest frame.

## 4. 160°广角取舍 / 160° Wide-Angle Trade-off

优点是覆盖前方和两侧、近距离障碍不易离开画面、便于观察弯角。代价是桶形畸变、单位目标像素更少和边缘误差更大。必须使用标定、去畸变或查表补偿，并测量不同位置和距离的检测误差。

Advantages are broad front/side coverage, retention of nearby obstacles in view and improved corner visibility. Costs are barrel distortion, fewer pixels per target and larger edge errors. Calibration, undistortion or lookup compensation is required, together with error measurements at different positions and distances.

## 5. 安装 / Mounting

- 安装在车辆纵向中心附近并朝向正前方 / Mount near the longitudinal centre and point straight ahead.
- 支架可重复定位并标记角度 / Use a repeatable bracket with angle marks.
- 同时看到障碍主体和接地区域，减少车身遮挡 / View obstacle bodies and ground contact while reducing body occlusion.
- 防止线束、支架或层板遮挡镜头 / Prevent wiring, bracket or plate obstruction.
- 固定USB插头，避免振动瞬断 / Mechanically secure the USB plug against vibration.
- 避免强灯直射，必要时加遮光罩 / Avoid direct strong light and add a hood if needed.
- 固定焦距后标定，角度变化后重新验证 / Calibrate after focus is fixed and revalidate after angle changes.

最终必须记录距地高度、相对前轴距离、俯仰角和安装照片；当前没有实测数据，不填写假值。

Final records must include height above ground, distance from the front axle, pitch angle and mounting photographs. No values are invented before measurement.

## 6. 障碍识别流程 / Obstacle-Detection Pipeline

1. 获取最新480p彩色帧 / Acquire the latest 480p colour frame.
2. 使用标定参数去畸变 / Undistort with calibration parameters.
3. 裁剪可行驶区域ROI / Crop the drivable-region ROI.
4. 转为HSV或Lab / Convert to HSV or Lab.
5. 生成红绿掩膜；红色使用两段色相 / Build red and green masks; use two hue ranges for red.
6. 开运算去噪、闭运算填补 / Apply opening for noise and closing for gaps.
7. 按面积、比例、位置和连续帧筛选 / Filter by area, aspect, location and temporal stability.
8. 输出 `{color, center_x, bottom_y, area, confidence, timestamp}` / Output the same record.
9. 状态机规划通过侧；超时或低置信度时停车 / Plan the passing side; stop on timeout or low confidence.

## 7. 性能指标 / Performance Metrics

| 指标 / Metric | 方法 / Method | 当前值 / Current Value | 用途 / Purpose |
|---|---|---|---|
| 分辨率与FPS / Resolution and FPS | 枚举+1000帧计时 / Enumeration + 1000-frame timing | 待测 / TBD | 确认UVC模式 / Confirm UVC mode |
| 端到端延迟 / End-to-end latency | 时间戳或高速录像 / Timestamps or high-speed video | 待测 / TBD | 安全距离 / Safety distance |
| 红/绿召回率 / Red/green recall | 多位置和光照标注集 / Labelled positions and lighting | 待测 / TBD | 减少漏检 / Reduce misses |
| 颜色误判率 / Colour error rate | 红绿混合数据 / Mixed red-green data | 待测 / TBD | 防止方向错误 / Prevent wrong avoidance |
| 空场误检 / Empty-track false positives | 无障碍完整回合 / Obstacle-free laps | 待测 / TBD | 防止无故转向 / Avoid false steering |
| 稳定检测距离 / Stable detection range | 逐级增加距离 / Incremental distance | 待测 / TBD | 设置减速点 / Set slowdown point |
| 边缘误差 / Edge-position error | 多横向角度标定 / Multiple lateral angles | 待测 / TBD | 验证去畸变 / Validate undistortion |
| 30分钟稳定性 / 30-minute stability | 掉帧、负载、温度 / Drops, load and temperature | 待测 / TBD | 验证USB和散热 / Validate USB and cooling |
| 串口延迟 / Serial latency | 采集到Arduino收包 / Capture to Arduino receive | 待测 / TBD | 设置命令超时 / Set command timeout |

## 8. 车载核验 / Onboard Verification

在Orange Pi使用 `lsusb`、`v4l2-ctl --list-devices` 和 `v4l2-ctl --list-formats-ext -d /dev/video0` 检查设备、格式、分辨率和帧率。程序必须打印实际width/height/fps。拔掉摄像头、遮挡镜头和重启视觉进程均应产生可预测停车。

On the Orange Pi, use `lsusb`, `v4l2-ctl --list-devices` and `v4l2-ctl --list-formats-ext -d /dev/video0` to inspect devices, formats, resolutions and frame rates. The program must print actual width/height/fps. Camera removal, lens obstruction and vision-process restart must all cause a predictable stop.

## 9. 规则与安全 / Rules and Safety

摄像头是唯一环境感知设备，所有处理在车上完成。比赛期间不使用Wi-Fi或蓝牙传输图像或控制。摄像头、视觉进程或串口失效时，Arduino通过命令超时停车；没有超声波安全层。

The camera is the only environmental sensor and all processing occurs onboard. Wi-Fi and Bluetooth are not used for images or control during competition. If the camera, vision process or serial link fails, the Arduino stops through its command-timeout watchdog; no ultrasonic safety layer exists.

## 10. 信息来源 / Sources

参数整理于2026-07-14，来源为团队订单记录和SKU截图。网页信息可能变化，且记录中存在分辨率表述冲突；最终结论必须以实物照片和车载UVC枚举结果为准。

Parameters were compiled on 2026-07-14 from the team order record and SKU screenshot. Online information may change and the record contains conflicting resolution claims; final conclusions must therefore be based on hardware photographs and onboard UVC enumeration.
