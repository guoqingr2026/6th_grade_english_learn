#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build practice supplement from appendix 2–5 + grammar pages (OR-merge, never delete banks)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from appendix_parser import (  # noqa: E402
    parse_appendix_expressions,
    parse_appendix_words,
    parse_catalog,
    plain_lines,
    reading_sentence_pairs,
)
from textbook_catalog import UNITS  # noqa: E402

OUT = ROOT / "data" / "practice" / "supplement.json"
QUIZ_BANK = ROOT / "data" / "question-banks" / "quiz-bank.json"
FILL_BANK = ROOT / "data" / "question-banks" / "fillblank-bank.json"
READING_DIR = ROOT / "data" / "study-hub" / "library" / "reading"

IRREGULAR = {
    "be": ("was/were", "been"),
    "go": ("went", "gone"),
    "see": ("saw", "seen"),
    "eat": ("ate", "eaten"),
    "take": ("took", "taken"),
    "run": ("ran", "run"),
    "wake": ("woke", "woken"),
    "begin": ("began", "begun"),
    "win": ("won", "won"),
    "buy": ("bought", "bought"),
    "spend": ("spent", "spent"),
    "come": ("came", "come"),
    "make": ("made", "made"),
    "send": ("sent", "sent"),
    "feel": ("felt", "felt"),
    "hurt": ("hurt", "hurt"),
    "have": ("had", "had"),
    "get": ("got", "got/gotten"),
    "do": ("did", "done"),
    "say": ("said", "said"),
    "tell": ("told", "told"),
    "think": ("thought", "thought"),
    "find": ("found", "found"),
    "give": ("gave", "given"),
    "know": ("knew", "known"),
    "leave": ("left", "left"),
    "meet": ("met", "met"),
    "put": ("put", "put"),
    "read": ("read", "read"),
    "sit": ("sat", "sat"),
    "sleep": ("slept", "slept"),
    "speak": ("spoke", "spoken"),
    "stand": ("stood", "stood"),
    "swim": ("swam", "swum"),
    "teach": ("taught", "taught"),
    "understand": ("understood", "understood"),
    "wear": ("wore", "worn"),
    "write": ("wrote", "written"),
}


def merge_by_id(existing: list[dict], new_items: list[dict], prefer: str = "existing") -> list[dict]:
    out: dict[str, dict] = {}
    for item in existing:
        if item.get("id"):
            out[str(item["id"])] = item
    for item in new_items:
        iid = str(item.get("id", ""))
        if not iid:
            continue
        if iid not in out or prefer == "new":
            out[iid] = item
    return list(out.values())


def load_bank(path: Path, key: str) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get(key, []))


def covered_words(quiz: list[dict], fill: list[dict]) -> set[str]:
    text = json.dumps(quiz + fill, ensure_ascii=False).lower()
    return set(re.findall(r"[a-z]{4,}", text))


def parse_appendix5_irregular() -> list[dict]:
    rows: list[dict] = []
    pending_base: str | None = None
    for fname in ("appendix-p099.html", "appendix-p100.html", "appendix-p101.html"):
        path = READING_DIR / fname
        if not path.exists():
            continue
        for line in plain_lines(path):
            if re.match(r"^(Base form|原形)", line, re.I):
                continue
            parts = re.split(r"\s{2,}|\t", line.strip())
            if len(parts) >= 3 and re.match(r"^[a-z]", parts[0], re.I):
                base = parts[0].lower().strip()
                past = parts[1].strip()
                part = parts[2].strip()
                rows.append({"base": base, "past": past, "participle": part, "unit": 0})
                continue
            m = re.match(r"^([a-z][a-z ]*?)\s+([a-z/]+)\s+([a-z/]+)$", line.strip(), re.I)
            if m:
                rows.append({
                    "base": m.group(1).lower().strip(),
                    "past": m.group(2).strip(),
                    "participle": m.group(3).strip(),
                    "unit": 0,
                })
    return rows


def parse_grammar_appendix3() -> list[dict]:
    """Appendix 3 grammar overview from intro-p006 / intro-p007."""
    points: list[dict] = []
    for unit in UNITS:
        u = unit["num"]
        gd = unit.get("grammar_discover", {})
        title = gd.get("title") or f"Unit {u} 语法"
        hints = gd.get("hints", [])
        observe = gd.get("observe", [])
        examples = [en for en, _zh in observe[:3]] or hints[:2]
        rule = "；".join(hints) if hints else title
        points.append({
            "id": f"supp-grammar-u{u}",
            "unit": u,
            "title": f"Unit {u} {title}",
            "rule": rule,
            "examples": examples[:4] or [f"Unit {u} grammar example."],
        })
    # intro pages extra lines
    for fname in ("intro-p006.html", "intro-p007.html"):
        for line in plain_lines(READING_DIR / fname):
            if line.startswith("Grammar —"):
                continue
            m = re.match(r"^Unit (\d+)", line, re.I)
            if m and "Grammar" in line:
                continue
    return points


