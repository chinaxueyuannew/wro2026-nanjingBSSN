# 版本与工程迭代日志 / Version and Engineering Changelog

## V1.0 历史巡墙基线 / Historical Wall-Following Baseline

- Arduino UNO、双超声波、舵机、PWM/DIR、30 cm右墙P控制和串口日志 / Arduino UNO, dual ultrasonic, servo, PWM/DIR, 30 cm right-wall P control and serial logging.
- 局限：无启动、颜色、速度闭环、停车区或滤波 / Limits: no start state, colour, speed loop, parking zone or filtering.

## V1.1–V2.0 早期计划 / Early Plans

- 曾计划超声波滤波、编码器PID和完整状态机 / Previously planned ultrasonic filtering, encoder PID and a full state machine.
- 当时路线改为Orange Pi视觉+Arduino安全执行，并计划有线协议、绕障、圈数和停车；该架构后来被单板GPIO直控替代 / The route at that time changed to Orange Pi vision + Arduino safety execution with wired protocol, avoidance, lap count and parking; it was later replaced by single-board GPIO control.

## 2026-07-15 视觉计算平台 / Vision Compute Platform

- 确认Zero 3W 4GB/A733并区别Zero 3/H618 / Confirmed Zero 3W 4GB/A733, distinct from Zero 3/H618.
- 记录CPU、NPU、接口、5 V/3 A、散热、验收、BOM、接线、风险和复现 / Documented CPU, NPU, interfaces, power, cooling, acceptance, BOM, wiring, risk and reproduction.
- 实机枚举、协议和稳定性待验 / Hardware enumeration, protocol and stability pending.

## 2026-07-16 视觉源码与安全 / Vision Source and Safety

- 加入两份Python程序、依赖和串口示例 / Added two Python programs, dependencies and serial example.
- 默认速度改0，修正阈值和制动，丢源/退出发送停止 / Set default speed to zero, corrected thresholds/braking and stop on source loss/exit.
- 首页整合视频、照片、状态和索引 / Integrated video, photos, status and index on landing page.

## 2026-07-16 照片和赛事资料 / Photos and Competition Material

- 统一命名11张制作过程照片 / Renamed 11 process photographs consistently.
- 加入正式团队照、北京冠军照和比赛车辆照 / Added official team, Beijing championship and competition-vehicle photos.
- 趣味团队照和六视图待补 / Informal team photo and six views pending.

## 2026-07-16 视觉唯一感知 / Vision-Only Perception

- 确认只使用USB摄像头和Orange Pi，不使用超声波/编码器 / Confirmed USB camera and Orange Pi only, with no ultrasonic/encoder use.
- 当时信号链为摄像头→Orange Pi→有线串口→Arduino→执行器，现仅作上一版本记录 / The chain at that stage was camera→Orange Pi→wired serial→Arduino→actuators and is now a previous-version record only.
- 历史传感器程序统一标记为参考 / Marked historical sensor programs as references.
- 压缩视频为H.264 1080p/30 FPS、106.8秒、87.07 MiB并进入Git / Added compressed H.264 1080p/30 FPS, 106.8 s, 87.07 MiB video to Git.

## 2026-07-16 团队资料 / Team Profile

- 加入队旗、校名、成员、教练和职责 / Added flag, school name, members, coach and roles.
- 加入陆昭颖两张照片和张隽泽照片 / Added two Lu Zhaoying portraits and one Zhang Junze portrait.
- 加入黄鸣博正式成员照并补齐三名队员个人照片 / Added Huang Mingbo's formal portrait and completed the three-member portrait set.
- 首页、团队页和照片索引互链 / Linked landing page, team profile and photo index.

## 2026-07-16 全仓库中英对照 / Repository-Wide Bilingual Documentation

- 首页及全部Markdown文档改为中文后紧跟英文 / Converted the landing page and all Markdown documents to Chinese followed directly by English.
- 标题、正文、表格、检查项和图片说明均双语化 / Made headings, prose, tables, checklists and image captions bilingual.

