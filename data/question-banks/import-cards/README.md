# 题卡导入说明

将课堂或练习产出的题目整理为 **题卡包（JSON）**，放入本目录后，运行 `启动.bat` 即可自动导入到对应题库。

## 快速步骤

1. 复制 `_templates/` 中的示例文件到本目录（`import-cards/`）
2. 重命名为有意义的名字，如 `quiz-unit3-week8.json`
3. 修改 `items` 数组中的题目（每题必须有唯一 `id`）
4. 双击 `启动.bat`（先导入题卡 → 再同步 MD → 再启动服务）
5. 浏览器 `Ctrl+F5` 刷新，标签页数量会更新

## 题卡包格式

```json
{
  "cardType": "quiz | fillblank | writing",
  "action": "append",
  "source": "来源说明（可选）",
  "items": [ ... ]
}
```

| 字段 | 说明 |
|------|------|
| `cardType` | 目标题库：`quiz` 选择题 / `fillblank` 综合填空 / `writing` 作文 |
| `action` | `append`（默认，按 id 新增或覆盖）/ `replace`（整库替换，慎用） |
| `source` | 备注来源，如「2026-03-28 课堂测验」 |
| `items` | 题目数组，字段规范见上级 `README.md` |

## 导入后文件去向

- 成功导入的题卡包会移动到 `import-cards/done/` 存档
- 导入结果写入 `quiz-bank.json` / `fillblank-bank.json` / `writing-bank.json`

## 仅导入、不启动服务

```bat
python scripts\import-question-cards.py
python scripts\sync-question-banks.py
```

## AI 辅助出题建议

可将本目录示例 + 字段规范发给 AI，要求输出 **可直接保存的 JSON 题卡包**，保存后放入 `import-cards/` 即可。
