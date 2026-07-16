# 建议提交计划 / Recommended Commit Plan

规则要求主分支至少有3条说明明确的有效提交。以下只是提交拆分建议；本次文档更新不会自动提交、暂存或推送，由队伍检查后自行执行。

The rubric requires at least three clearly described meaningful commits on the main branch. The following is only a grouping recommendation. This documentation update does not automatically commit, stage or push; the team should review and perform those actions.

| 顺序 / Order | 建议提交说明 / Suggested Commit Message | 应包含 / Include | 验收 / Acceptance |
|---:|---|---|---|
| 1 | `docs: map 2026 rubric evidence and add archival engineering log` | 评分地图、证据登记、README、工程日志PDF / Rubric map, evidence register, README and engineering-log PDF | 链接可用，PDF可读 / Links valid; PDF readable |
| 2 | `control: switch current vehicle to Orange Pi direct GPIO output` | `orange_pi_gpio.py`、GPIO配置、源代码说明、软件架构、测试 / GPIO output, configuration, code guide, architecture and tests | Python检查通过；实物映射和架空故障测试完成 / Python checks pass; physical mapping and lifted fault tests complete |
| 3 | `hardware: add vision-only wiring diagram and verified pin map` | PNG/SVG接线图、接线说明、实物照片 / PNG/SVG diagram, wiring guide and hardware photos | 型号/电压/引脚与实车一致 / Models, voltages and pins match vehicle |
| 4 | `test: record power vision and full-lap validation results` | 真实测试表、日志、照片、参数 / Actual tests, logs, photographs and parameters | 原始证据与汇总一致 / Raw evidence matches summary |
| 5 | `release: freeze competition configuration and video mapping` | 版本号、提交SHA、镜像校验值、视频元数据、检查表 / Version, SHA, image checksum, video metadata and checklist | 截止前公共仓库可访问 / Public repository accessible before deadline |

不要为了“提交次数”制造空提交，也不要把上述工程主题压缩为一个含糊的“更新”。每次提交说明应指出子系统和工程目的；测试失败也应保留，并在下一次提交说明修复依据。

Do not create empty commits merely to increase the count, and do not squash these engineering themes into a vague “update”. Each message should name the subsystem and engineering purpose. Preserve failed tests and explain the evidence behind the next fix.
