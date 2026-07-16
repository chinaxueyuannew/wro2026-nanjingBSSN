# 车辆驾驶演示视频 Vehicle Driving Demonstration

**当前方案 / Current approach:** 视频对应的车辆以USB摄像头视觉作为唯一环境感知。The demonstrated vehicle uses USB-camera vision as its only environmental sensing method.

## 正式视频链接

**视频标题 / Title:** 2026 WRO Future Engineers | 南京博颂学校 BONA SONORITY SCHOOL NANJING | Autonomous Driving Demonstration

**YouTube URL:** <https://youtu.be/DJcxiJCEFdo>

**链接状态：** 已于 2026-07-15 验证，可正常打开并显示上述标题。最终提交前再次用未登录浏览器确认公开或“不公开列出”访问权限。

[![观看南京博颂学校WRO自动驾驶演示](https://img.youtube.com/vi/DJcxiJCEFdo/hqdefault.jpg)](https://youtu.be/DJcxiJCEFdo)

点击缩略图即可在 YouTube 观看。

## 本地演示文件

仓库中已加入 `南京博颂学校未来工程师1.0演视视频.mp4`，检查结果为：

| 项目 | 检查值 |
|---|---:|
| 时长 | 106.812秒（约1分47秒） |
| 画面 | 1920×1080，30 FPS，H.264 |
| 音频 | AAC |
| 大小 | 91,299,421字节（87.07 MiB） |

该压缩版本已经进入Git记录并低于普通Git单文件100 MB限制。比赛公开观看仍以YouTube链接为准；未压缩原片应另外备份，不要再加入仓库。

## 视频必须展示

- 最终参赛车辆与仓库照片一致；
- 独立启动按钮启动，启动前车辆保持停止；
- 连续自动驾驶片段不少于规则要求的时长；
- 完整展示视觉直线、转弯、赛道循迹和安全停车；
- 若作为障碍挑战证明，应展示红绿障碍物的合规处理；
- 视频无剪切到无法判断是否人工干预的程度；
- 链接为公开或任何持有链接者可访问。

## 对应版本记录

| 项目 | 内容 |
|---|---|
| 学校/队伍 School/Team | 南京博颂学校 / BONA SONORITY SCHOOL NANJING |
| YouTube视频ID | `DJcxiJCEFdo` |
| 拍摄日期 | 待填写 |
| Git 提交号 | 待填写 |
| 视觉程序 | `src源代码/bev_segmentation.py`（是否为视频版本待确认） |
| 驱动器 | AT8236 / DRV8701，二选一 |
| 高层计算机 | Orange Pi Zero 3W 4GB |
| 底层控制器 | UNO / ESP32，最终版本待确认 |
| 电池电压 | 待填写 |
| 速度参数 | 待填写 |
| 视觉参数 | 相机模式、ROI、HSV、道路/信标权重、最大转向待填写 |
| 其他距离/速度传感器 | 当前不使用超声波和编码器 |
| 场地配置 | 待填写 |
| 连续成功回合 | 待填写 |

记录视频对应的提交号能证明演示行为与仓库代码一致，避免后续参数更新造成无法复现。
