#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Report appendix 2–5 coverage in practice data (read-only, no deletes)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from appendix_parser import parse_appendix_expressions, parse_appendix_words  # noqa: E402

QUIZ = ROOT / "data" / "question-banks" / "quiz-bank.json"
FILL = ROOT / "data" / "question-banks" / "fillblank-bank.json"
SUPP = ROOT / "data" / "practice" / "supplement.json"


def load_items() -> str:
    chunks: list[str] = []
    for path, key in ((QUIZ, "questions"), (FILL, "questions")):
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            chunks.append(json.dumps(data.get(key, []), ensure_ascii=False))
    if SUPP.exists():
        supp = json.loads(SUPP.read_text(encoding="utf-8"))
        for k in ("quiz", "fillblank", "vocabularyCards", "phrases", "verbTriples"):
            chunks.append(json.dumps(supp.get(k, []), ensure_ascii=False))
    return " ".join(chunks).lower()


def main() -> None:
    blob = load_items()
    words = parse_appendix_words()
    exprs = parse_appendix_expressions()

    print("=" * 60)
    print("Appendix 2–5 coverage report (read-only)")
    print("=" * 60)

    missing_words: list[str] = []
    for u, lst in words.items():
        for w in lst:
            token = w.word.lstrip("★").lower().split()[0]
            if len(token) >= 4 and token not in blob:
                missing_words.append(f"U{u} {w.word}")

    missing_expr: list[str] = []
    for u, lst in exprs.items():
        for e in lst:
            token = e.en.lower().split()[0]
            if len(token) >= 4 and token not in blob:
                missing_expr.append(f"U{u} {e.en}")

    total_w = sum(len(v) for v in words.values())
    total_e = sum(len(v) for v in exprs.values())
    hit_w = total_w - len(missing_words)
    hit_e = total_e - len(missing_expr)

    print(f"Appendix 2 words: {hit_w}/{total_w} referenced in banks+supplement")
    if missing_words[:15]:
        print("  sample gaps:", ", ".join(missing_words[:15]))
        if len(missing_words) > 15:
            print(f"  ... and {len(missing_words) - 15} more")

    print(f"Appendix 4 expressions: {hit_e}/{total_e} referenced")
    if missing_expr[:10]:
        print("  sample gaps:", ", ".join(missing_expr[:10]))

    print("\nRun `python scripts/build_practice_supplement.py` to OR-merge gaps into supplement.json")

    irreg_path = ROOT / "data" / "practice" / "irregular-verbs.json"
    if irreg_path.exists():
        irreg = json.loads(irreg_path.read_text(encoding="utf-8"))
        n = len(irreg.get("verbs", []))
        print(f"Appendix 5 irregular verbs file: {n}/47")
        if n != 47:
            print("  [WARN] irregular-verbs.json count mismatch")
    return 0 if not missing_words and not missing_expr else 1


if __name__ == "__main__":
    raise SystemExit(main())
