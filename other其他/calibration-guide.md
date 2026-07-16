# 标定与参数调优手册 / Calibration and Parameter-Tuning Guide

**当前范围：** 只标定舵机、摄像头、视觉参数和开环速度命令；不标定超声波或编码器。

**Current scope:** Calibrate only the servo, camera, vision parameters and open-loop speed commands; ultrasonic and encoder calibration is not used.

## 总原则 / General Principle

一次只改变一个参数，并记录提交号、电池电压、场地、轮胎和结果。顺序为机械与舵机→摄像头→视觉→速度映射→完整回合。

Change one parameter at a time and record commit, battery voltage, field, tyres and result. Follow mechanical/servo → camera → vision → speed mapping → full laps.

## 1. 舵机 / Servo

1. 抬轮并断开电机动力 / Lift wheels and disconnect motor power.
2. 输出90°并调整舵臂、拉杆到直行 / Output 90° and adjust horn/links for straight wheels.
3. 每2°寻找无机械顶死的左右极限 / Step by 2° to find non-binding limits.
4. 内缩3°–5°作为软件余量 / Move inward by 3°–5° for software margin.
5. 低速直行2 m微调中位 / Fine-tune centre over a 2 m low-speed run.
6. 保存 `SERVO_RIGHT/CENTER/LEFT` 并拍照 / Save values and photographs.

## 2. 当前不适用 / Not Applicable to Current Configuration

编码器接口不接线，不做速度闭环；前方和右侧超声波不安装。底盘规格中的CPR、减速比和团队早期超声波参数仅作历史参考。

Encoder interfaces are not connected and no speed loop is used; front and right ultrasonic sensors are not installed. CPR and gear ratio from the chassis specifications, together with the team's earlier ultrasonic parameters, are historical references only.

## 3. 视觉速度映射 / Vision Speed Mapping

架空确认方向，再用固定距离记录多个 `speed` 命令的平均速度和停车距离；在不同电量重复，设置最大速度、弯道限速、障碍减速和失效停车。当前是目标量到PWM的开环映射，不称为速度PI。

Confirm direction with wheels lifted, then record average speed and stopping distance for several `speed` commands over a fixed distance. Repeat at different battery levels and set maximum speed, turn limit, obstacle slowdown and failure stop. This is open-loop target-to-PWM mapping, not speed PI.

## 4. 视觉转向与恢复 / Vision Steering and Recovery

低速确认道路和信标转向符号；从小权重和小最大转向开始。蛇形时降低权重/限幅或增加平滑。测试直道、弯道、边缘、阴影、反光、双颜色和短时丢失。参数以完整回合成功率和零碰撞为准。

At low speed, confirm road and beacon steering signs; begin with small weights and steering limits. If oscillation occurs, reduce weights/limits or increase smoothing. Test straights, turns, image edges, shadows, reflections, both colours and temporary loss. Select parameters by full-lap success and zero collisions.

顺逆时针参数可分别保存。遮挡或目标丢失必须停车，不得盲行。

CW and CCW parameters may be stored separately. Occlusion or target loss must cause a stop, never blind travel.

## 5. 摄像头 / Camera

1. 固定最终位置、焦距和支架 / Fix final position, focus and mount.
2. 在中央、四角和不同距离采集15–20张棋盘格 / Capture 15–20 checkerboards at centre, corners and distances.
3. 保存内参、畸变系数和分辨率 / Save intrinsics, distortion and resolution.
4. 检查去畸变直线并避免过度裁剪 / Check straight lines and avoid excessive cropping.
5. 采集红、绿、黑墙、地垫、阴影和反光 / Capture red, green, black wall, mat, shadow and reflection samples.
6. 在HSV或Lab设阈值并记录光照范围 / Set HSV or Lab thresholds and record lighting ranges.
7. 用独立数据计算误检、漏检和延迟 / Measure false positives, misses and latency on independent data.
8. 核对曝光和白平衡锁定 / Check exposure and white-balance locking.

160°镜头边缘畸变明显，必须去畸变或使用像素到视角查找表。

The 160° lens has strong edge distortion; use undistortion or a pixel-to-angle lookup table.

## 标定记录 / Calibration Record

| 日期 / Date | 项目 / Item | 修改前 / Before | 修改后 / After | 条件 / Conditions | 结果 / Result | 提交 / Commit |
|---|---|---|---|---|---|---|
| 待填 / TBD | 舵机中位 / Servo centre | 90° | | 抬轮+2 m / Lifted + 2 m | | |
| 待填 / TBD | 摄像头角度 / Camera angle | 待测 / TBD | | 固定支架 / Fixed mount | | |
| 待填 / TBD | 速度映射 / Speed mapping | 默认 / Default | | 固定距离 / Fixed distance | | |
| 待填 / TBD | 道路/信标权重 / Road/beacon weights | 默认 / Default | | 赛道+障碍 / Track + obstacle | | |
