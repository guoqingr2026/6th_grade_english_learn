# 2026新人教版 PEP 六年级英语上册 · 综合知识记忆训练营

**旭日长空光照人生（Sunshine Life Team）出品**

面向 PEP 六年级上册（2024/2026 修订版）的 **离线 Web 学习系统**：课文讲读、知识点精讲、多模块练习、错题本、双轨积分、局域网多端同步。双击 `启动.bat` 即可在教室或家庭局域网使用。

---

## 一、快速开始

| 步骤 | 操作 |
|------|------|
| 1 | 双击 **`启动.bat`**（自动导入题卡、同步课文、启动服务） |
| 2 | 浏览器打开 **`http://localhost:8080`** |
| 3 | 右侧保存昵称 → 多设备时点 **「同步数据」** |

**手机同 WiFi**：`http://{电脑IPv4}:8080`（`ipconfig` 查看地址，勿用 localhost）。

**分发包**：运行 `sync-release.bat` 后压缩 `release/` 文件夹为 ZIP。

---

## 二、功能模块

| 模块 | 说明 |
|------|------|
| 单词卡片 | 附录词汇闪卡，支持单元筛选与家长判题 |
| 语法句型 / 常用语 | 句型与表达练习，单元筛选 |
| 选择题 / 综合填空 / 优秀作文 | 闯关练习，**不自动跳题、不自动朗读** |
| 不规则动词专项 | **附录5 共 47 个**（`data/practice/irregular-verbs.json`） |
| 课文中英文讲读 | 左图右文；仅点 **「朗读」** 本页逐句 TTS |
| 知识点精讲 | 10 步结构；U1–U6 各 Part 含填空问答 + 写作范文 |
| 错题本 / 学习日志 | 自动收录 + 单元筛选 |
| 积分 / 家长密码 | 做题积分自动；行为积分与兑换需家长密码 |

交互原则详见 [FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md) §1.5。

---

## 三、文档索引（全部手册）

| 文件 | 读者 | 内容 |
|------|------|------|
| **[FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md)** | 教师 / 家长 / 维护者 | **完整产品说明书**：部署、同步、讲读精讲、题库规则、发布清单、维护命令 |
| **[PARENT_GUIDE.md](./PARENT_GUIDE.md)** | 家长（勿给学生） | 家长密码、积分、多端同步、朗读与跳题说明 |
| **[DEPLOY.md](./DEPLOY.md)** | 运维 | 公网静态托管（无局域网同步 API） |
| **[release/使用说明.txt](./release/使用说明.txt)** | 终端用户 | 一页纸快速说明 |
| **[data/question-banks/README.md](./data/question-banks/README.md)** | 命题 / 加题 | CSV 模板、OR 合并、AI 提示词 |
| **[data/study-hub/README.md](./data/study-hub/README.md)** | 内容编辑 | 讲读/精讲 CSV、JSON、朗读规则 |
| **[release/README_RELEASE.md](./release/README_RELEASE.md)** | 打包发布 | release 目录检查清单 |
| **[CHANGELOG.md](./CHANGELOG.md)** | 全员 | **变更日志**（每次合入必填 `[Unreleased]`） |
| **[CONTRIBUTING.md](./CONTRIBUTING.md)** | 贡献者 / 维护者 | 合入流程与 **审核清单** |
| **[README_EN.md](./README_EN.md)** | 国际读者 | 英文项目总览 |

---

## 四、项目结构

```
englishi learn/                    # 项目根（开发 + 运行）
├── 启动.bat                       # 一键启动（推荐入口）
├── sync-release.bat               # 同步到 release/ 分发包
├── index.html                     # 主页面
├── app.js                         # 练习、积分、同步、筛选（~3.3k 行）
├── study-hub.js                   # 讲读/精讲弹窗、TTS（~2.1k 行）
├── styles.css                     # 样式（~2.2k 行）
├── mastery.js                     # 掌握度统计
├── textbook_catalog.py            # U1–U6 课本元数据
├── FINAL_PRODUCT_MANUAL.md        # 产品说明书
├── PARENT_GUIDE.md
├── README.md                      # 本文件
├── assets/images/textbook/pages/  # 课本扫描图 page-001…098（体积最大）
├── data/
│   ├── question-banks/            # 选择题 / 填空 / 作文默认题库
│   ├── practice/
│   │   ├── supplement.json        # 附录2–5 OR 合并补充包
│   │   └── irregular-verbs.json   # 附录5 不规则动词 47 个
│   └── study-hub/
│       ├── reading-bank.json      # 讲读句子库
│       ├── knowledge-bank.json    # 精讲 bodyHtml 索引
│       └── library/
│           ├── reading/           # 讲读 HTML（按页）
│           └── knowledge/         # 精讲 HTML（26 页）
├── scripts/                       # 生成、校验、同步 Python 脚本
├── word-sources/                  # Unit1–6 课文双语 CSV
├── lan-sync/                      # 运行时：按昵称存放同步数据
├── release/                       # 可分发 ZIP 包（结构与根目录对应）
└── .cursor/skills/
    └── pep6-knowledge-lecture/    # Cursor 精讲生成 Skill
```

### 体量统计（约，不含 `lan-sync` 运行时数据）

| 项目 | 数值 |
|------|------|
| 项目总大小 | **~398 MB**（主要为课本 PNG） |
| `assets/` 图片 | ~131 MB |
| `data/` 数据 | ~2.8 MB |
| `scripts/` | ~0.4 MB |
| `release/` 分发包 | ~131 MB（含图片与 data 副本） |
| 文件总数 | ~790 |
| 讲读 HTML 页 | **112** |
| 精讲 HTML 页 | **26**（U1–U6 × 4 Part + 复习；U3 Part B 为手工标杆） |

