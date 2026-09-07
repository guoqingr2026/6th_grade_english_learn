#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Align all units with PEP 2026 official textbook content."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GLOBAL_REPLACEMENTS = [
    ("欢聚一堂", "相聚在一起"),
    ("善于理财", "合理管理金钱"),
    ("What did you do, Peter?", "What did you do, Leo?"),
    ("Hi, Peter!", "Hi, Leo!"),
    ("Peter visited", "Leo visited"),
    ("你做什么了，彼得？", "你做什么了，利奥？"),
    (
        "Chen Jie: Nice! And you, Chen Jie? What did you do last weekend?",
        "Binbin: Nice! And you, Chen Jie? What did you do last weekend?",
    ),
    (
        "1. What did Binbin do last weekend? Binbin joined an online book fair last weekend.",
        "1. What did Binbin do last weekend? Binbin went to a science fair last weekend. He talked to some scientists and saw a robot that looked like Robin.",
    ),
    (
        "彬彬上周末参加了一个线上书展。",
        "彬彬上周末去了科学展。他和科学家交谈，还看到一个长得像罗宾的机器人。",
    ),
]

SKIP_FILES = {"sync_all_units_official.py", "sync_u1_amazing_places.py"}

LISTEN_BLOCK = """<p class="en">Listen and answer. 🎧</p>
<p class="zh">听录音并回答。🎧</p>
<p class="en">Chen Jie: Hi, Binbin. How was your weekend?</p>
<p class="zh">陈洁：嗨，彬彬。你的周末过得怎么样？</p>
<p class="en">Binbin: Great! I went to a science fair. I really liked it.</p>
<p class="zh">彬彬：很棒！我去了科学展。我非常喜欢。</p>
<p class="en">Amy: What did you like about it?</p>
<p class="zh">艾米：你喜欢科学展的哪些方面？</p>
<p class="en">Binbin: I talked to some scientists. I also saw a robot. It looked like Robin. Maybe Robin can meet it one day.</p>
<p class="zh">彬彬：我和一些科学家交谈了。我还看到一个机器人，它长得像罗宾。也许罗宾有一天能见到它。</p>
<p class="en">Chen Jie: I hope so.</p>
<p class="zh">陈洁：我希望如此。</p>
"""


def patch_text(path: Path) -> bool:
    if not path.is_file() or path.suffix not in {".html", ".json", ".py", ".js", ".md", ".csv"}:
        return False
    if any(s in path.name for s in SKIP_FILES):
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in GLOBAL_REPLACEMENTS:
        text = text.replace(old, new)
    if path.name == "u2-p025.html" and "I went to a science fair" not in text:
        marker = "<p class=\"en\">Binbin, Chen Jie and Amy are talking about last weekend."
        if marker in text:
            text = text.replace(marker, LISTEN_BLOCK + marker, 1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def patch_catalog() -> None:
    path = ROOT / "textbook_catalog.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('"title_cn": "欢聚一堂"', '"title_cn": "相聚在一起"', 1)
    text = text.replace('"title_cn": "善于理财"', '"title_cn": "合理管理金钱"', 1)
    path.write_text(text, encoding="utf-8")


def walk_and_patch(base: Path) -> list[str]:
    changed = []
    for p in base.rglob("*"):
        if p.is_file() and patch_text(p):
            changed.append(str(p.relative_to(ROOT)))
    return changed


def patch_unit2_csv() -> None:
    path = ROOT / "word-sources/Unit2_课文双语.csv"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        for old, new in GLOBAL_REPLACEMENTS:
            line = line.replace(old, new)
        out.append(line)
    if "science fair" not in "\n".join(out):
        idx = next(i for i, l in enumerate(out) if "What did Binbin do last weekend?" in l and l.startswith("18,"))
        insert = [
            '18,"Chen Jie: Hi, Binbin. How was your weekend?",陈洁：嗨，彬彬。你的周末过得怎么样？',
            "18,Binbin: Great! I went to a science fair. I really liked it.,彬彬：很棒！我去了科学展。我非常喜欢。",
            "18,Amy: What did you like about it?,艾米：你喜欢科学展的哪些方面？",
            '18,"Binbin: I talked to some scientists. I also saw a robot. It looked like Robin. Maybe Robin can meet it one day.",彬彬：我和一些科学家交谈了。我还看到一个机器人，它长得像罗宾。也许罗宾有一天能见到它。',
            "18,Chen Jie: I hope so.,陈洁：我希望如此。",
        ]
        out = out[:idx] + insert + out[idx:]
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    patch_catalog()
    patch_unit2_csv()
    changed = walk_and_patch(ROOT / "data")
    changed += walk_and_patch(ROOT / "release" / "data")
    for rel in ("app.js", "release/app.js", "generate_notes.py", "scripts/build-study-hub.py", "release/scripts/build-study-hub.py"):
        p = ROOT / rel
        if p.exists() and patch_text(p):
            changed.append(rel)
    print(f"[OK] Patched {len(changed)} files")
    for c in sorted(set(changed))[:40]:
        print(f"  - {c}")
    if len(changed) > 40:
        print(f"  ... and {len(changed) - 40} more")


if __name__ == "__main__":
    main()
