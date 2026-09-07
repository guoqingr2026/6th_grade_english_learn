# 贡献与合入指南

感谢参与 **PEP 六年级英语上册综合知识记忆训练营** 的维护。自 **2026-08-01** 起，所有改动须记录 **CHANGELOG** 并经 **审核** 后方可合入。

---

## 一、基本原则

| 原则 | 说明 |
|------|------|
| **Changelog 必填** | 每次 PR / 合入在 `CHANGELOG.md` 的 `[Unreleased]` 下追加条目 |
| **审核后合入** | 至少 1 名项目维护者 Approve 后方可合并 |
| **数据安全** | 题库、精讲、词卡 **按 id OR 合并**；禁止无备份整库覆盖 |
| **标杆保护** | `u3-k-part-b.html` 正文不得被生成器整页覆盖 |
| **release 同步** | 影响运行行为的改动合入后应执行 `sync-release.bat` 并写入 Changelog |

---

## 二、工作流程

```
1. 从 main 拉取最新代码
2. 创建功能分支（建议：feat/xxx、fix/xxx、docs/xxx）
3. 完成改动 + 更新 CHANGELOG.md [Unreleased]
4. 本地验证（见下方检查清单）
5. 提交 PR，填写模板勾选项
6. 维护者审核 → 通过后合并
7. 发布时：将 [Unreleased] 归入新版本号并打 tag（如 v1.0.1）
```

### 分支命名建议

- `feat/unit-filter-journal` — 新功能
- `fix/verb-triple-load` — 缺陷修复
- `docs/changelog-policy` — 仅文档
- `content/u5-part-a-lecture` — 精讲/题库内容

---

## 三、CHANGELOG 写法

在 `CHANGELOG.md` 的 `[Unreleased]` 下按类型追加 bullet，**一行说清用户可见影响**：

```markdown
## [Unreleased]

### Added
- 学习日志增加按单元导出 CSV。

### Fixed
- 修复填空题在单元筛选为「全部」时偶发空白。

### Docs
- 更新 `data/question-banks/README.md` 导入示例。
```

- **Added**：新功能、新文件、新题库条目（大批量生成可概括写，细节放 PR 描述）
- **Changed**：行为或 UI 变更（含破坏性变更须醒目说明）
- **Fixed**：Bug 修复
- **Removed**：删除功能或文件
- **Security**：权限、密码、同步安全相关
- **Docs**：仅文档、注释、手册

纯 typo、无用户影响的格式整理 **可不写** Changelog（由维护者裁量）。

---

## 四、合入前自检清单

维护者与贡献者合并前请确认：

### 代码与行为

- [ ] `CHANGELOG.md` `[Unreleased]` 已更新
- [ ] 未整库覆盖 `quiz-bank.json` / `fillblank-bank.json` / `knowledge-bank.json`
- [ ] 新题/卡片含 **`unit`** 字段（1–6 或 0）
- [ ] 练习模块未引入自动朗读 / 答后自动跳题（除非经产品确认并写进 Changelog）
- [ ] 精讲生成未覆盖 `u3-k-part-b.html` 正文（仅允许 append 块）

### 脚本与数据

- [ ] 若改附录或补充包：已运行 `python scripts/validate_appendix_coverage.py`
- [ ] 若改精讲生成：已运行 `python scripts/generate_u12_knowledge.py` 并 spot-check HTML
- [ ] 若改 supplement：已运行 `python scripts/build_practice_supplement.py`

### 发布

- [ ] 若影响终端用户：已运行 `sync-release.bat`
- [ ] `FINAL_PRODUCT_MANUAL.md` 或子 README 已同步（若行为变更）
- [ ] PR 描述含 **测试说明**（如何验证）

---

## 五、审核职责（维护者）

审核 PR 时须确认：

1. **Changelog** 条目与 diff 一致、分类正确。
2. **数据安全**：无 bulk delete、无 force 覆盖用户数据路径。
3. **回归风险**：讲读/精讲 TTS、同步、积分、错题本核心路径。
4. **文档**：用户可见变更是否更新手册或 README。
5. **拒绝合入** 时须在 PR 注明原因；贡献者修正后重新请求审核。

无 GitHub 时，等效流程：**本地 diff 审查 + 维护者在 CHANGELOG 署名 + 书面确认** 后方可合入共享目录。

### GitHub 仓库建议设置

1. **Settings → Branches → Branch protection rules**（`main` / `master`）  
   - Require a pull request before merging  
   - Require approvals（至少 1）  
   - 可选：Require status checks — 勾选 `Changelog check` workflow  
2. 编辑 [.github/CODEOWNERS](./.github/CODEOWNERS)，填入维护者 `@GitHub用户名`  
3. PR 使用 [.github/pull_request_template.md](./.github/pull_request_template.md)

---

## 六、内容类贡献（精讲 / 题库）

| 类型 | 推荐方式 |
|------|----------|
| 精讲 HTML | 编辑 `scripts/knowledge_u12_sections.py` / `knowledge_u36_sections.py` 或 Skill 生成后走 PR |
| 讲读 CSV | `word-sources/UnitN_课文双语.csv` → `启动.bat` |
| 加题 | 网页 CSV 导入或 `import-cards/` JSON，**id 唯一** |
| 手工标杆 | 直接改 `u3-k-part-b.html` 须维护者审核，且 Changelog 标注 `Changed` |

---

## 七、联系方式

- 产品说明：[FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md)
- 英文总览：[README_EN.md](./README_EN.md)
- 变更历史：[CHANGELOG.md](./CHANGELOG.md)

**旭日长空光照人生（Sunshine Life Team）**
