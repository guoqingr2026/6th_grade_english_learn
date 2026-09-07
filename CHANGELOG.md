# Changelog

本文件记录 **PEP 六年级英语上册综合知识记忆训练营** 的全部重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)（主版本.次版本.修订号）。

---

## 变更记录规范（自 2026-08-01 起生效）

1. **每次合入前**必须在本文档 `[Unreleased]` 下追加条目（或发布时归入版本号小节）。
2. **合入须审核**：至少 **1 名维护者** 审阅通过后方可合并（见 [CONTRIBUTING.md](./CONTRIBUTING.md)）。
3. 条目分类：`Added` | `Changed` | `Fixed` | `Removed` | `Security` | `Docs`。
4. 涉及题库/精讲/脚本生成时，注明是否 **merge-by-id**、是否影响 `release/`。
5. 发布版本时：将 `[Unreleased]` 内容移至新版本号，并写上发布日期。

---

## [Unreleased]

### Added

- 精讲版块 **截图存档**：工具栏「截图·任务 / 截图·作业」，Win+Shift+S 后 Ctrl+V 粘贴，自动命名保存至 `assets/images/snip/unit{N}/{task|homework}/`，精讲下方画廊展示，支持查看与删除。
- `data/study-hub/snip-index.json`：截图索引；API `save-snip` / `list-snips` / `delete-snip`。
- **版本管控**：`VERSION`（1.1.0）、`scripts/release_pack.py`、`发布打包.bat`、`manifests/` 文件清单与 `docs/VERSION_HISTORY.md` 差异记录。
- `docs/学生学习辅导手册.docx` / `.pdf`：学生书面辅导资料（软件使用 + U1–U6 全册学习资料 + 附录5）。
- `scripts/generate_student_handbook.py`、`生成学生辅导手册.bat`：一键生成上述手册。
- `README_EN.md`：英文版项目总览。
- `CONTRIBUTING.md`：贡献流程、Changelog 要求、合入审核清单。
- `.github/pull_request_template.md`：PR 模板（含 Changelog 与审核勾选项）。

### Changed

- 学生学习辅导手册增加 **第三篇：112 页课文双语全文**（与 `library/reading/*.html` 一致）。
- 学生学习辅导手册增加 **第四篇：知识点精讲全文**（31 页，与 `library/knowledge/*.html` 及 `knowledge-bank.json` 一致）。
- 局域网自动同步间隔改为 **10 秒**；同步后保留当前练习题与连连看进度。
- 不规则动词专项移除 Unit 1–6 单元筛选，固定练习附录5 全部 47 词。
- 讲读/精讲朗读：过滤填空下划线与装饰符号；精讲 `pre` 树状图等富文本按行提取并识别中英文。
- TTS 声色拆分为 **中文声 / 英文声** 独立选择；默认中文 Xiaoxiao Online、英文 Ava Online。
- TTS 过滤增强：支持全角下划线 `＿` 等填空符号，中英文朗读统一走 `ttsSanitize`。
- 讲读/精讲词汇高亮：改为 **附录2 完整单词**，按当前课本 **P.x** 页码匹配；整词边界匹配，避免 `was`/`ill` 误嵌在 `washed`/`illness` 中。
- `启动.bat` / `生成学生辅导手册.bat`：改用 `python --version` 检测 Python（不依赖 `where.exe`）；支持 Python 3.12。

### Fixed

- 修复语法连连看、选择题、填空在自动同步/刷新后题目或词块顺序意外变化的问题。

### Docs

- `docs/学生学习辅导手册`：学生书面辅导资料生成说明。
- `README.md`：增加变更日志、贡献指南、英文 README 链接。

---

## [1.0.0] - 2026-08-01

首个可交付版本（内容闭环 + 文档齐全 + 发布检查清单）。

### Added

- 离线 Web 学习系统：`启动.bat` + `lan_server.py` 局域网静态站与同步 API。
- 练习模块：单词卡片、语法句型、常用语、选择题、综合填空、不规则动词专项、优秀作文、错题本、学习日志。
- 课文中英文讲读 + 知识点精讲（PPT 全屏弹窗、课本图、附录高亮、交互笔记）。
- 双轨积分、家长密码、多端「同步数据」、`lan-sync/` 按昵称存储。
- 题库程序分离：`data/question-banks/*.json` + CSV/题卡导入 + `import-question-cards.py`。
- `data/practice/supplement.json`：附录2–5 **OR 合并**补充包；`build_practice_supplement.py`。
- `data/practice/irregular-verbs.json`：附录5 **47** 个不规则动词独立词表。
- `scripts/knowledge_u36_sections.py`：U3–U6 各 Part 课文填空问答 + 写作范文（U3 Part B 深度）。
- `scripts/knowledge_u12_sections.py`：U1–U2 各 Part 课文填空问答 + 写作范文（6 题/Part）。
- `scripts/validate_appendix_coverage.py`：附录2/4/5 覆盖只读校验。
- `scripts/generate_u12_knowledge.py`：U1–U6 + 复习精讲生成；`PATCH_APPEND_PAGE_IDS` 保护 `u3-k-part-b` 正文。
- 各练习模块 **单元筛选**（语法、常用语、动词、错题本、日志等）。
- Cursor Skill：`.cursor/skills/pep6-knowledge-lecture/SKILL.md`。
- 文档：`FINAL_PRODUCT_MANUAL.md`、`PARENT_GUIDE.md`、`DEPLOY.md`、`release/使用说明.txt` 及子目录 README。
- `sync-release.bat` + `release/` 可分发 ZIP 包结构。

### Changed

- 练习区：**取消自动朗读与答后自动跳题**；仅讲读/精讲工具栏「朗读」在本页链式 TTS。
- 动词专项改为从 `irregular-verbs.json` 加载，不再被 supplement 覆盖 verb 列表。
- 精讲 U1–U6 各 Part 统一含「课文填空与问答精讲」与写作范文区块。
- U3 Part B：保留手工标杆正文，生成器仅 **追加** 标准填空/写作块。
- 根目录 `README.md` 重写为项目总览（结构、体量、手册索引、Skill/MCP、发布清单）。

### Fixed

- 附录解析单行 HTML、`sync_u12_practice` 整库覆盖、`app.js` 词卡生成函数损坏等历史问题（merge-by-id + 备份恢复策略）。
- `FINAL_PRODUCT_MANUAL.md` 章节编号（交互原则 1.5–1.8）。

### Security

- 家长密码保护手动判题、行为积分、兑换与一键重置；`PARENT_GUIDE.md` 勿分发给学生。

---

## [0.9.0] - 2026-07-28（内部里程碑）

### Added

- U3–U6 知识点精讲批量生成（跳过 `u3-k-part-b` 覆盖）。
- `data/practice/supplement.json` 运行时 OR 合并。
- 单元筛选首批接入（词卡、选择题、填空、作文）。

### Changed

- U1/U2 讲读与练习题 **prefer=existing** 合并策略。

---

## 版本对照

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-08-01 | 首个对外可交付版本 |
| 0.9.0 | 2026-07-28 | U3–U6 精讲与补充包内部里程碑 |

[Unreleased]: https://github.com/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/releases/tag/v1.0.0
[0.9.0]: https://github.com/releases/tag/v0.9.0
