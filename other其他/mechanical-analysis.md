# 机械设计与理论计算 / Mechanical Design and Theoretical Calculations

**当前配置：** 编码器数据仅作底盘规格参考，当前控制不使用编码器反馈。

**Current configuration:** Encoder data is retained only as chassis reference information and is not used for current control.

## 1. 阿克曼转向 / Ackermann Steering

转弯时内前轮半径较小，所以内轮转角应大于外轮。理想关系为：

During a turn, the inner front wheel follows a smaller radius, so its steering angle should be larger. The ideal relationship is:

`cot(δ_outer) - cot(δ_inner) = W / L`

其中 `L` 为轴距，`W` 为轮距。实际关系受舵臂、拉杆孔位、间隙和轮胎变形影响，必须用俯视照片和实测转角验证。

Here `L` is wheelbase and `W` is track width. Servo horn geometry, linkage holes, play and tyre deformation affect the real relationship, which must be verified with top-view photographs and angle measurements.

## 2. 转弯半径 / Turning Radius

等效自行车模型： / Equivalent bicycle model:

`R = L / tan(δ)`

使用 `L=0.174 m` 和标称 `R=0.475 m`： / With `L=0.174 m` and rated `R=0.475 m`:

`δ_equivalent = atan(0.174 / 0.475) ≈ 20.1°`

该角度是转向几何，不是“小于20°”的爬坡指标。最终应低速完整转圈，分别测量左右轨迹半径。

This is a steering-geometry angle, unrelated to the “below 20°” climbing specification. Complete low-speed circles and measure left and right path radii separately.

## 3. 速度参考 / Speed Reference

当前车辆不接编码器，实际速度用固定距离计时。以下公式只解释底盘规格参数：

The current vehicle does not connect encoders; measure actual speed over a fixed distance. The following equation only explains the published chassis data:

`v = ΔN × πD / (CPR × i × Δt)`

使用 `CPR=12`、`i=8.864`、`D=0.047 m`，理论每脉冲约1.39 mm。必须确认CPR计数方式，否则可能产生2倍或4倍误差。

With `CPR=12`, `i=8.864` and `D=0.047 m`, theoretical travel is about 1.39 mm per pulse. The CPR counting convention must be confirmed to avoid twofold or fourfold error.

1692 rpm对应约4.17 m/s，而底盘规格资料另列3.5 m/s参考值。前者视为理论值，后者视为运行参考值，最终以实测为准。

The listed 1692 rpm corresponds to about 4.17 m/s, while the chassis specification also lists a 3.5 m/s reference. Treat the former as theoretical and the latter as practical reference; measurement is authoritative.

## 4. 驱动力与扭矩 / Traction and Torque

- `T_wheel = T_motor × i × η`
- `F_traction = T_wheel / r_wheel`

电机规格为6–12 V、1.9 A、22.8 W；舵机为4.5–7 V、400–800 mA、10 kg·cm。没有扭矩曲线和效率实测时不虚构牵引力，应以斜坡或已知阻力试验验证。

Motor specifications are 6–12 V, 1.9 A and 22.8 W; servo specifications are 4.5–7 V, 400–800 mA and 10 kg·cm. Do not invent traction without torque-curve and efficiency measurements; validate it with a ramp or known-resistance test.

## 5. 重心与安装 / Centre of Gravity and Mounting

- 电池和重件低位居中 / Keep the battery and heavy parts low and central.
- 线束远离拉杆、轴和轮胎 / Keep wiring away from links, shafts and tyres.
- 摄像头支架必须刚性且可重复定位 / Make the camera bracket rigid and repeatable.
- 电路板使用绝缘垫柱 / Use insulating standoffs under circuit boards.
- 可调结构做位置标记 / Mark all adjustable structures.

## 6. 机械验收 / Mechanical Acceptance

| 项目 / Item | 方法 / Method | 合格判据 / Criterion |
|---|---|---|
| 转向中位 / Steering centre | 低速直行2 m / 2 m low-speed straight run | 无持续偏转 / No persistent drift |
| 左右极限 / Limits | 抬轮逐度测试 / Lifted-wheel angle steps | 无顶死或干涉 / No stall or interference |
| 回差 / Backlash | 双向回中测角 / Approach centre from both sides | 可重复并记录 / Repeatable and recorded |
| 轮胎车轴 / Wheels and axles | 手动转动 / Rotate manually | 无卡滞松旷 / No binding or looseness |
| 紧固件 / Fasteners | 扭矩与标记 / Torque and marks | 无松动缺件 / No loose or missing parts |
| 摄像头支架 / Camera mount | 轻触后复查ROI / Recheck ROI after light touch | 画面稳定 / Image remains stable |
| 线束 / Wiring | 全转向观察 / Observe full steering travel | 无拉扯夹擦 / No pull, pinch or rub |