## 2026-07-16 规则评分审计与工程归档 / Rule-Rubric Audit and Engineering Archive

- 逐页核对2026规则第8页和附录C五维30分技术文档量表 / Audited rule page 8 and the Appendix C five-dimension, 30-point documentation rubric page by page.
- 新增五维评分证据地图、缺失证据登记、提交计划和双语工程日志PDF / Added a five-dimension evidence map, missing-evidence register, commit plan and bilingual engineering-log PDF.
- 新增正式PNG/SVG接线图和可重复生成PDF的脚本 / Added formal PNG/SVG wiring diagrams and a reproducible PDF build script.
- 新增当时的视觉串口执行程序：D8物理启动、严格解析、输出限幅、250 ms看门狗和故障后重新启动；现标记为上一版本 / Added the then-current vision serial executor with D8 physical start, strict parsing, output limits, a 250 ms watchdog and post-fault re-arm; now marked as the previous version.
- 使用Arduino AVR Boards `1.8.8`和Servo `1.3.0`完成UNO目标编译：5544 bytes程序空间、277 bytes全局变量 / Completed an UNO-target build with Arduino AVR Boards `1.8.8` and Servo `1.3.0`: 5,544 bytes of program storage and 277 bytes of global-variable memory.
- 明确区分当前ASCII协议与尚未实现的序号/时间戳/CRC增强协议 / Clearly separated the current ASCII protocol from the unimplemented sequence/timestamp/CRC hardened protocol.
- 本轮只更新工作区，未暂存、提交或推送 / Updated the working tree only; nothing was staged, committed or pushed.

## 2026-07-16 Orange Pi GPIO/PWM直控 / Direct Orange Pi GPIO/PWM Control

- 删除当前车辆的具体车型编号，仅保留经实物确认的阿克曼四驱机械特征与尺寸 / Removed the current vehicle's specific model identifier while retaining verified Ackermann four-wheel-drive features and dimensions.
- 现行链路改为摄像头→Orange Pi视觉/决策/安全状态→GPIO/PWM→舵机与电机驱动器，不安装Arduino，不使用板间串口 / Changed the current chain to camera→Orange Pi vision/decision/safety state→GPIO/PWM→servo and motor driver, with no Arduino or inter-board serial link.
- 新增 `orange_pi_gpio.py` 和默认 `enabled=false`、映射为 `-1` 的 `gpio_config.example.json`，防止未知引脚误动作 / Added `orange_pi_gpio.py` and a `gpio_config.example.json` with `enabled=false` and `-1` mappings to prevent movement from unknown pins.
- 视觉程序改为同进程调用GPIO输出层，加入物理按钮、限幅、方向切换前归零、250 ms控制更新看门狗、异常/退出清理 / Updated vision to call the GPIO output layer in-process, adding a physical button, limits, zero-before-direction-change, a 250 ms control-update watchdog and exception/exit cleanup.
- 重写现行接线图、软件架构、测试G-01至G-10、复现指南、FMEA、评分证据和工程日志，Arduino内容仅保留为明确的上一版本历史 / Rebuilt the current wiring, software architecture, G-01 through G-10 tests, reproduction guide, FMEA, scoring evidence and engineering log; Arduino remains only as clearly labelled previous-version history.
- 明确真实GPIO line与PWM chip/channel必须由冻结镜像、设备树、排针和枚举结果确认，未填写推测值 / Required real GPIO lines and PWM chip/channels to be confirmed from the frozen image, device tree, header and enumeration; no guessed values were entered.
- 明确进程看门狗不能保证覆盖Linux/PWM整体冻结，增加故障注入和独立硬件使能保护决策项 / Documented that a process watchdog cannot guarantee coverage of a complete Linux/PWM freeze and added fault-injection and independent-hardware-enable decision items.
- 本轮只更新工作区，未暂存、提交或推送 / Updated the working tree only; nothing was staged, committed or pushed.