def build_vocab_cards() -> list[dict]:
    cards: list[dict] = []
    words_by_unit = parse_appendix_words()
    for unit in UNITS:
        u = unit["num"]
        pairs = reading_sentence_pairs(u, "part-a") + reading_sentence_pairs(u, "part-b")
        for w in words_by_unit.get(u, []):
            example = "—"
            for en, _zh in pairs:
                if w.word.lower().split()[0] in en.lower():
                    example = en[:120]
                    break
            cards.append({
                "id": f"supp-vocab-u{u}-{re.sub(r'[^a-z0-9]+', '-', w.word.lower())[:40]}",
                "unit": u,
                "category": f"附录2 · P.{w.page}",
                "front": w.display_word,
                "ipa": w.ipa,
                "zh": w.gloss,
                "example": example,
                "exampleZh": "",
                "image": "",
            })
    return cards


def build_phrases() -> list[dict]:
    phrases: list[dict] = []
    for unit in UNITS:
        u = unit["num"]
        for en, zh in unit.get("part_a_phrases", []) + unit.get("part_b_phrases", []):
            phrases.append({
                "id": f"supp-phrase-u{u}-{hash(en) & 0xFFFFFF:06x}",
                "unit": u,
                "scene": f"Unit {u} 讲读",
                "en": en,
                "zh": zh,
            })
        for expr in parse_appendix_expressions().get(u, []):
            phrases.append({
                "id": f"supp-expr-u{u}-{hash(expr.en) & 0xFFFFFF:06x}",
                "unit": u,
                "scene": f"Unit {u} 附录四",
                "en": expr.en,
                "zh": expr.zh,
            })
    return phrases


def build_quiz_and_fill(existing_quiz: list[dict], existing_fill: list[dict]) -> tuple[list[dict], list[dict]]:
    quiz: list[dict] = []
    fill: list[dict] = []
    covered = covered_words(existing_quiz, existing_fill)
    words_by_unit = parse_appendix_words()

    for unit in UNITS:
        u = unit["num"]
        for w in words_by_unit.get(u, []):
            key = w.word.lower().split()[0]
            if len(key) < 4 or key in covered:
                continue
            wid = re.sub(r"[^a-z0-9]+", "-", w.word.lower())[:30]
            fill.append({
                "id": f"supp-fb-u{u}-{wid}",
                "unit": u,
                "part": "A",
                "prompt": f"Appendix 2 word (Unit {u}): ___ ({w.gloss})",
                "hintZh": w.gloss,
                "answers": [w.word.lstrip("★").strip()],
            })
            quiz.append({
                "id": f"supp-q-u{u}-{wid}",
                "unit": u,
                "part": "A",
                "badge": f"附录2 Unit {u}",
                "prompt": f"Which word means 「{w.gloss}」?",
                "options": [w.word.lstrip("★"), "unknown", "holiday", "energy"][:4],
                "answer": w.word.lstrip("★"),
                "explainCorrect": f"附录2：{w.word} = {w.gloss}",
                "optionReasons": {},
            })
            covered.add(key)
    return quiz, fill


def build_verb_triples() -> list[dict]:
    path = ROOT / "data" / "practice" / "irregular-verbs.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    triples = []
    for v in data.get("verbs", []):
        triples.append({
            "id": v["id"],
            "unit": 0,
            "base": v["base"],
            "past": v["past"],
            "participle": v["participle"],
            "usage": f"附录5：{v.get('zh', '')}",
            "sentence": f"{v['base']} — {v['past']} — {v['participle']}",
            "fillPrompt": f"附录5：{v['base']} 的过去式是 ___",
            "fillAnswer": str(v["past"]).split("/")[0].strip(),
            "fillClue": "Irregular verbs",
        })
    return triples


def main() -> None:
    existing_quiz = load_bank(QUIZ_BANK, "questions")
    existing_fill = load_bank(FILL_BANK, "questions")

    quiz_new, fill_new = build_quiz_and_fill(existing_quiz, existing_fill)
    supplement = {
        "version": 1,
        "note": "OR-merge at runtime; never replaces default banks wholesale",
        "vocabularyCards": build_vocab_cards(),
        "phrases": build_phrases(),
        "grammarPoints": parse_grammar_appendix3(),
        "quiz": quiz_new,
        "fillblank": fill_new,
        "verbTriples": build_verb_triples(),
        "catalogGrammar": {
            f"u{k[0]}-{k[1]}": {"focus": v.focus_zh, "grammar": v.grammar_zh}
            for k, v in parse_catalog().items()
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        supplement["quiz"] = merge_by_id(old.get("quiz", []), supplement["quiz"], prefer="existing")
        supplement["fillblank"] = merge_by_id(old.get("fillblank", []), supplement["fillblank"], prefer="existing")
        supplement["vocabularyCards"] = merge_by_id(
            old.get("vocabularyCards", []), supplement["vocabularyCards"], prefer="existing"
        )
        supplement["phrases"] = merge_by_id(old.get("phrases", []), supplement["phrases"], prefer="existing")
        supplement["grammarPoints"] = merge_by_id(
            old.get("grammarPoints", []), supplement["grammarPoints"], prefer="existing"
        )
        supplement["verbTriples"] = merge_by_id(
            old.get("verbTriples", []), supplement["verbTriples"], prefer="existing"
        )

    OUT.write_text(json.dumps(supplement, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] supplement -> {OUT}")
    print(
        f"  vocab {len(supplement['vocabularyCards'])}, phrases {len(supplement['phrases'])}, "
        f"grammar {len(supplement['grammarPoints'])}, quiz +{len(quiz_new)}, fill +{len(fill_new)}, "
        f"verbs {len(supplement['verbTriples'])}"
    )


if __name__ == "__main__":
    main()
