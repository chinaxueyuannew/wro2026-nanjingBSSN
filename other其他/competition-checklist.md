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
- [ ] 舵机、电机和Orange Pi不从UNO 5 V取大电流 / Servo, motor and Orange Pi do not draw high current from UNO 5 V.
- [ ] Orange Pi 5 V、USB-C、摄像头和串口牢固 / Orange Pi 5 V, USB-C, camera and serial are secure.
- [ ] 启动按钮有效，上电保持停止 / Start button works and vehicle stays stopped at power-up.
- [ ] Wi-Fi、蓝牙和热点关闭，`rfkill`/`ip link`通过 / Wi-Fi, Bluetooth and hotspot disabled; checks pass.
- [ ] 无异常热、味或舵机嗡鸣 / No abnormal heat, smell or servo buzz.

## 软件与场地 / Software and Field

- [ ] Arduino程序匹配实车驱动器和视觉协议 / Arduino matches driver and vision protocol.
- [x] `VisionSerialExecutor.ino` 使用Arduino AVR Boards `1.8.8`和Servo `1.3.0`通过UNO目标编译 / The executor builds for the UNO target with Arduino AVR Boards `1.8.8` and Servo `1.3.0`.
- [ ] 程序上传至实物UNO，U-01至U-10均有结果和证据 / Upload the sketch to the physical UNO and record results and evidence for U-01 through U-10.
- [ ] 冻结镜像离线自动启动 / Frozen image autostarts offline.
- [ ] 识别4 GB、摄像头和串口 / 4 GB, camera and serial are recognised.
- [ ] 保存提交、编译和参数 / Commit, build and parameters saved.
- [ ] 舵机、电机和视觉命令方向正确 / Servo, motor and vision-command directions correct.
- [ ] 文档与无超声波/编码器实车一致 / Documentation matches no-sensor wiring.
- [ ] 摄像头、视觉和串口断开均超时停车 / Camera, vision and serial loss all stop on timeout.
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
