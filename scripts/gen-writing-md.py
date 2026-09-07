import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "data" / "question-banks"
data = json.loads((root / "writing-bank.json").read_text(encoding="utf-8"))
lines = [
    "# 作文范文题库（审核稿）",
    "",
    "> 上方表格便于阅读；**实际同步以文末 bank-json 代码块为准**。",
    "",
    "## 目录（每单元 3 篇）",
    "",
]
for unit in range(1, 7):
    lines.append(f"### Unit {unit}")
    lines.append("| ID | 标题 | 仿写填空 | 答案 |")
    lines.append("|----|------|----------|------|")
    for s in data["samples"]:
        if s["unit"] == unit:
            fp = s["fillPrompt"].replace("|", "/")
            lines.append(f"| {s['id']} | {s['title']} | {fp} | {s['fillAnswer']} |")
    lines.append("")
lines += [
    "## 待审核区（课堂新范文暂放此处，审核后写入 bank-json）",
    "",
    "---",
    "",
    "## 机器同步区（修改此处后运行 启动.bat）",
    "",
    "```bank-json",
    json.dumps(data, ensure_ascii=False, indent=2),
    "```",
    "",
]
(root / "writing-bank.md").write_text("\n".join(lines), encoding="utf-8")
print("OK")
