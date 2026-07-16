# 机械模型与尺寸 / Mechanical Models and Dimensions

**当前配置：** 最终装配只需要摄像头视觉支架，不需要超声波支架或编码器信号线。

**Current configuration:** The final assembly requires only a camera mount for vision, with no ultrasonic mounts or encoder signal wiring.

基础底盘为 **RF-A101HE-109010203 阿克曼智能车**。已确认结构包括前轮舵机转向、四根转向拉杆、四轮驱动、前后差速器、中间传动轴和带霍尔编码器接口的电机。当前只使用电机驱动功能，编码器接口不接线。底部亚克力板预留Arduino UNO R3孔位，顶部安装Orange Pi、USB摄像头和电源模块。

The base platform is the **RF-A101HE-109010203 Ackermann smart-car chassis**. Confirmed features include servo-operated front-wheel steering, four steering links, four-wheel drive, front and rear differentials, a longitudinal driveshaft and motors with Hall-encoder interfaces. Only motor drive is currently used; encoder signals are not connected. The lower acrylic plate provides Arduino UNO R3 holes, while the upper plate carries the Orange Pi, USB camera and power modules.

## 团队确认的尺寸与性能 / Team-Confirmed Dimensions and Performance

| 项目 / Item | 数值 / Value |
|---|---:|
| 整车外形 / Overall size | 260 × 140 × 85 mm |
| 去防撞棉主体长度 / Body length without foam bumpers | 246 mm |
| 轴距 / Wheelbase | 174 mm |
| 轮距 / Track width | 123 mm |
| 车轮直径 / Wheel diameter | 47 mm |
| 离地间隙 / Ground clearance | 6 mm |
| 基础重量 / Base mass | 0.7 kg |
| 标称附加载荷 / Rated additional load | 0.3 kg |
| 最小转弯半径 / Minimum turning radius | 475 mm |
| 标称爬坡角 / Rated climbing angle | Below 20° / 小于20° |

安装主控、电池、摄像头和支架后，应重新测量总长、总宽、总高和总质量。

After mounting the controllers, battery, camera and brackets, remeasure overall length, width, height and mass.

本目录中的 `HSP94182层板.dxf` 是可编辑二维CAD文件，可用于层板加工和孔位复核。最终装车后必须逐项核对文件几何与实际层板；当前不宣称它已经是最终比赛版本。

The editable 2D CAD file `HSP94182层板.dxf` supports plate manufacturing and hole-position verification. Its geometry must be checked against the actual plate after final assembly; it is not yet claimed as the final competition version.

## 正式提交前待补 / Items Required Before Final Submission

- 底盘俯视尺寸图：轴距、轮距、轮径、总长、总宽和总高。 / Top-view dimension drawing: wheelbase, track, wheel diameter, overall length, width and height.
- 摄像头支架CAD/STL、距地高度和俯仰角。 / Camera-mount CAD/STL, height above ground and pitch angle.
- 控制板、电池和稳压模块固定件。 / Mounts for controllers, battery and regulators.
- 舵机中位、拉杆孔位和最大安全转角。 / Servo centre, linkage holes and maximum safe steering angle.
- 最终装配图和物料表。 / Final assembly drawing and bill of materials.
- 文件单位、加工方向、材料和紧固件规格。 / File units, manufacturing orientation, materials and fastener specifications.

不要用未经实测的商品页面数据代替最终参赛车辆尺寸。

Do not substitute unmeasured product-page data for final competition-vehicle dimensions.
