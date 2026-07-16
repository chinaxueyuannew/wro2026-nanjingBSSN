#!/usr/bin/env python3
"""Build the bilingual archival engineering log required by the 2026 rubric.

Run from any directory:
    python other其他/build_engineering_log_pdf.py

The generated PDF is intentionally evidence-led. Unknown hardware values and
unperformed measurements remain explicitly marked as pending.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).with_name("engineering-log.pdf")
WIRING_IMAGE = ROOT / "schemes原理图" / "system-wiring.png"
TEAM_FLAG = ROOT / "t-photos团队照片" / "team-flag.jpg"
TEAM_PHOTO = ROOT / "t-photos团队照片" / "team-official.jpg"
VEHICLE_PHOTO = ROOT / "v-photos车辆照片" / "vehicle-competition-run.jpg"
LU_PORTRAIT = ROOT / "t-photos团队照片" / "陆昭颖.jpg"
ZHANG_PORTRAIT = ROOT / "t-photos团队照片" / "张隽泽.jpg"
HUANG_PORTRAIT = ROOT / "t-photos团队照片" / "黄鸣博.jpg"

PAGE_W, PAGE_H = A4
MARGIN_X = 1.65 * cm
MARGIN_TOP = 1.65 * cm
MARGIN_BOTTOM = 1.55 * cm

FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("Deng", str(FONT_DIR / "Deng.ttf")))
pdfmetrics.registerFont(TTFont("DengBold", str(FONT_DIR / "Dengb.ttf")))
pdfmetrics.registerFontFamily(
    "Deng", normal="Deng", bold="DengBold", italic="Deng", boldItalic="DengBold"
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CNTitle", fontName="DengBold", fontSize=23, leading=31,
    alignment=TA_CENTER, textColor=colors.HexColor("#102A43"), spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="CNSubTitle", fontName="Deng", fontSize=13, leading=20,
    alignment=TA_CENTER, textColor=colors.HexColor("#334E68"), spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H1CN", fontName="DengBold", fontSize=17, leading=23,
    textColor=colors.HexColor("#17375E"), spaceBefore=9, spaceAfter=7, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H2CN", fontName="DengBold", fontSize=12.5, leading=18,
    textColor=colors.HexColor("#1F5A92"), spaceBefore=7, spaceAfter=5, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="BodyCN", fontName="Deng", fontSize=9.3, leading=14.3,
    textColor=colors.HexColor("#243B53"), alignment=TA_LEFT, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="SmallCN", fontName="Deng", fontSize=7.8, leading=11.5,
    textColor=colors.HexColor("#486581"), spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="CaptionCN", fontName="Deng", fontSize=7.8, leading=11.5,
    textColor=colors.HexColor("#486581"), alignment=TA_CENTER, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="CalloutCN", fontName="Deng", fontSize=9, leading=14,
    textColor=colors.HexColor("#7A3E00"), backColor=colors.HexColor("#FFF7E6"),
    borderColor=colors.HexColor("#F0A040"), borderWidth=0.7, borderPadding=7,
    spaceBefore=5, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="CellCN", fontName="Deng", fontSize=7.4, leading=10.5,
    textColor=colors.HexColor("#243B53"),
))
styles.add(ParagraphStyle(
    name="CellHeadCN", fontName="DengBold", fontSize=7.6, leading=10.7,
    textColor=colors.white, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="CodeCN", fontName="Courier", fontSize=8.2, leading=12,
    textColor=colors.HexColor("#102A43"), backColor=colors.HexColor("#EAF2F8"),
    borderPadding=5, spaceAfter=5,
))


def p(text, style="BodyCN"):
    return Paragraph(text, styles[style])


def bilingual(zh, en, style="BodyCN"):
    return [KeepTogether([
        p(f"<b>中文：</b>{zh}", style),
        p(f"<b>English:</b> {en}", style),
    ])]


def heading(number, zh, en):
    return p(f"{number} {zh} / {en}", "H1CN")


def subheading(number, zh, en):
    return p(f"{number} {zh} / {en}", "H2CN")


def cell(text, head=False):
    return Paragraph(str(text), styles["CellHeadCN" if head else "CellCN"])


def table(rows, widths, repeat=1, header=True, padd=5):
    processed = []
    for r_idx, row in enumerate(rows):
        processed.append([cell(v, head=(header and r_idx == 0)) for v in row])
    t = Table(processed, colWidths=widths, repeatRows=repeat if header else 0, hAlign="LEFT")
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), "Deng"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#9FB3C8")),
        ("LEFTPADDING", (0, 0), (-1, -1), padd),
        ("RIGHTPADDING", (0, 0), (-1, -1), padd),
        ("TOPPADDING", (0, 0), (-1, -1), padd),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padd),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17375E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ]
        if len(rows) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FA")]))
    t.setStyle(TableStyle(commands))
    return t


def fit_image(path, max_w, max_h):
    img = Image(str(path))
    scale = min(max_w / img.imageWidth, max_h / img.imageHeight)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    img.hAlign = "CENTER"
    return img


def page_decor(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#BCCCDC"))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_X, PAGE_H - 1.12 * cm, PAGE_W - MARGIN_X, PAGE_H - 1.12 * cm)
        canvas.setFont("Deng", 7.6)
        canvas.setFillColor(colors.HexColor("#486581"))
        canvas.drawString(MARGIN_X, PAGE_H - 0.88 * cm, "南京博颂学校 / BONA SONORITY SCHOOL NANJING")
        canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 0.88 * cm, "2026 WRO Future Engineers")
    canvas.setStrokeColor(colors.HexColor("#BCCCDC"))
    canvas.line(MARGIN_X, 1.03 * cm, PAGE_W - MARGIN_X, 1.03 * cm)
    canvas.setFont("Deng", 7.5)
    canvas.setFillColor(colors.HexColor("#486581"))
    canvas.drawString(MARGIN_X, 0.67 * cm, "双语工程研发日志 / Bilingual Engineering Log")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.67 * cm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
    title="南京博颂学校 2026 WRO Future Engineers 双语工程研发日志",
    author="BONA SONORITY SCHOOL NANJING",
    subject="2026 WRO Future Engineers engineering process, architecture, tests and evidence",
)
frame = Frame(
    MARGIN_X, MARGIN_BOTTOM, PAGE_W - 2 * MARGIN_X, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
    id="normal", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
)
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_decor)])

story = []

# Cover
story += [Spacer(1, 0.65 * cm)]
if TEAM_FLAG.exists():
    story += [fit_image(TEAM_FLAG, 12.5 * cm, 5.3 * cm), Spacer(1, 0.35 * cm)]
story += [
    p("2026 WRO Future Engineers", "CNTitle"),
    p("结构化工程研发日志 / Structured Engineering Log", "CNTitle"),
    Spacer(1, 0.18 * cm),
    p("南京博颂学校 / BONA SONORITY SCHOOL NANJING", "CNSubTitle"),
    p("陆昭颖（程序） · 张隽泽（结构） · 黄鸣博（电子） · 薛源（教练）", "CNSubTitle"),
    p("Lu Zhaoying (Programming) · Zhang Junze (Mechanical) · Huang Mingbo (Electronics) · Xue Yuan (Coach)", "CNSubTitle"),
    Spacer(1, 0.35 * cm),
    p("版本 / Version: Documentation Audit 2026-07-16", "CNSubTitle"),
    p("GitHub: https://github.com/chinaxueyuannew/wro2026-nanjingBSSN", "SmallCN"),
    p("YouTube: https://youtu.be/DJcxiJCEFdo", "SmallCN"),
    Spacer(1, 0.35 * cm),
    p(
        "状态声明 / Status statement: 当前架构为USB彩色摄像头 + Orange Pi视觉/决策 + GPIO/PWM直接执行；不安装Arduino，不使用超声波或编码器反馈。"
        "文档中所有待测字段保持空缺，不以推测数据冒充实测。 / The current architecture is USB colour camera + Orange Pi vision/decisions + direct GPIO/PWM execution; no Arduino, ultrasonic or encoder feedback is used. Every pending measurement remains explicit and is never replaced by assumed data.",
        "CalloutCN",
    ),
]
story.append(PageBreak())

# Team page
story += [heading("", "参赛团队", "Competition Team")]
story += bilingual(
    "南京博颂学校队伍由三名学生和一名教练组成。程序、结构和电子采用明确接口协作，每名成员同时参与联调、风险复核和比赛准备。",
    "The BONA SONORITY SCHOOL NANJING team consists of three students and one coach. Programming, mechanical structure and electronics collaborate through defined interfaces, while every member also participates in integration, risk review and competition preparation.",
)
if LU_PORTRAIT.exists() and ZHANG_PORTRAIT.exists() and HUANG_PORTRAIT.exists():
    portrait_table = Table([
        [fit_image(LU_PORTRAIT, 4.7 * cm, 6.1 * cm), fit_image(ZHANG_PORTRAIT, 4.7 * cm, 6.1 * cm), fit_image(HUANG_PORTRAIT, 4.7 * cm, 6.1 * cm)],
        [cell("陆昭颖 / Lu Zhaoying<br/><b>程序 / Programming</b>"), cell("张隽泽 / Zhang Junze<br/><b>结构 / Mechanical</b>"), cell("黄鸣博 / Huang Mingbo<br/><b>电子 / Electronics</b>")],
        [cell("视觉、算法、GPIO控制、参数与软件测试 / Vision, algorithms, GPIO control, parameters and software tests"), cell("底盘、支架、装配、尺寸与转向复核 / Chassis, mounts, assembly, dimensions and steering review"), cell("供电、GPIO/PWM接口、驱动器、舵机、线束与上电安全 / Power, GPIO/PWM interfaces, driver, servo, wiring and power-on safety")],
    ], colWidths=[5.6 * cm, 5.6 * cm, 5.6 * cm], hAlign="CENTER")
    portrait_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#9FB3C8")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EAF2F8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [portrait_table, Spacer(1, 0.28 * cm)]
story += [p("教练 / Coach：薛源 / Xue Yuan——项目指导、安全审查、测试计划、技术文档与比赛准备 / Project guidance, safety review, test planning, technical documentation and competition preparation.", "CalloutCN")]
if TEAM_PHOTO.exists():
    story += [KeepTogether([
        fit_image(TEAM_PHOTO, 13.8 * cm, 6.2 * cm),
        p("正式团队照 / Official team photograph", "CaptionCN"),
    ])]
story.append(PageBreak())

# Contents and executive summary
story += [heading("0.", "阅读指南", "Reading Guide")]
story += bilingual(
    "本日志与GitHub仓库共同记录研发过程、设计选择、风险、测试和复现方法。裁判可先阅读本页和第2节证据矩阵，再按五个评分维度跳转到详细章节。",
    "This log and the GitHub repository jointly record the development process, design choices, risks, tests and reproduction method. Judges may begin with this page and the Section 2 evidence matrix, then inspect the five rubric dimensions.",
)
toc_rows = [
    ["章节 / Section", "内容 / Content"],
    ["1", "项目摘要与当前边界 / Project summary and current boundaries"],
    ["2", "2026规则五维证据矩阵 / Five-dimension rule evidence matrix"],
    ["3", "系统架构与接口 / System architecture and interfaces"],
    ["4", "工程研发阶段 / Engineering development stages"],
    ["5", "移动性能与机械设计 / Mobility and mechanical design"],
    ["6", "动力与纯视觉传感架构 / Power and vision-only sensing"],
    ["7", "软件、状态机与障碍策略 / Software, state machine and obstacle strategy"],
    ["8", "系统思维、取舍与风险 / Systems thinking, trade-offs and risk"],
    ["9", "测试、指标与迭代 / Tests, metrics and iteration"],
    ["10", "可复现性、提交与证据缺口 / Reproducibility, commits and evidence gaps"],
    ["11", "最终签署 / Final sign-off"],
]
story += [table(toc_rows, [3.2 * cm, 13.6 * cm]), Spacer(1, 0.25 * cm)]
story += [p(
    "重要 / Important: 本PDF展示当前可核验证据与明确计划，不能单独证明车辆已经通过全部实车测试。最终提交前必须把原始照片、测量记录、日志和对应Git提交补入仓库，并重新生成本PDF。 / This PDF presents current verifiable evidence and explicit plans; it does not by itself prove full vehicle validation. Before final submission, add raw photographs, measurements, logs and matching commits, then rebuild this PDF.",
    "CalloutCN",
)]

story += [heading("1.", "项目摘要与当前边界", "Project Summary and Current Boundaries")]
story += bilingual(
    "车辆以阿克曼四轮驱动底盘为机械基础。USB彩色摄像头是唯一环境传感器；Orange Pi Zero 3W 4GB在同一平台上完成视觉、路径决策、安全状态和GPIO/PWM执行，直接控制转向舵机与PWM/DIR电机驱动器。当前不安装Arduino。",
    "The vehicle uses a four-wheel-drive Ackermann chassis. A USB colour camera is the only environmental sensor; an Orange Pi Zero 3W 4GB performs vision, path decisions, safety state and GPIO/PWM execution on the same platform, directly controlling the steering servo and PWM/DIR motor driver. No Arduino is currently installed.",
)
summary_rows = [
    ["子系统 / Subsystem", "当前实现 / Current Implementation", "验证边界 / Validation Boundary"],
    ["机械 / Mechanical", "阿克曼前轮转向、四轮机械驱动、前后差速 / Ackermann front steering, mechanical 4WD, front/rear differentials", "装车尺寸、质量、舵角和半径待测 / Final dimensions, mass, angles and radii pending"],
    ["感知 / Perception", "160°广角、480p、30 FPS USB彩色摄像头 / 160° wide-angle, 480p, 30 FPS USB colour camera", "内参、畸变、位姿和识别指标待测 / Intrinsics, distortion, pose and metrics pending"],
    ["计算 / Compute", "Orange Pi Zero 3W 4GB；CPU/OpenCV基线 / Orange Pi Zero 3W 4GB; CPU/OpenCV baseline", "板端版本、温度、延迟和镜像校验待冻结 / Board versions, temperature, latency and image checksum pending"],
    ["执行 / Execution", "Orange Pi GPIO方向/按钮 + 内核PWM速度/舵机；默认禁用 / Orange Pi GPIO direction/button + kernel PWM speed/steering; disabled by default", "真实line/channel、波形、驱动接口和机械限位待核 / Real line/channel, waveforms, driver interface and limits pending"],
    ["安全 / Safety", "上电停车、物理启动、输出限幅、方向切换前归零、250 ms进程看门狗 / Power-on stop, physical arm, limits, zero-before-direction-change and 250 ms process watchdog", "实际停车时间、Linux/PWM冻结边界、独立硬件保护和最坏停车距离待测 / Stop timing, Linux/PWM freeze boundary, hardware fail-safe and worst stopping distance pending"],
]
story += [table(summary_rows, [2.65 * cm, 7.2 * cm, 6.95 * cm])]

if TEAM_PHOTO.exists() and VEHICLE_PHOTO.exists():
    story += [Spacer(1, 0.25 * cm)]
    photos = Table([
        [fit_image(TEAM_PHOTO, 7.8 * cm, 4.6 * cm), fit_image(VEHICLE_PHOTO, 7.8 * cm, 4.6 * cm)],
        [cell("正式团队照 / Official team photograph"), cell("比赛现场车辆 / Vehicle on competition field")],
    ], colWidths=[8.4 * cm, 8.4 * cm])
    photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(photos)

# Rubric matrix
story += [heading("2.", "2026规则五维证据矩阵", "2026 Five-Dimension Rule Evidence Matrix")]
story += bilingual(
    "每个维度最高6分。下表中的“目标证据”来自规则附录C的高级工程实践要求；“当前状态”只描述仓库可见材料，不预测最终得分。",
    "Each dimension is worth up to 6 points. The target evidence below follows the advanced-practice criteria in Appendix C. Current status describes visible repository evidence and does not predict a final score.",
)
rubric_rows = [
    ["维度 / Dimension", "当前证据 / Current Evidence", "6分目标证据 / Target Evidence for 6"],
    ["1 移动与机械 / Mobility and mechanical", "阿克曼选型、几何/速度公式、层板DXF、机械测试表 / Rationale, geometry/speed formulas, plate DXF and test tables", "扭矩/速度实测、左右半径、刚度/稳定性、改动前后数据 / Measured torque/speed, left/right radii, stiffness/stability and before/after data"],
    ["2 动力与传感 / Power and sensing", "分支供电、正式接线图、视觉选型、标定与FMEA / Branch power, formal wiring, vision rationale, calibration and FMEA", "准确型号、电流预算、相机位姿/标定、光影/断连故障结果 / Exact models, current budget, camera pose/calibration and lighting/disconnection results"],
    ["3 软件与障碍 / Software and obstacles", "视觉模块、恢复逻辑、GPIO安全状态机、默认禁用、250 ms看门狗 / Vision modules, recovery, GPIO safety state, disabled default and 250 ms watchdog", "真实GPIO/PWM映射、停车/圈数、识别/延迟/FPS、冻结边界和连续回合 / Real mapping, parking/laps, recognition/latency/FPS, freeze boundary and consecutive laps"],
    ["4 系统与决策 / Systems and decisions", "高低层分工、约束、方案取舍、FMEA、阶段日志 / Layer roles, constraints, trade-offs, FMEA and staged log", "至少3条由实测支撑的X/Y选择与迭代影响 / At least three measured X/Y decisions and quantified iteration effects"],
    ["5 可复现与GitHub / Reproducibility and GitHub", "官方模板结构、README>5000字符、代码/DXF/接线/测试/日志 / Official structure, README >5,000, code/DXF/wiring/tests/log", "3+有效提交、六视图、最终CAD、镜像校验、独立复现 / 3+ meaningful commits, six views, final CAD, image checksum and independent reproduction"],
]
story += [table(rubric_rows, [3.0 * cm, 6.9 * cm, 6.9 * cm])]

story += [subheading("2.1", "裁判快速路径", "Judge-Facing Quick Path")]
quick_rows = [
    ["要看什么 / Evidence", "仓库入口 / Repository Entry"],
    ["总览、视频和团队 / Overview, video and team", "README.md"],
    ["评分证据 / Rubric evidence", "other其他/scoring-evidence.md"],
    ["机械与计算 / Mechanics and calculations", "other其他/mechanical-analysis.md + models模型/"],
    ["正式电路图 / Formal wiring", "schemes原理图/system-wiring.png + wiring.md"],
    ["视觉与执行代码 / Vision and executor code", "src源代码/bev_segmentation.py + orange_pi_gpio.py"],
    ["测试、FMEA和标定 / Tests, FMEA and calibration", "other其他/tests.md + FMEA.md + calibration-guide.md"],
    ["缺失证据 / Missing evidence", "other其他/evidence-register.md"],
]
story += [table(quick_rows, [5.0 * cm, 11.8 * cm])]

# Architecture
story += [heading("3.", "系统架构与接口", "System Architecture and Interfaces")]
story += bilingual(
    "当前采用单板分层：Orange Pi上的视觉与决策层只产生逻辑目标，集中式GPIO安全输出层执行限幅、物理授权、PWM/DIR、250 ms控制更新看门狗和退出清理。该方案减少控制器和板间协议，但视觉与执行共享故障域。",
    "The current single-board design is layered: vision and decision code produces logical targets, while a central GPIO safety-output layer owns limits, physical arming, PWM/DIR, a 250 ms control-update watchdog and exit cleanup. This reduces controllers and inter-board protocol, but vision and execution share one fault domain.",
)
if WIRING_IMAGE.exists():
    story += [fit_image(WIRING_IMAGE, 17.0 * cm, 12.3 * cm), p("图1 / Figure 1. 当前纯视觉系统候选接线；所有待核字段必须由实物闭环。 / Current vision-only candidate wiring; every pending field requires physical closure.", "SmallCN")]

story += [subheading("3.1", "GPIO/PWM执行契约", "GPIO/PWM Execution Contract")]
story += [p("set_control(steer, speed)    # -100...100", "CodeCN")]
contract_rows = [
    ["属性 / Property", "当前定义 / Current Definition", "工程含义 / Engineering Meaning"],
    ["范围 / Range", "同进程逻辑量-100...100 / In-process logical values -100...100", "输出层二次限幅 / Output layer applies final bounds"],
    ["周期 / Period", "约50 ms / Approximately 50 ms", "约20 Hz控制更新；单调时钟记录年龄 / Approximately 20 Hz; monotonic control age"],
    ["超时 / Timeout", "250 ms", "电机PWM=0、舵机回中、进入CONTROL_FAILSAFE / Zero motor PWM, centre steering, enter CONTROL_FAILSAFE"],
    ["启动 / Arming", "外部上拉常开按钮，GPIO映射待冻结 / External-pull-up NO button; mapping pending", "上电和故障后都需要物理动作 / Physical action required after power-up and fault"],
    ["边界 / Boundary", "进程线程，不是硬件看门狗 / Process thread, not a hardware watchdog", "Linux/PWM整体冻结需独立硬件保护评估 / Linux/PWM freeze needs hardware-fail-safe assessment"],
]
story += [table(contract_rows, [3.0 * cm, 6.3 * cm, 7.5 * cm])]

story += [subheading("3.2", "安全状态机", "Safety State Machine")]
state_rows = [
    ["状态 / State", "进入 / Entry", "动作 / Action", "退出 / Exit"],
    ["DRY_RUN", "enabled=false", "不打开GPIO/PWM，只显示请求值 / Open no GPIO/PWM; report requested values", "核验配置后人工启用 / Enable after verification"],
    ["WAIT_START", "硬件打开或物理停车 / Hardware opened or physical stop", "电机0、舵机中位 / Motor zero, steering centre", "去抖后的物理按键 / Debounced physical arm"],
    ["GPIO_DRIVE", "已授权且有新鲜更新 / Armed with fresh update", "执行限幅GPIO/PWM / Execute bounded GPIO/PWM", "按钮、异常或250 ms超时 / Button, exception or 250 ms timeout"],
    ["CONTROL_FAILSAFE", "控制更新超时 / Control-update timeout", "电机0、舵机中位、不自动恢复 / Motor zero, centre, no auto-recovery", "物理重新授权 / Physical re-arm"],
]
story += [table(state_rows, [3.1 * cm, 4.4 * cm, 5.6 * cm, 3.7 * cm])]

# Development stages
story += [heading("4.", "工程研发阶段", "Engineering Development Stages")]
stages = [
    ("1", "仓库建立", "Repository setup", "按官方Future Engineers模板建立模型、其他、原理图、源码、团队照片、车辆照片和视频入口。", "Created models, other, schemes, source, team-photo, vehicle-photo and video entries using the official Future Engineers structure."),
    ("2", "超声波巡墙基线", "Ultrasonic wall-follow baseline", "早期以右侧/前方超声波验证底盘、电机和舵机方向；控制简单但不能处理颜色，当前不使用。", "An early right/front ultrasonic baseline verified chassis, motor and servo directions; it could not handle colour and is not currently used."),
    ("3", "编码器与驱动试验", "Encoder and driver experiments", "团队完成双PWM、PWM/DIR和编码器PI试验程序，用于理解接口和闭环；当前车辆不连接编码器。", "The team developed dual-PWM, PWM/DIR and encoder-PI experiments to understand interfaces and feedback; the current vehicle does not connect encoders."),
    ("4", "阿克曼机械资料", "Ackermann mechanical record", "整理底盘尺寸、轴距、轮距、轮径、传动与层板DXF，并区分现有规格记录和装车待测值。", "Recorded chassis dimensions, wheelbase, track, wheel diameter, drivetrain and plate DXF, separating existing specification records from assembled measurements."),
    ("5", "车载视觉计算", "Onboard vision compute", "当时建立Orange Pi视觉 + Arduino执行试验分层，使用USB摄像头、有线串口和独立5 V支路；阶段13已替代该方案。", "At that stage, established experimental Orange Pi vision + Arduino execution using a USB camera, wired serial and independent 5 V branch; Stage 13 later replaced it."),
    ("6", "视觉原型", "Vision prototype", "加入道路预处理和红绿分割，完成默认停车、丢源/退出停车和恢复阶段修正。", "Added road preprocessing and red-green segmentation, correcting default stop, source-loss/exit stop and recovery behaviour."),
    ("7", "照片与赛事证据", "Photographs and competition evidence", "整理制作过程、三名成员、正式团队、赛事和比赛车辆照片，并明确趣味团队照和六视图缺口。", "Indexed development, all three member portraits, official team, competition and vehicle photographs and identified the missing informal team photograph and six views."),
    ("8", "纯视觉范围冻结", "Vision-only scope freeze", "明确当前不安装超声波、不读取编码器，避免历史代码与当前配置混淆。", "Defined no ultrasonic installation and no encoder reading to prevent historical code from being confused with current configuration."),
    ("9", "团队职责", "Team responsibilities", "明确程序、结构、电子和教练职责以及接口复核流程。", "Defined programming, mechanical, electronics and coach responsibilities and interface review flow."),
    ("10", "中英对照与导航", "Bilingual documentation and navigation", "统一同页中英对照，建立首页、目录和跨文件跳转。", "Standardised same-page Chinese-English presentation and built landing-page, index and cross-file navigation."),
    ("11", "上一版规则复核", "Previous-version rule audit", "发现当时的视觉文本协议无匹配执行端，新增D2/D6/D7/D8 Arduino串口候选、250 ms看门狗和接线图；现仅作上一版本记录。", "Found that the previous-stage visual text protocol lacked a matching executor and added a D2/D6/D7/D8 Arduino serial candidate, 250 ms watchdog and wiring; now retained only as previous-version history."),
    ("12", "上一版UNO编译", "Previous-version UNO build", "完成上一版UNO目标编译：5544 bytes程序空间、277 bytes全局变量；该结果不代表当前装车。", "Built the previous-version UNO target using 5,544 bytes of program storage and 277 bytes of global memory; this does not represent the current vehicle."),
    ("13", "Orange Pi GPIO/PWM直控", "Direct Orange Pi GPIO/PWM", "当前链路改为摄像头→Orange Pi视觉/决策/安全状态→GPIO/PWM→执行器；新增默认禁用配置、物理按钮、方向切换前归零和250 ms控制更新看门狗。真实line/channel待冻结，Linux/PWM冻结需独立硬件保护评估。", "Changed the current chain to camera→Orange Pi vision/decision/safety state→GPIO/PWM→actuators; added disabled defaults, physical arming, zero-before-direction-change and a 250 ms control-update watchdog. Real line/channels require freezing, and Linux/PWM freezes require an independent-hardware-fail-safe assessment."),
]
for num, zh_title, en_title, zh, en in stages:
    story.append(KeepTogether([
        subheading(f"4.{num}", zh_title, en_title),
        p(f"<b>中文：</b>{zh}<br/><b>English:</b> {en}", "BodyCN"),
    ]))

# Mechanics
story += [heading("5.", "移动性能与机械设计", "Mobility and Mechanical Design")]
story += bilingual(
    "阿克曼转向相较差速滑移转向，能够让内外前轮沿不同半径滚动，降低轮胎横向擦滑并提高直线稳定性。代价是机构、间隙、左右对称性和标定更敏感。前后差速器允许转弯时各轮速度不同，中央传动轴实现机械四驱。",
    "Compared with skid steering, Ackermann geometry lets the inner and outer front wheels roll along different radii, reducing lateral tyre scrub and improving straight stability. The cost is greater sensitivity to mechanism, play, left/right symmetry and calibration. Front and rear differentials permit different wheel speeds in turns, while the central shaft provides mechanical four-wheel drive.",
)
mechanical_rows = [
    ["参数 / Parameter", "现有记录 / Recorded Value", "证据类型 / Evidence Type", "最终要求 / Final Requirement"],
    ["底盘外形 / Base size", "260×140×85 mm；去防撞棉约246 mm / 260×140×85 mm; ~246 mm without foam", "现有规格资料 / Existing specification record", "装车后实测并拍照 / Measure assembled vehicle with photo"],
    ["轴距 / Wheelbase", "174 mm", "现有规格资料 / Existing record", "卡尺/钢尺复核 / Verify by measurement"],
    ["轮距 / Track", "123 mm", "现有规格资料 / Existing record", "左右和前后说明 / Record left/right and front/rear"],
    ["轮径 / Wheel diameter", "47 mm", "现有规格资料 / Existing record", "多点测量取均值 / Multi-point average"],
    ["离地间隙 / Ground clearance", "6 mm", "现有规格资料 / Existing record", "最终负载下实测 / Measure at final load"],
    ["质量 / Mass", "基础约0.7 kg / Base ~0.7 kg", "现有规格资料 / Existing record", "整车电子秤实测 / Weigh final vehicle"],
    ["最小转弯半径 / Minimum radius", "标称475 mm / Rated 475 mm", "现有规格资料 / Existing record", "左/右各5次 / Five trials each direction"],
]
story += [table(mechanical_rows, [3.1 * cm, 4.7 * cm, 4.1 * cm, 4.9 * cm])]

story += [subheading("5.1", "计算模型", "Calculation Model")]
story += [
    p("理论车速 / Theoretical speed: v = π × D × n / 60", "CodeCN"),
    p("含齿轮速比时 / With gear ratio: v = π × D × n_motor / (60 × i)", "CodeCN"),
    p("轮端扭矩 / Wheel torque: T_wheel = T_motor × i × η", "CodeCN"),
    p("牵引力 / Tractive force: F = T_wheel / (D/2)", "CodeCN"),
]
story += bilingual(
    "47 mm轮径和1692 rpm换算约4.17 m/s，高于记录中的12 V参考速度3.5 m/s。该差异可能来自空载/负载、转速定义、轮胎变形和传动损失，因此文档保留两者并要求固定距离实测，而不选择性删除不一致数据。",
    "A 47 mm wheel at 1692 rpm converts to approximately 4.17 m/s, above the recorded 3.5 m/s reference at 12 V. The difference may arise from no-load/load conditions, rpm definition, tyre deformation and drivetrain loss. Both values are retained and require fixed-distance measurement rather than selectively deleting the inconsistency.",
)
story += [subheading("5.2", "机械验证与迭代", "Mechanical Validation and Iteration")]
mechanical_test_rows = [
    ["测试 / Test", "方法 / Method", "指标 / Metric", "状态 / Status"],
    ["舵机安全限位 / Safe servo limits", "架空逐度测试 / Lifted incremental test", "无顶死、留机械余量 / No stall, retained margin", "待测 / Pending"],
    ["直线偏差 / Straight deviation", "低速2 m，多次 / Repeated low-speed 2 m", "横向偏差均值/范围 / Mean/range", "待测 / Pending"],
    ["左右半径 / Left/right radii", "同地面同电量各5次 / Five each, same surface/battery", "均值、范围、不对称 / Mean, range, asymmetry", "待测 / Pending"],
    ["速度映射 / Speed mapping", "5+命令固定距离 / 5+ commands over fixed distance", "m/s与停车距离 / m/s and stopping distance", "待测 / Pending"],
    ["结构刚度 / Structural stiffness", "支架扰动前后图像位姿 / Image pose before/after disturbance", "像素/角度漂移 / Pixel/angle drift", "待测 / Pending"],
]
story += [table(mechanical_test_rows, [3.8 * cm, 5.3 * cm, 4.6 * cm, 3.1 * cm])]

# Power and sensing
story += [heading("6.", "动力与纯视觉传感架构", "Power and Vision-Only Sensing")]
story += bilingual(
    "单摄像头方案能同时提取赛道边界、行驶方向和红绿障碍颜色，机械布置简单且信息密度高；但没有独立距离冗余，对光照、反光、遮挡、畸变、掉帧和延迟更加敏感。缓解措施包括固定支架、内参/畸变标定、ROI、曝光/白平衡控制、低置信度降速、进程退出清零和GPIO控制更新看门狗。",
    "A single camera can extract track borders, direction and red-green obstacle colour with a simple mount and high information density. However, it provides no independent ranging redundancy and is more sensitive to lighting, reflections, occlusion, distortion, dropped frames and latency. Mitigations include a rigid mount, intrinsic/distortion calibration, ROI, exposure/white-balance control, low-confidence slowdown, zero-on-exit and a GPIO control-update watchdog.",
)
story += [subheading("6.1", "配电原则", "Power-Distribution Principles")]
power_rows = [
    ["支路 / Branch", "规划 / Plan", "风险 / Risk", "必须验证 / Required Verification"],
    ["电机 / Motor", "电池经总开关/保险到驱动器 / Battery through main switch/fuse to driver", "启动峰值导致压降/噪声 / Start surge causes sag/noise", "峰值电流、电池最低电压、线径、保险 / Peak current, minimum voltage, wire and fuse"],
    ["Orange Pi + camera", "独立稳定5 V/3 A支路 / Independent stable 5 V/3 A branch", "掉压重启、USB断连 / Brownout reboot, USB loss", "视觉工况电流、5 V最小值、温度 / Vision current, 5 V minimum, temperature"],
    ["Steering servo", "独立4.5–7 V支路，不从Orange Pi排针取电 / Separate 4.5–7 V branch; not from Orange Pi header", "舵机峰值干扰控制器 / Servo peaks disturb controller", "左右极限电流、复位、抖动 / Limit current, resets, jitter"],
    ["地与信号 / Ground and signals", "控制共地；大电流回路短且与USB/GPIO分开 / Common ground; short motor return, separated from USB/GPIO", "地弹、GPIO误动作 / Ground bounce, false GPIO action", "布线照片、故障注入 / Harness photos, fault injection"],
]
story += [table(power_rows, [3.0 * cm, 5.4 * cm, 4.1 * cm, 4.3 * cm])]

story += [subheading("6.2", "动力预算方法", "Power-Budget Method")]
story += [p("I_peak = I_motor_start + I_servo_peak + I_orange_pi_camera + I_controller + safety_margin", "CodeCN")]
power_budget_rows = [
    ["负载 / Load", "电压 / Voltage", "典型 / Typical", "峰值 / Peak", "当前状态 / Current Status"],
    ["Orange Pi + camera", "5 V", "待测 / TBD", "设计支路3 A / 3 A branch design", "板端负载测试待做 / Board load test pending"],
    ["转向舵机 / Servo", "4.5–7 V", "记录400–800 mA / Recorded 400–800 mA", "堵转待测 / Stall TBD", "架空极限和温升待测 / Lifted limit and temperature pending"],
    ["驱动电机 / Drive motor", "6–12 V", "记录额定1.9 A / Recorded rated 1.9 A", "启动待测 / Start TBD", "5次峰值测试待做 / Five surge trials pending"],
    ["总计 / Total", "—", "待计算 / TBD", "待计算 + ≥25%余量 / TBD + ≥25% margin", "准确器件和实测后填写 / Fill after exact hardware and measurement"],
]
story += [table(power_budget_rows, [3.8 * cm, 2.2 * cm, 3.5 * cm, 3.5 * cm, 3.8 * cm])]

story += [subheading("6.3", "相机标定证据", "Camera-Calibration Evidence")]
camera_rows = [
    ["项目 / Item", "方法 / Method", "应保存 / Preserve", "状态 / Status"],
    ["UVC模式 / UVC mode", "板端枚举 / Board enumeration", "设备名、VID:PID、分辨率/FPS / Device, VID:PID, modes", "待板端 / Pending"],
    ["内参与畸变 / Intrinsics and distortion", "多姿态棋盘格 / Multi-pose checkerboard", "矩阵、系数、图像数、重投影误差 / Matrix, coefficients, count, reprojection error", "待测 / Pending"],
    ["安装位姿 / Mount pose", "尺与角度工具 / Ruler and angle tool", "高度、俯仰、横向偏置、照片 / Height, pitch, offset, photo", "待测 / Pending"],
    ["曝光与颜色 / Exposure and colour", "场地明/暗/阴影/反光 / Bright/dark/shadow/reflection", "曝光、白平衡、HSV、结果 / Exposure, white balance, HSV, result", "待测 / Pending"],
]
story += [table(camera_rows, [3.6 * cm, 4.5 * cm, 6.0 * cm, 2.7 * cm])]

# Software and obstacle strategy
story += [heading("7.", "软件、状态机与障碍应对策略", "Software, State Machine and Obstacle Strategy")]
module_rows = [
    ["模块 / Module", "输入 / Input", "处理 / Processing", "输出 / Output", "状态 / Status"],
    ["bev_road.py", "摄像头/录像 / Camera/video", "亮度、Sobel/HSV、实验BEV、连通域 / Brightness, Sobel/HSV, experimental BEV, components", "道路候选与调试 / Road candidates and debug", "语法通过；标定待做 / Syntax passed; calibration pending"],
    ["bev_segmentation.py", "320×240彩色帧 / 320×240 colour frame", "红绿HSV、道路密度、CW/CCW、恢复状态 / Red-green HSV, road density, CW/CCW, recovery", "逻辑steer/speed，约20 Hz / Logical steer/speed, ~20 Hz", "原型；实车指标待做 / Prototype; vehicle metrics pending"],
    ["orange_pi_gpio.py", "逻辑目标 + 物理按钮 / Logical targets + physical button", "GPIO/PWM、限幅、状态、250 ms看门狗 / GPIO/PWM, limits, state, watchdog", "舵机PWM + 电机PWM/DIR / Steering PWM + motor PWM/DIR", "语法通过；真实映射和硬件待验 / Syntax passed; mapping and hardware pending"],
]
story += [table(module_rows, [3.2 * cm, 3.3 * cm, 5.5 * cm, 3.0 * cm, 2.8 * cm])]

story += [subheading("7.1", "算法选择", "Algorithm Selection")]
story += bilingual(
    "当前基线选择传统OpenCV而不是依赖尚未验证的NPU路径，因为HSV、形态学、连通域和道路密度容易解释、离线复现和参数审查。它的代价是对光照和阈值敏感，因此必须冻结相机参数并用分层数据集报告指标。BEV用于把透视道路映射到近似俯视空间，但当前源点仍需实车地面标定，不能把实验映射写成最终几何。",
    "The baseline uses conventional OpenCV rather than an unverified NPU path because HSV, morphology, connected components and road density are explainable, reproducible offline and easy to audit. The cost is lighting and threshold sensitivity, so camera parameters must be frozen and metrics reported on a stratified dataset. BEV maps the perspective road into an approximate top view, but its source points still require vehicle-ground calibration and the experimental mapping must not be described as final geometry.",
)

story += [subheading("7.2", "红绿障碍策略", "Red-Green Obstacle Strategy")]
obstacle_rows = [
    ["场景 / Scenario", "当前策略 / Current Strategy", "边界风险 / Edge Risk", "验证指标 / Validation Metric"],
    ["红色 / Red", "按比赛通过侧产生转向力 / Generate steering force for required passing side", "远小目标、反光、边缘畸变 / Small distant target, reflection, edge distortion", "召回、通过侧正确率、最小识别距离 / Recall, passing-side accuracy, minimum range"],
    ["绿色 / Green", "与红色方向相反的合规侧 / Opposite compliant side from red", "绿色背景/白平衡漂移 / Green background or white-balance drift", "召回、误检、完整回合 / Recall, false positives, full laps"],
    ["红绿同时 / Both", "按距离/风险和方向策略选择 / Select using distance/risk and direction strategy", "遮挡、面积排序错误 / Occlusion, incorrect area ordering", "组合场景成功率 / Combined-scene success rate"],
    ["暂时丢失 / Temporary loss", "先停车或低速恢复，不保持旧高速 / Stop or low-speed recovery; do not hold old high speed", "恢复转向符号错误 / Wrong recovery steering sign", "恢复时间、碰撞、超时 / Recovery time, contacts, timeout"],
    ["摄像头/进程失效 / Camera/process failure", "视觉请求0；GPIO更新看门狗停车 / Vision requests zero; GPIO update watchdog stops", "Linux/PWM整体冻结可能保持最后输出 / Complete Linux/PWM freeze may hold output", "停车时间、冻结边界与硬件保护 / Stop time, freeze boundary and hardware fail-safe"],
]
story += [table(obstacle_rows, [3.0 * cm, 5.2 * cm, 4.5 * cm, 4.1 * cm])]

story += [subheading("7.3", "尚未实现的比赛功能", "Competition Functions Not Yet Complete")]
story += bilingual(
    "停车区识别、圈数统计、最终停车、方向初始化的完整实车逻辑和尚未量化的低置信度策略仍是提交前缺口。文档已经给出接口与测试位置，但不会把计划描述成已完成。",
    "Parking-zone recognition, lap counting, final stop, complete vehicle direction initialisation and a quantified low-confidence policy remain pre-submission gaps. Interfaces and test locations are documented, but plans are not presented as completed behaviour.",
)

# Systems thinking and risk
story += [heading("8.", "系统思维、方案取舍与风险", "Systems Thinking, Trade-offs and Risk")]
trade_rows = [
    ["选择 / Choice", "替代方案/代价 / Alternative or Cost", "工程理由 / Engineering Rationale", "数据闭环 / Data Closure"],
    ["阿克曼转向 / Ackermann", "差速滑移更简单 / Skid steering simpler", "汽车式轨迹、直线稳定、轮胎擦滑小 / Automotive path, straight stability, less scrub", "左右半径、偏差、机构迭代待测 / Radii, deviation and iteration pending"],
    ["Orange Pi单板GPIO直控 / Single-board Orange Pi GPIO", "双控制器有故障隔离 / Two controllers add fault isolation", "减少器件、线束和协议延迟；输出集中审查 / Fewer parts, wires and protocol latency; centralised output review", "映射、波形、冻结边界与硬件保护待测 / Mapping, waveforms, freeze boundary and hardware protection pending"],
    ["单USB彩色摄像头 / One USB colour camera", "多传感器有冗余 / Multiple sensors add redundancy", "同时看赛道与颜色，布置简洁 / Track and colour together, simple layout", "光影、召回、误检、断连待测 / Lighting, recall, FP and loss pending"],
    ["本地GPIO/PWM / Local GPIO/PWM", "板间控制器可独立失效停车 / A second controller can stop independently", "无无线、无板间协议、延迟路径短 / No radio or inter-board protocol; short latency path", "设备树、资源占用和独立保护待冻结 / Device tree, ownership and independent protection pending"],
    ["开环速度 / Open-loop speed", "编码器PI抗负载变化 / Encoder PI resists load variation", "当前明确不读取编码器，先降低集成复杂度 / No encoder reading in current scope; lower integration complexity", "电量分层速度/停车距离映射待测 / Battery-stratified speed and stopping map pending"],
]
story += [table(trade_rows, [3.2 * cm, 4.0 * cm, 5.5 * cm, 4.1 * cm])]

story += [subheading("8.1", "主要FMEA", "Principal FMEA")]
fmea_rows = [
    ["故障 / Failure", "影响 / Effect", "控制 / Control", "验证 / Verification"],
    ["上电运动 / Power-on motion", "损坏或违规 / Damage or violation", "enabled=false模板 + WAIT_START物理启动 / Disabled template + WAIT_START arm", "G-01/G-02反复冷启动 / Repeated G-01/G-02 cold starts"],
    ["GPIO/PWM映射错误 / Wrong GPIO/PWM mapping", "误动作或损坏 / Unintended action or damage", "模板映射-1、非法配置拒绝启用 / Template mappings -1; invalid config rejected", "排针/设备树/枚举核对 + G-04"],
    ["控制循环停止 / Control-loop stall", "旧输出持续 / Stale output persists", "250 ms控制更新看门狗 / 250 ms control-update watchdog", "G-05五次实际时间 / Five G-05 measurements"],
    ["故障自动恢复 / Automatic post-fault motion", "无人确认即运动 / Motion without confirmation", "必须物理重新启动 / Physical re-arm required", "G-06/G-07"],
    ["Linux/PWM整体冻结 / Complete Linux/PWM freeze", "最后PWM可能持续 / Last PWM may persist", "当前仅总开关和人工旁站 / Currently main switch and spotter only", "故障注入并决定独立硬件保护 / Inject faults and decide hardware fail-safe"],
    ["电机启动压降 / Motor-start sag", "Orange Pi复位 / Orange Pi reset", "分支供电、保险、短回路、余量 / Branch power, fuse, short return, margin", "E-08五次峰值 / Five E-08 surge trials"],
    ["舵机顶死 / Servo stall", "过流、发热、转向损伤 / Overcurrent, heat, damage", "软件限幅 + 机械余量 / Software limit + mechanical margin", "M-09/E-09"],
    ["强光/阴影/反光 / Bright/shadow/reflection", "颜色误判、道路丢失 / Colour error, road loss", "固定相机参数、分层测试、降速/停车 / Frozen parameters, stratified tests, slow/stop", "S-04/S-10"],
    ["无线未关闭 / Radios enabled", "规则风险与不确定通信 / Rule risk and uncontrolled communication", "本地自动启动前执行关闭并保存证据 / Disable before local autostart and preserve evidence", "rfkill/ip link截图 / rfkill/ip link evidence"],
]
story += [table(fmea_rows, [3.2 * cm, 4.0 * cm, 5.5 * cm, 4.1 * cm])]

story += [subheading("8.2", "数据驱动决策格式", "Data-Driven Decision Format")]
story += [p(
    "约束/问题 → 候选X与Y → 同条件测试 → 量化结果 → 选择 → 新风险与缓解 → 对应提交和证据<br/>"
    "Constraint/problem → candidates X and Y → controlled test → quantified result → selection → new risk and mitigation → matching commit and evidence",
    "CalloutCN",
)]

# Tests
story += [heading("9.", "测试、量化指标与迭代", "Tests, Quantitative Metrics and Iteration")]
story += bilingual(
    "测试按静态/架空、低速、子系统、完整回合和故障注入逐级推进。每次固定提交、电池、场地、光照和参数；记录失败；相邻迭代只改变一个主要变量。",
    "Testing progresses through static/lifted, low-speed, subsystem, full-lap and fault-injection levels. Each run fixes commit, battery, field, lighting and parameters; failures are preserved; adjacent iterations change one principal variable.",
)
test_rows = [
    ["ID/类别 / Category", "方法 / Method", "必须报告 / Required Report", "通过目标 / Pass Target"],
    ["G-01...G-10 GPIO安全", "DRY_RUN、抬轮GPIO/PWM与故障注入 / DRY_RUN, lifted GPIO/PWM and fault injection", "映射、频率、占空比、脉宽、超时、退出和方向切换波形 / Mapping, frequency, duty, pulse, timeout, exit and direction-change waveforms", "无上电运动；超时/退出停车；故障不自动恢复 / No power-on motion; timeout/exit stop; no auto-recovery"],
    ["机械 / Mechanical", "尺寸、质量、2 m直线、左右圆、固定距离 / Dimensions, mass, 2 m straight, circles, fixed distance", "均值、范围、照片、异常 / Mean, range, photo, anomalies", "尺寸合规、无机构干涉、重复性可解释 / Compliant, no interference, explainable repeatability"],
    ["动力 / Power", "静止、视觉、直行、启动、最大转向 / Idle, vision, straight, start, full steer", "电压/电流均值峰值、5 V最低、温度 / Voltage/current mean/peak, 5 V min, temperature", "无复位/断连；额定值有余量 / No reset/loss; rating margin"],
    ["视觉 / Vision", "按颜色、距离、位置、光照分层 / Stratify by colour, range, position, lighting", "TP/FN/FP、召回、空场误检 / TP/FN/FP, recall, empty false positives", "由实际任务目标冻结阈值 / Freeze thresholds from task targets"],
    ["性能 / Performance", "端到端时间戳或高速录像 / End-to-end timestamps or high-speed video", "均值、P95、最大延迟、FPS、掉帧 / Mean, P95, max latency, FPS, drops", "最坏延迟与速度/停车距离安全匹配 / Worst latency compatible with speed/stopping distance"],
    ["完整赛程 / Full run", "CW/CCW、红绿组合、停车 / CW/CCW, colour combinations, parking", "每回合时间、碰撞、干预、失败类型 / Per-run time, contacts, intervention, failure type", "目标：连续10回合零碰撞/零干预 / Target: ten consecutive zero-contact, zero-intervention runs"],
]
story += [table(test_rows, [3.2 * cm, 4.8 * cm, 5.6 * cm, 3.2 * cm])]

story += [subheading("9.1", "视觉指标定义", "Vision Metric Definitions")]
metric_rows = [
    ["指标 / Metric", "定义 / Definition", "用途 / Use"],
    ["召回率 / Recall", "TP / (TP + FN)", "避免漏检红绿障碍 / Avoid missed obstacles"],
    ["精确率 / Precision", "TP / (TP + FP)", "避免错误障碍触发 / Avoid false obstacle actions"],
    ["空场误检率 / Empty-track FP rate", "有误触发的空场帧 / 全部空场帧 / False-trigger empty frames / all empty frames", "避免无故急转 / Avoid unjustified steering"],
    ["端到端延迟 / End-to-end latency", "采集曝光到GPIO/PWM输出变化 / Capture exposure to GPIO/PWM output change", "结合速度计算安全距离 / Combine with speed for safe distance"],
    ["成功回合率 / Successful-lap rate", "无碰撞、无干预且完成规则任务的回合 / Runs completed without contact or intervention", "总体可靠性 / Overall reliability"],
]
story += [table(metric_rows, [4.1 * cm, 7.1 * cm, 5.6 * cm])]

story += [subheading("9.2", "单次测试记录", "Single-Test Record")]
record_rows = [
    ["字段 / Field", "记录 / Record"],
    ["日期、参与人员 / Date and participants", ""],
    ["Git提交、软件/镜像版本 / Git commit and software/image version", ""],
    ["硬件、电池、电压 / Hardware, battery and voltage", ""],
    ["场地、方向、光照 / Field, direction and lighting", ""],
    ["假设与唯一改动 / Hypothesis and single change", ""],
    ["参数与过程 / Parameters and procedure", ""],
    ["原始数据与证据链接 / Raw data and evidence link", ""],
    ["结果、失败分类 / Result and failure classification", ""],
    ["结论与下一步 / Conclusion and next step", ""],
]
story += [table(record_rows, [6.0 * cm, 10.8 * cm])]

# Reproducibility
story += [heading("10.", "可复现性、提交与证据缺口", "Reproducibility, Commits and Evidence Gaps")]
story += bilingual(
    "仓库沿用WRO Future Engineers官方模板前缀，并在中文目录名后保留原模板类别。README已超过5000字符；代码、DXF、PNG/SVG接线、测试、FMEA、标定、BOM和变更记录均有入口。满分声明仍取决于主分支有效提交、最终CAD、六视图、冻结版本和独立复现。",
    "The repository retains the official WRO Future Engineers category prefixes with Chinese folder names. README exceeds 5,000 characters; code, DXF, PNG/SVG wiring, tests, FMEA, calibration, BOM and change records are indexed. A full-score claim still depends on meaningful main-branch commits, final CAD, six views, frozen versions and independent reproduction.",
)
repo_rows = [
    ["目录 / Folder", "内容 / Content", "规则用途 / Rule Purpose"],
    ["models模型", "底盘、尺寸、层板DXF / Chassis, dimensions, plate DXF", "CAD与机械复现 / CAD and mechanical reproduction"],
    ["schemes原理图", "PNG/SVG接线、GPIO/PWM映射和配电 / PNG/SVG wiring, GPIO/PWM mapping and power", "电路接线 / Electrical reproduction"],
    ["src源代码", "视觉、GPIO/PWM安全执行、默认禁用配置和历史实验 / Vision, GPIO/PWM safe execution, disabled config and history", "完整源代码与架构 / Source code and architecture"],
    ["other其他", "BOM、测试、标定、FMEA、日志、评分证据 / BOM, tests, calibration, FMEA, log, rubric evidence", "工程过程与可复现性 / Process and reproducibility"],
    ["t-photos团队照片", "队伍、赛事、制作过程 / Team, competition, development", "团队与研发证据 / Team and process evidence"],
    ["v-photos车辆照片", "比赛现场；六视图待补 / Competition field; six views pending", "每侧、顶部、底部照片 / Every side, top and bottom"],
    ["video视频", "YouTube与本地压缩视频 / YouTube and local compressed video", "至少30秒自动驾驶 / At least 30 s autonomous driving"],
]
story += [table(repo_rows, [3.4 * cm, 7.4 * cm, 6.0 * cm])]

story += [subheading("10.1", "独立复现验收", "Independent Reproduction Acceptance")]
story += bilingual(
    "由未参与编程的队员仅依据仓库完成：定位接线和程序、枚举GPIO/PWM、核对排针与line/channel、安装Python依赖、复制默认禁用配置、解释状态机、完成DRY_RUN和架空G-01至G-10、触发250 ms控制更新超时并定位日志。记录用时、卡住步骤和由此产生的文档修改。无口头提示且所有映射有证据后才可声明完全可复现。",
    "A member who did not write the software must use only the repository to locate wiring and programs, enumerate GPIO/PWM, map header pins to line/channels, install Python dependencies, copy the disabled configuration, explain the state machine, complete DRY_RUN and lifted-wheel G-01 through G-10, trigger the 250 ms control-update timeout and locate logs. Record elapsed time, blocked steps and documentation changes. Claim full reproducibility only when no verbal assistance is needed and all mappings have evidence.",
)

story += [subheading("10.2", "提交前关键缺口", "Critical Pre-Submission Gaps")]
gap_rows = [
    ["优先级 / Priority", "缺口 / Gap", "完成证据 / Completion Evidence", "负责人 / Owner"],
    ["P0", "确认电池、驱动器、稳压器、舵机型号和电气接口 / Confirm battery, driver, regulator, servo and interfaces", "标签照片 + 更新BOM/接线/图纸 / Label photos + updated BOM/wiring", "黄鸣博 / Huang Mingbo"],
    ["P0", "冻结GPIO/PWM映射并完成G-01...G-10 / Freeze GPIO/PWM mapping and complete G-01...G-10", "排针对照、枚举、配置哈希、波形、超时视频和签字 / Header map, enumeration, config hash, waveforms, timeout video and sign-off", "陆昭颖 + 黄鸣博"],
    ["P0", "关闭Linux/PWM冻结安全边界 / Close Linux/PWM freeze boundary", "故障注入结果 + 独立硬件保护决策与实现 / Fault results + hardware-fail-safe decision and implementation", "陆昭颖 + 黄鸣博 + 薛源"],
    ["P0", "六视图与趣味团队照 / Six views and informal team photo", "规定文件名的原图 / Originals with required filenames", "全队 / Team"],
    ["P0", "相机内参、位姿、HSV与识别指标 / Camera calibration, pose, HSV and metrics", "配置、样本、混淆统计 / Config, samples, confusion statistics", "陆昭颖 / Lu Zhaoying"],
    ["P0", "停车区、圈数与最终停车 / Parking, lap count and final stop", "状态机、代码、边界测试和视频 / State machine, code, edge tests and video", "陆昭颖 / Lu Zhaoying"],
    ["P1", "装车尺寸、质量、速度、半径和支架CAD / Final dimensions, mass, speed, radius and mount CAD", "测量照片、原始表、CAD / Photos, raw table and CAD", "张隽泽 / Zhang Junze"],
    ["P1", "电流、最低电压、温度和30分钟稳定性 / Current, minimum voltage, temperature and 30-minute stability", "原始日志 + 汇总 / Raw logs + summary", "黄鸣博 + 陆昭颖"],
    ["P1", "连续10回合和故障注入 / Ten consecutive laps and faults", "逐回合表、原视频、失败记录 / Per-run table, original video, failures", "全队 / Team"],
    ["P1", "冻结提交、镜像SHA-256和视频映射 / Freeze commit, image SHA-256 and video mapping", "SHA、版本清单、video.md / SHA, version list, video.md", "陆昭颖 + 薛源"],
    ["P1", "主分支3+有效提交 / 3+ meaningful main-branch commits", "不同工程主题的清晰提交说明 / Clear messages for distinct engineering themes", "全队 / Team"],
]
story += [table(gap_rows, [2.0 * cm, 6.0 * cm, 5.9 * cm, 2.9 * cm])]

story += [subheading("10.3", "建议提交序列", "Recommended Commit Sequence")]
commit_rows = [
    ["顺序 / Order", "说明 / Message", "主题 / Theme"],
    ["1", "docs: map 2026 rubric evidence and add archival engineering log", "评分、PDF与导航 / Rubric, PDF and navigation"],
    ["2", "control: add direct Orange Pi GPIO executor and process watchdog", "GPIO/PWM与安全执行 / GPIO/PWM and safe execution"],
    ["3", "hardware: add direct-control wiring and verified GPIO/PWM map", "电气复现 / Electrical reproduction"],
    ["4", "test: record power vision and full-lap validation results", "实测与迭代 / Measurements and iteration"],
    ["5", "release: freeze competition configuration and video mapping", "提交快照 / Submission freeze"],
]
story += [table(commit_rows, [2.1 * cm, 9.7 * cm, 5.0 * cm])]
story += [p("本次生成不执行Git暂存、提交或推送；由队伍审核后自行提交。 / This build does not stage, commit or push. The team will review and commit independently.", "CalloutCN")]

# Sign-off
story += [heading("11.", "最终签署与声明", "Final Sign-Off and Declaration")]
story += bilingual(
    "签署表示负责人已经核对对应实物、原始数据、代码和文档的一致性，不表示预先保证裁判分数。任何最终修改都必须重新运行链接、代码和PDF检查，并记录新的提交号。",
    "Sign-off confirms that the responsible person checked consistency among physical hardware, raw data, code and documentation. It does not pre-guarantee a judging score. Any final change requires link, code and PDF checks to be repeated and a new commit recorded.",
)
sign_rows = [
    ["负责人 / Owner", "核验范围 / Verification Scope", "日期 / Date", "提交/证据 / Commit or Evidence", "签名 / Signature"],
    ["陆昭颖 / Lu Zhaoying", "视觉、状态机、参数、软件版本 / Vision, state machine, parameters, software versions", "", "", ""],
    ["张隽泽 / Zhang Junze", "尺寸、机械图、转向、六视图 / Dimensions, drawings, steering, six views", "", "", ""],
    ["黄鸣博 / Huang Mingbo", "型号、接线、电流、电压、保险、安全 / Models, wiring, current, voltage, fuse, safety", "", "", ""],
    ["薛源 / Xue Yuan", "规则、视频、截止时间和总体验收 / Rules, video, deadline and final acceptance", "", "", ""],
]
story += [table(sign_rows, [3.1 * cm, 6.7 * cm, 2.0 * cm, 3.0 * cm, 2.0 * cm], padd=7)]

story += [Spacer(1, 0.45 * cm), subheading("11.1", "引用与归档", "References and Archive")]
references = [
    "《未来工程师无人驾驶2026赛季规则》，附录C：工程日志与文档提交要求。 / Future Engineers Autonomous Driving 2026 Season Rules, Appendix C.",
    "《2026未来工程师—技术文档评审标准》。 / 2026 Future Engineers Engineering Documentation Rubric.",
    "WRO Future Engineers official repository template: https://github.com/world-robot-olympiad-association/wro2022-fe-template",
    "Public repository: https://github.com/chinaxueyuannew/wro2026-nanjingBSSN",
    "Driving video: https://youtu.be/DJcxiJCEFdo",
]
for ref in references:
    story.append(p("• " + ref, "BodyCN"))

story += [Spacer(1, 0.5 * cm), p(
    "文档结束 / End of document<br/>生成文件：other其他/engineering-log.pdf<br/>生成脚本：other其他/build_engineering_log_pdf.py",
    "CNSubTitle",
)]

doc.build(story)
print(f"Generated: {OUTPUT}")
