#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge Unit 1-2 practice items into banks — never delete existing by unit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIZ_BANK = ROOT / "data" / "question-banks" / "quiz-bank.json"
FILL_BANK = ROOT / "data" / "question-banks" / "fillblank-bank.json"
RELEASE_QUIZ = ROOT / "release" / "data" / "question-banks" / "quiz-bank.json"
RELEASE_FILL = ROOT / "release" / "data" / "question-banks" / "fillblank-bank.json"

# New questions only (ids not in release baseline)
NEW_QUIZ = [
    {
        "id": "u1a-2",
        "unit": 1,
        "part": "A",
        "badge": "Unit 1 Part A 课文精练",
        "prompt": "It was great! I ___ the Great Wall.",
        "options": ["climb", "climbed", "climbing", "climbs"],
        "answer": "climbed",
        "explainCorrect": "描述上周末经历，climb 用过去式 climbed。",
        "optionReasons": {
            "climb": "原形不能单独表示过去。",
            "climbed": "正确。",
            "climbing": "现在分词不能作谓语。",
            "climbs": "三单现在时不合语境。",
        },
    },
    {
        "id": "u1a-3",
        "unit": 1,
        "part": "A",
        "badge": "Unit 1 Part A 课文精练",
        "prompt": "Please ___ me some pictures.",
        "options": ["send", "sent", "sending", "sends"],
        "answer": "send",
        "explainCorrect": "祈使句 Please 后接动词原形 send。",
        "optionReasons": {
            "send": "正确。",
            "sent": "过去式不能用于祈使句。",
            "sending": "分词不能单独作谓语。",
            "sends": "第三人称单数形式错误。",
        },
    },
    {
        "id": "u1b-2",
        "unit": 1,
        "part": "B",
        "badge": "Unit 1 Part B 课文精练",
        "prompt": "Where did you go over the summer holidays, Binbin?",
        "options": [
            "I go to Xi'an with my family.",
            "I went to Xi'an with my family.",
            "I going to Xi'an with my family.",
            "I will went to Xi'an with my family.",
        ],
        "answer": "I went to Xi'an with my family.",
        "explainCorrect": "回答过去旅行用 went。",
        "optionReasons": {
            "I go to Xi'an with my family.": "一般现在时不合过去语境。",
            "I went to Xi'an with my family.": "正确。",
            "I going to Xi'an with my family.": "缺少 be 动词。",
            "I will went to Xi'an with my family.": "will 后不能接 went。",
        },
    },
    {
        "id": "u2a-2",
        "unit": 2,
        "part": "A",
        "badge": "Unit 2 Part A 课文精练",
        "prompt": "We cleaned the house and ___ fu on the door.",
        "options": ["paste", "pasted", "pasting", "pastes"],
        "answer": "pasted",
        "explainCorrect": "与 cleaned 并列，用过去式 pasted。",
        "optionReasons": {
            "paste": "原形与 cleaned 时态不一致。",
            "pasted": "正确。",
            "pasting": "分词不能并列作谓语。",
            "pastes": "三单形式错误。",
        },
    },
    {
        "id": "u2b-2",
        "unit": 2,
        "part": "B",
        "badge": "Unit 2 Part B 课文精练",
        "prompt": "I liked watching the ___.",
        "options": ["run", "runs", "runners", "running"],
        "answer": "runners",
        "explainCorrect": "课文：I liked watching the runners.",
        "optionReasons": {
            "run": "动词原形不能作 watching 的宾语。",
            "runs": "三单形式不合句意。",
            "runners": "正确，参赛者。",
            "running": "动名词虽可说，但课文用 runners。",
        },
    },
]

NEW_FILL = [
    {
        "id": "fb-u1-06",
        "unit": 1,
        "part": "B",
        "type": "noun",
        "prompt": "There are over seven thousand ___ warriors.",
        "clue": "中文：陶制的（黏土）。",
        "answer": "clay",
        "analysis": "clay warriors 陶俑。",
    },
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_by_id(existing: list[dict], incoming: list[dict], prefer: str = "existing") -> list[dict]:
    """Merge question lists by id. prefer='existing' keeps old when id clashes."""
    by_id: dict[str, dict] = {}
    order: list[str] = []
    for item in existing:
        iid = item.get("id", "")
        if iid:
            by_id[iid] = item
            if iid not in order:
                order.append(iid)
    for item in incoming:
        iid = item.get("id", "")
        if not iid:
            continue
        if iid in by_id and prefer == "existing":
            continue
        if iid not in by_id:
            order.append(iid)
        by_id[iid] = item
    return [by_id[i] for i in order if i in by_id]


def rebuild_bank(target: Path, baseline: Path, new_items: list[dict]) -> tuple[int, int]:
    """Restore baseline U1/U2 from release, merge current file, then add new items."""
    base = load_json(baseline)
    current = load_json(target) if target.exists() else base
    base_ids = {q["id"] for q in base.get("questions", [])}
    # Keep all non-U1/U2 from current + full baseline as foundation
    u12_base = [q for q in base.get("questions", []) if q.get("unit") in (1, 2)]
    other = [q for q in current.get("questions", []) if q.get("unit") not in (1, 2)]
    merged = merge_by_id(u12_base, [q for q in current.get("questions", []) if q.get("unit") in (1, 2)])
    merged = merge_by_id(merged, new_items, prefer="existing")
    final = other + merged
    # Stable sort: by unit then id
    final.sort(key=lambda q: (q.get("unit", 99), q.get("id", "")))
    target.write_text(
        json.dumps({**base, "questions": final}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    added = len([q for q in new_items if q["id"] not in base_ids])
    return len(merged), added


def main() -> None:
    n_quiz, add_quiz = rebuild_bank(QUIZ_BANK, RELEASE_QUIZ, NEW_QUIZ)
    n_fill, add_fill = rebuild_bank(FILL_BANK, RELEASE_FILL, NEW_FILL)
    print(f"quiz-bank: {n_quiz} U1/U2 items ({add_quiz} new ids added)")
    print(f"fillblank-bank: {n_fill} U1/U2 items ({add_fill} new ids added)")
    print("app.js: NOT auto-patched (use textbook_catalog data; avoid regex corruption)")


if __name__ == "__main__":
    main()