### 默认题库规模

| 题库 | 数量 | 说明 |
|------|------|------|
| 选择题 `quiz-bank.json` | 17 | 可与 CSV / supplement 合并扩容 |
| 综合填空 `fillblank-bank.json` | 32 | |
| 作文 `writing-bank.json` | 18 | |
| `supplement.json` | +89 选择 / +89 填空 | 启动时 OR 合并 |
| 不规则动词 | **47** | 固定独立文件，不走 supplement |

---

## 五、内容生成与维护命令

```powershell
cd "C:\Users\guoqren\.cursor\englishi learn"

# 精讲：U1–U6 + 复习（U3 Part B 仅追加填空/写作块，不覆盖正文）
python scripts/generate_u12_knowledge.py

# 附录2–5 → supplement.json（OR 合并，不删默认库）
python scripts/build_practice_supplement.py

# 附录覆盖只读校验（142 词 / 55 表达 / 47 动词）
python scripts/validate_appendix_coverage.py

# 同步 release 分发包
sync-release.bat
```

**数据安全**：题库与精讲一律 **按 id 合并**；禁止整库覆盖。精讲标杆页 `u3-k-part-b.html` 正文受保护，仅追加标准「课文填空与问答」「写作范文」区块。

精讲填空/写作数据源：

- `scripts/knowledge_u12_sections.py` — Unit 1–2
- `scripts/knowledge_u36_sections.py` — Unit 3–6

---

## 六、Cursor Skill 与 MCP

### Skill（项目内）

| 路径 | 名称 | 用途 |
|------|------|------|
| `.cursor/skills/pep6-knowledge-lecture/SKILL.md` | `pep6-knowledge-lecture` | 按 **U3 Part B 金标准** 生成/更新知识点精讲 HTML；引用附录2/4、10 步结构、举一反三 |

在 Cursor 中说「生成 U5 Part A 精讲」「更新知识点精讲」时会自动匹配该 Skill。

### MCP（项目内）

**本项目仓库内未配置专用 MCP 服务器**（无 `.cursor/mcp.json` 或项目级 MCP 定义）。

运行时若使用 Cursor IDE 的 **cursor-app-control** 等全局 MCP，属于编辑器环境能力，非本仓库交付物。

---

## 七、精讲内容完成度

| 范围 | 课文填空与问答 | 写作范文 | 备注 |
|------|----------------|----------|------|
| Unit 1–2 | ✅ 各 Part A/B/C/Reading | ✅ 各 Part | 已按 U3 Part B 深度扩展（6 题/Part） |
| Unit 3 | ✅ | ✅ | Part B 手工精讲 + 末尾标准区块 |
| Unit 4–6 | ✅ | ✅ | `knowledge_u36_sections.py` |
| Revision | 复习页 | — | `appendix-k-revision` |

金标准参考：`data/study-hub/library/knowledge/u3-k-part-b.html`（~53k 字符，深度教学法内容）。

---

## 八、发布检查清单（摘要）

- [ ] `sync-release.bat` 后 `release/启动.bat` 可打开 localhost:8080
- [ ] 动词专项显示 **47/47**
- [ ] 练习区无自动朗读/跳题；讲读/精讲仅「朗读」链式 TTS
- [ ] `validate_appendix_coverage.py` 无缺口
- [ ] 各模块 **单元筛选** 可用
- [ ] 完整清单见 [FINAL_PRODUCT_MANUAL.md §七](./FINAL_PRODUCT_MANUAL.md)

---

## 九、项目总结

本仓库是一套 **可离线部署、可局域网同步、可渐进扩展** 的六年级英语综合学习产品：

1. **内容层**：112 页中英讲读 + 26 页知识点精讲（含附录校验与补充包 OR 合并）。
2. **练习层**：多题型闯关、47 个不规则动词专项、错题本与掌握度统计。
3. **运营层**：双轨积分、家长密码、CSV/题卡加题、HTML 报告导出。
4. **工程层**：纯静态前端 + Python 本地服务（`lan_server.py`）；题库与页面逻辑分离；merge-by-id 保护已有数据。
5. **协作层**：`pep6-knowledge-lecture` Skill 固化精讲生成规范；手册覆盖产品、家长、题库、讲读四条线。

**推荐工作流**：日常用根目录 `启动.bat` 上课 → 学期末 `sync-release.bat` 打包 → 按 `FINAL_PRODUCT_MANUAL.md` 备份 `lan-sync/` 与导出报告。

---

## 十一、变更管理与合入审核

自 **2026-08-01** 起：

1. **所有合入**须在 [CHANGELOG.md](./CHANGELOG.md) 的 `[Unreleased]` 记录变更。
2. **须维护者审核**后方可合并，流程见 [CONTRIBUTING.md](./CONTRIBUTING.md)。
3. GitHub PR 使用 [.github/pull_request_template.md](./.github/pull_request_template.md) 勾选清单；CI 会在改动代码/数据时检查是否更新 Changelog。

英文总览：[README_EN.md](./README_EN.md)

## 十、版本与许可

- **当前版本**：1.0.0（见 [CHANGELOG.md](./CHANGELOG.md)）
- **教材**：2026 秋 PEP 人教版六年级英语上册（修订版）
- **文档**：随功能更新，以仓库内最新 Markdown 为准
- **团队**：旭日长空光照人生（Sunshine Life Team）

如有问题，请先查阅 [FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md) 第九节 Q&A。
