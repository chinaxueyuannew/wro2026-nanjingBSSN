# 比赛前检查表 / Competition Checklist

本检查表用于视觉唯一感知车辆，不包含超声波或编码器检查。 / This checklist is for the vision-only vehicle and contains no ultrasonic or encoder checks.

## 文件提交 / Repository Submission

- [ ] 仓库公开可访问 / Repository is publicly accessible.
- [ ] 提交记录和说明反映研发 / Commit history and messages reflect development.
- [ ] README满足当年要求 / README meets current-year requirements.
- [x] 五维评分证据地图和缺失证据登记表已建立 / Five-dimension evidence map and missing-evidence register created.
- [x] 双语结构化工程日志PDF已归档 / Bilingual structured engineering-log PDF archived.
- [x] 正式团队照、冠军照和比赛车辆照已归档 / Official team, award and competition-vehicle photos archived.
- [ ] 趣味团队照、黄鸣博个人照和车辆六视图已补 / Informal team photo, Huang Mingbo portrait and six views added.
- [ ] CAD、接线、BOM、代码和测试与实车一致 / CAD, wiring, BOM, code and tests match the vehicle.
- [ ] PNG接线图中的型号、额定值和引脚均由实物核验 / Models, ratings and pins in the PNG wiring diagram are physically verified.
- [ ] 演示视频公开可访问且版本已记录 / Video is accessible and its version recorded.
- [ ] 截止前提交并保存提交号/截图 / Submit before deadline and save commit/screenshots.

## 机械 / Mechanical

- [ ] 轮胎、拉杆、舵臂、螺母、传动轴和差速器正常 / Tyres, links, horn, nuts, shaft and differentials are sound.
- [ ] 电池、层板和摄像头支架牢固 / Battery, plates and camera mount are secure.
- [ ] 摄像头高度与角度正确 / Camera height and angle are correct.
- [ ] 线束远离车轮和传动件 / Wiring is clear of wheels and drivetrain.
- [ ] 车辆尺寸合规 / Vehicle dimensions comply.

## 电气 / Electrical

- [ ] 电池电压、极性、共地、保险和总开关正常 / Battery voltage, polarity, ground, fuse and main switch are correct.
- [ ] 舵机和电机不从Orange Pi排针取大电流 / Servo and motor do not draw load current from the Orange Pi header.
- [ ] Orange Pi 5 V、USB-C、摄像头、GPIO/PWM和共地连接牢固 / Orange Pi 5 V, USB-C, camera, GPIO/PWM and common-ground connections are secure.
- [ ] 启动按钮有效，上电保持停止 / Start button works and vehicle stays stopped at power-up.
- [ ] Wi-Fi、蓝牙和热点关闭，`rfkill`/`ip link`通过 / Wi-Fi, Bluetooth and hotspot disabled; checks pass.
- [ ] 无异常热、味或舵机嗡鸣 / No abnormal heat, smell or servo buzz.

## 软件与场地 / Software and Field

- [x] `orange_pi_gpio.py` 与视觉程序通过Python语法检查 / `orange_pi_gpio.py` and the vision program pass Python syntax checks.
- [ ] 冻结并记录实际GPIO line、PWM chip/channel、设备树和权限 / Freeze and record actual GPIO lines, PWM chip/channels, device tree and permissions.
- [ ] G-01至G-10 GPIO安全测试均有结果和证据 / Record results and evidence for GPIO safety tests G-01 through G-10.
- [ ] 冻结镜像离线自动启动 / Frozen image autostarts offline.
- [ ] 识别4 GB、摄像头、gpiochip和PWM设备 / 4 GB, camera, gpiochip and PWM devices are recognised.
- [ ] 保存提交、编译和参数 / Commit, build and parameters saved.
- [ ] 舵机、电机和视觉命令方向正确 / Servo, motor and vision-command directions correct.
- [ ] 文档与无超声波/编码器实车一致 / Documentation matches no-sensor wiring.
- [ ] 摄像头失效、视觉异常、控制更新停滞和程序退出均停车 / Camera failure, vision exception, stale control update and program exit all stop the vehicle.
- [ ] 30分钟温度、FPS和5 V正常 / Temperature, FPS and 5 V remain normal for 30 minutes.
- [ ] ROI、曝光、白平衡和红绿阈值适应现场 / ROI, exposure, white balance and thresholds suit field.
- [ ] 至少完成一个完整回合 / At least one full lap completed.
- [ ] 提交满分证据前完成连续10回合、识别率、延迟、功耗和故障注入表 / Before a full-score claim, complete ten consecutive laps, recognition, latency, power and fault-injection records.

## 上场记录 / Run Record

- 回合 / Run:
- 提交 / Commit:
- 电池与电压 / Battery and voltage:
- 参数 / Parameters:
- 成绩与时间 / Score and time:
- 触碰或失误 / Contacts or errors:
- 日志/视频 / Log/video:
- 下一轮唯一修改 / Only change for next run:
