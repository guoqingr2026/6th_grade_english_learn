## Summary

<!-- 1–3 句话说明本 PR 目的与用户可见影响 -->

## Type

- [ ] Feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Docs only (`docs`)
- [ ] Content (lecture / question banks)
- [ ] Release / `release/` sync

## Changelog

- [ ] **已更新** `CHANGELOG.md` → `[Unreleased]` 小节
- [ ] 条目类型：<!-- Added / Changed / Fixed / Removed / Security / Docs -->

## Testing

<!-- 如何验证；列出命令或手动步骤 -->

- [ ] `python scripts/validate_appendix_coverage.py`（若动附录/补充包）
- [ ] `python scripts/generate_u12_knowledge.py`（若动精讲生成）
- [ ] 浏览器冒烟：启动.bat → localhost:8080
- [ ] `sync-release.bat`（若影响分发包）

## Data safety

- [ ] 未整库覆盖默认题库 / 精讲 JSON
- [ ] 新条目含 `unit` 字段（如适用）
- [ ] `u3-k-part-b.html` 正文未被整页覆盖

## Review

- [ ] 已自测完成，请求维护者审核
- [ ] 维护者 Approve 后方可合并（见 CONTRIBUTING.md）
