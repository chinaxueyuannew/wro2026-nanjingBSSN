# 团队介绍 / Team Profile

## 学校与队伍 / School and Team

**中文：** 我们来自南京博颂学校，参加 WRO Future Engineers（未来工程师）项目。团队以阿克曼无人驾驶车辆为工程平台，当前使用 USB 彩色摄像头和 Orange Pi 进行视觉感知与决策，并通过 Arduino 执行转向和电机控制。

**English:** We are the Future Engineers team from **BONA SONORITY SCHOOL NANJING**. Our engineering platform is an autonomous Ackermann-steering vehicle. The current vehicle uses a USB colour camera and an Orange Pi for vision and decision-making, while an Arduino executes steering and motor commands.

- 学校中文名 / Chinese school name：**南京博颂学校**
- 学校英文名 / English school name：**BONA SONORITY SCHOOL NANJING**
- 参赛组别 / Category：**WRO Future Engineers / 未来工程师**
- 当前感知方案 / Current perception：**USB摄像头视觉 / USB camera vision only**

## 学校队旗 / School Flag

[![南京博颂学校队旗 / Bona Sonority School Nanjing flag](../t-photos团队照片/team-flag.jpg)](../t-photos团队照片/team-flag.jpg)

**中文：** 队旗使用深蓝色背景、白色学校标志，并同时展示“南京博颂学校”和“BONA SONORITY SCHOOL NANJING”。比赛现场合影中的队旗与本文件一致。

**English:** The team flag uses a dark-blue background and the white school emblem, together with the names “南京博颂学校” and “BONA SONORITY SCHOOL NANJING”. The same flag appears in the team's competition photographs.

## 团队成员 / Team Members

| 姓名 Name | 分工 Role | 主要职责 Main Responsibilities |
|---|---|---|
| 陆昭颖 / Lu Zhaoying | 程序 / Programming | Orange Pi视觉程序、道路与红绿障碍识别、参数调试、串口协议、软件测试与日志 / Orange Pi vision, road and red/green obstacle detection, parameter tuning, serial protocol, software tests and logs |
| 张隽泽 / Zhang Junze | 结构 / Mechanical Structure | 阿克曼底盘、层板与摄像头支架、机械装配、尺寸复核、转向限位与CAD资料 / Ackermann chassis, plates and camera mount, mechanical assembly, dimensional checks, steering limits and CAD records |
| 黄鸣博 / Huang Mingbo | 电子 / Electronics | 电源与配电、Arduino执行控制、电机驱动、舵机与线束、共地和上电安全检查 / Power distribution, Arduino execution control, motor driver, steering servo and wiring, common ground and power-on safety checks |
| 薛源 / Xue Yuan | 教练 / Coach | 项目指导、安全审查、测试计划、技术文档和比赛准备 / Project guidance, safety review, test planning, technical documentation and competition preparation |

## 成员照片 / Member Portraits

| 成员 Member | 照片 Portrait | 介绍 Profile |
|---|---|---|
| **陆昭颖 / Lu Zhaoying** | [![陆昭颖正式照片 / Formal portrait of Lu Zhaoying](../t-photos团队照片/陆昭颖.jpg)](../t-photos团队照片/陆昭颖.jpg) | **程序 / Programming**：负责Orange Pi视觉程序、道路与障碍识别、串口协议、参数调试和软件测试。 / Responsible for Orange Pi vision, road and obstacle detection, serial communication, parameter tuning and software testing. |
| **张隽泽 / Zhang Junze** | [![张隽泽正式照片 / Formal portrait of Zhang Junze](../t-photos团队照片/张隽泽.jpg)](../t-photos团队照片/张隽泽.jpg) | **结构 / Mechanical Structure**：负责阿克曼底盘、摄像头支架、机械装配、尺寸复核和转向限位。 / Responsible for the Ackermann chassis, camera mount, mechanical assembly, dimensional verification and steering limits. |
| **黄鸣博 / Huang Mingbo** | [![黄鸣博正式照片 / Formal portrait of Huang Mingbo](../t-photos团队照片/黄鸣博.jpg)](../t-photos团队照片/黄鸣博.jpg) | **电子 / Electronics**：负责供电、Arduino执行控制、电机驱动、舵机、线束和上电安全。 / Responsible for power, Arduino execution control, motor driver, steering servo, wiring and power-on safety. |

### 陆昭颖形象照 / Additional Portrait of Lu Zhaoying

[![陆昭颖形象照 / Additional portrait of Lu Zhaoying](../t-photos团队照片/陆昭颖形象照.jpg)](../t-photos团队照片/陆昭颖形象照.jpg)

**中文：** 此照片作为成员形象补充展示；正式成员识别与资料索引优先使用上方白底证件照。

**English:** This photograph is included as an additional team-member portrait. The formal white-background portrait above remains the primary identification image in the documentation.

## 协作方式 / Collaboration

**中文：** 程序、结构和电子三部分通过统一接口协作。结构组保证摄像头和控制器安装可重复；电子组保证供电、串口和执行器可靠；程序组根据固定的摄像头位置完成视觉标定并输出转向/速度目标。每次更改机械位置、接线或软件参数后，团队都应重新完成抬轮检查、低速测试和故障停车测试。

**English:** Programming, mechanical structure and electronics are connected through defined interfaces. The mechanical role keeps the camera and controllers repeatably mounted; the electronics role provides reliable power, serial communication and actuator wiring; the programming role calibrates vision for the fixed camera position and produces steering/speed targets. After any mechanical, wiring or software change, the team repeats the lifted-wheel check, low-speed test and failure-stop test.

## 相关资料 / Related Materials

- [正式团队照 / Official team photograph](../t-photos团队照片/team-official.jpg)
- [北京站冠军领奖照 / Beijing championship award photograph](../t-photos团队照片/award-beijing-champion.jpg)
- [制作过程照片 / Development process photographs](../t-photos团队照片/README.md)
- [车辆比赛现场 / Vehicle on the competition field](../v-photos车辆照片/vehicle-competition-run.jpg)
- [工程研发日志 / Engineering log](engineering-log.md)
