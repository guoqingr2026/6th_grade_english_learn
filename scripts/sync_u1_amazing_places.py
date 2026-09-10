#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync Unit 1 to official final edition: Amazing places + Part A Leo dialogue."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Unit 1 reading pages (exclude revision appendix u1-p081+)
U1_READING = [
    ROOT / "data/study-hub/library/reading/u1-p005.html",
    ROOT / "data/study-hub/library/reading/u1-p006.html",
    ROOT / "data/study-hub/library/reading/u1-p009.html",
    ROOT / "data/study-hub/library/reading/u1-p010.html",
    ROOT / "data/study-hub/library/reading/u1-p011.html",
    ROOT / "data/study-hub/library/reading/u1-p013.html",
    ROOT / "data/study-hub/library/reading/u1-p014.html",
    ROOT / "data/study-hub/library/reading/u1-p017.html",
    ROOT / "data/study-hub/library/reading/u1-p018.html",
    ROOT / "data/study-hub/library/reading/intro-p005.html",
]

U1_KNOWLEDGE = list((ROOT / "data/study-hub/library/knowledge").glob("u1-k-*.html"))

TITLE_REPLACEMENTS = [
    ("Amazing landmarks", "Amazing places"),
    ("Amazinglandmarks", "Amazing places"),
    ("Unit 1 — Amazing landmarks", "Unit 1 — Amazing places"),
    ("Unit 1 Amazing landmarks", "Unit 1 Amazing places"),
    ("神奇的地标", "奇妙之地"),
    ("壮美的地标", "奇妙之地"),
    ("What famous landmarks do you know?", "What amazing places do you know?"),
    ("你知道哪些著名地标？", "你知道哪些奇妙的地方？"),
    ("你知道哪些著名的地标？", "你知道哪些奇妙的地方？"),
    ("famous landmarks and talk about them", "amazing places and talk about them"),
    ("我能列举一些著名地标并进行介绍", "我能列举一些奇妙的地方并进行介绍"),
    ("famous landmarks in China and abroad", "amazing places in China and abroad"),
]

PART_A_REPLACEMENTS = [
    ("Zhang Peng is talking with John.", "Zhang Peng is talking with Leo."),
    ("张鹏正在和约翰交谈", "张鹏正在和利奥交谈"),
    ("Hi, Peter!", "Hi, Leo!"),
    ("Hi Peter!", "Hi Leo!"),
    ("Peter:", "Leo:"),
    ("Peter ", "Leo "),
    (", Peter?", ", Leo?"),
    (", Peter.", ", Leo."),
    ("What did you do, Peter?", "What did you do, Leo?"),
    ("Peter visited", "Leo visited"),
    ("彼得：", "利奥："),
    ("彼得", "利奥"),
    ("It's 21,000 kilometres in all", "It's about 21,000 kilometres long"),
    ("它全长21,000公里", "它全长约21,000公里"),
    ("21,000 kilometres in all", "about 21,000 kilometres long"),
]


def apply_replacements(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def patch_file(path: Path, extra: list[tuple[str, str]] | None = None) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    updated = apply_replacements(original, TITLE_REPLACEMENTS)
    if extra:
        updated = apply_replacements(updated, extra)
    if path.name == "u1-p011.html":
        # Interview activity keeps student named John — restore if overwritten
        updated = updated.replace("Leo often plays football", "John often plays football")
        updated = updated.replace("利奥经常在周末", "约翰经常在周末")
        updated = updated.replace("利奥　　我经常", "约翰　　我经常")
        updated = updated.replace("Interview and report 示例： Leo often", "Interview and report 示例： John often")
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def patch_json_unit1_title(obj, path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("title", "badge", "prompt", "example", "en", "zh", "explainCorrect") and isinstance(v, str):
                for old, new in TITLE_REPLACEMENTS:
                    obj[k] = obj[k].replace(old, new)
                for old, new in PART_A_REPLACEMENTS:
                    if "Binbin" not in obj[k]:  # keep Part B Binbin
                        obj[k] = obj[k].replace(old, new)
            else:
                patch_json_unit1_title(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            patch_json_unit1_title(item, f"{path}[{i}]")


def patch_supplement_unit1() -> int:
    path = ROOT / "data/practice/supplement.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for item in data.get("cards", data if isinstance(data, list) else []):
        if not isinstance(item, dict) or item.get("unit") != 1:
            continue
        for key in ("example", "front", "zh"):
            if key not in item or not isinstance(item[key], str):
                continue
            old = item[key]
            new = apply_replacements(old, TITLE_REPLACEMENTS)
            if "Binbin:" in old:
                new = new.replace("Leo:", "Binbin:").replace("利奥：", "彬彬：")
            if new != old:
                item[key] = new
                n += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return n


def main() -> None:
    changed: list[str] = []

    part_a_files = U1_READING + U1_KNOWLEDGE
    for p in part_a_files:
        if patch_file(p, PART_A_REPLACEMENTS) and str(p) not in changed:
            changed.append(str(p.relative_to(ROOT)))

    for rel in ("app.js", "index.html", "FINAL_PRODUCT_MANUAL.md", "word-sources/Unit1_课文双语.csv"):
        p = ROOT / rel
        extra = PART_A_REPLACEMENTS if rel.endswith(".csv") else None
        if patch_file(p, extra):
            changed.append(rel)

    # knowledge_u12_sections.py
    sec = ROOT / "scripts/knowledge_u12_sections.py"
    if patch_file(sec, PART_A_REPLACEMENTS):
        changed.append("scripts/knowledge_u12_sections.py")

    # textbook_data.json
    td = ROOT / "textbook_data.json"
    if td.exists():
        data = json.loads(td.read_text(encoding="utf-8"))
        for u in data:
            if u.get("num") == 1:
                u["title"] = "Amazing places"
        td.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append("textbook_data.json")

    # reading-bank: title + Part A only in unit 1 pages
    rb = ROOT / "data/study-hub/reading-bank.json"
    if rb.exists():
        bank = json.loads(rb.read_text(encoding="utf-8"))
        for page in bank.get("pages", []):
            if page.get("unit") != 1:
                continue
            for old, new in TITLE_REPLACEMENTS:
                if "title" in page:
                    page["title"] = page["title"].replace(old, new)
            for block in page.get("blocks", []):
                for sent in block.get("sentences", []):
                    for old, new in TITLE_REPLACEMENTS:
                        if "en" in sent:
                            sent["en"] = sent["en"].replace(old, new)
                        if "zh" in sent:
                            sent["zh"] = sent["zh"].replace(old, new)
                    pid = page.get("id", "")
                    if pid in ("u1-p011", "u1-p005", "u1-p009", "intro-p005"):
                        for old, new in PART_A_REPLACEMENTS:
                            if "en" in sent and "Binbin" not in sent["en"]:
                                sent["en"] = sent["en"].replace(old, new)
                            if "zh" in sent and "彬彬" not in sent["zh"]:
                                sent["zh"] = sent["zh"].replace(old, new)
                        if "en" in sent:
                            sent["en"] = sent["en"].replace("Leo often plays", "John often plays")
                        if "zh" in sent:
                            sent["zh"] = sent["zh"].replace("利奥经常在周末", "约翰经常在周末")
        rb.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append("data/study-hub/reading-bank.json")

    patch_supplement_unit1()
    changed.append("data/practice/supplement.json (unit 1)")

    print(f"[OK] Updated {len(changed)} targets:")
    for c in changed:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
