#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse Appendix 2 (words) and Appendix 4 (expressions) from reading library HTML."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING_DIR = ROOT / "data" / "study-hub" / "library" / "reading"
PAGE_MAP = ROOT / "data" / "study-hub" / "pdf-page-map.json"
INTRO_CATALOG = READING_DIR / "intro-p005.html"

# Absolute printed textbook page where each unit starts (from 目录一)
UNIT_ABS_START = {1: 2, 2: 14, 3: 26, 4: 38, 5: 50, 6: 62}

WORD_LINE_RE = re.compile(
    r"^\*?(?P<word>.+?)\s+/(?P<ipa>[^/]+)/\s*(?P<gloss>.+?)\s+p\.\s*(?P<page>\d+)\s*$",
    re.IGNORECASE,
)
PAGE_RE = re.compile(r"p\.\s*(\d+)", re.I)
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class AppendixWord:
    word: str
    ipa: str
    gloss: str
    page: int
    level2: bool
    unit: int

    @property
    def pos_page(self) -> str:
        """词性栏备注课本页码，如 P.4"""
        return f"P.{self.page}"

    @property
    def display_word(self) -> str:
        return f"★{self.word}" if self.level2 else self.word


@dataclass
class AppendixExpression:
    en: str
    zh: str
    unit: int
    page: str = ""


@dataclass
class CatalogPart:
    question_en: str
    question_zh: str
    focus_zh: str
    grammar_zh: str = ""


def strip_html(text: str) -> str:
    return unescape(TAG_RE.sub("", text)).replace("\xa0", " ").strip()


def plain_lines(html_path: Path) -> list[str]:
    if not html_path.exists():
        return []
    raw = html_path.read_text(encoding="utf-8")
    chunks = re.split(r"(?=<(?:p|h[1-6]|hr)\b)", raw, flags=re.I)
    lines: list[str] = []
    for chunk in chunks:
        text = strip_html(chunk)
        if text:
            lines.append(text)
    if len(lines) <= 1:
        text = strip_html(raw)
        lines = [ln.strip() for ln in re.split(r"[\n\r]+", text) if ln.strip()]
    return lines


def load_page_map() -> dict:
    return json.loads(PAGE_MAP.read_text(encoding="utf-8"))


def part_abs_pages(unit: int, part_key: str) -> set[int]:
    """Absolute printed book pages for a unit part."""
    pm = load_page_map()
    u = pm.get("units", {}).get(str(unit), {})
    sec = u.get(part_key, {})
    rel = sec.get("bookPages", [])
    start = UNIT_ABS_START.get(unit, 2)
    book_start = u.get("bookPageStart", 2)
    return {start + p - book_start for p in rel}


def shorten_example(en: str, max_words: int = 20) -> str:
    """Trim example to ≤max_words; drop speaker labels."""
    en = re.sub(r"^[A-Za-z][A-Za-z .'-]{0,20}:\s*", "", en.strip())
    en = re.sub(r"\s+", " ", en)
    words = en.split()
    if len(words) <= max_words:
        return en
    return " ".join(words[:max_words]) + "…"


def _parse_word_line(line: str, unit: int) -> AppendixWord | None:
    level2 = line.strip().startswith("*")
    clean = line.strip().lstrip("*").strip()
    # gingerbread /'dʒɪndʒəbred/ house 姜饼屋 p. 4  (before generic pattern)
    m2 = re.match(
        r"^(\S+)\s+/([^/]+)/\s+(\S+)\s+(.+?)\s+p\.\s*(\d+)\s*$",
        clean,
    )
    if m2 and not m2.group(3).startswith("/") and re.search(r"[\u4e00-\u9fff]", m2.group(4)):
        word = f"{m2.group(1)} {m2.group(3)}"
        return AppendixWord(word, m2.group(2).strip(), m2.group(4).strip(), int(m2.group(5)), level2, unit)
    m3 = re.match(
        r"^(\S+)\s+/([^/]+)/\s+(\S+)\s+/([^/]+)/\s+(.+?)\s+p\.\s*(\d+)\s*$",
        clean,
    )
    if m3:
        word = f"{m3.group(1)} {m3.group(3)}"
        return AppendixWord(word, f"{m3.group(2).strip()} {m3.group(4).strip()}", m3.group(5).strip(), int(m3.group(6)), level2, unit)
    m = WORD_LINE_RE.match(clean)
    if m:
        return AppendixWord(
            m.group("word").strip(),
            m.group("ipa").strip(),
            m.group("gloss").strip(),
            int(m.group("page")),
            level2,
            unit,
        )
    return None


def parse_appendix_words() -> dict[int, list[AppendixWord]]:
    """Parse appendix-p088.html (+ p089 for later units)."""
    by_unit: dict[int, list[AppendixWord]] = {i: [] for i in range(1, 7)}
    current = 1
    for fname in ("appendix-p088.html", "appendix-p089.html", "appendix-p090.html", "appendix-p091.html"):
        for line in plain_lines(READING_DIR / fname):
            m_unit = re.match(r"^Unit\s+(\d+)$", line, re.I)
            if m_unit:
                current = int(m_unit.group(1))
                continue
            if "Words in Each" in line or line.startswith("附录") or "二级词" in line:
                continue
            w = _parse_word_line(line, current)
            if w:
                by_unit[current].append(w)
    return by_unit


def parse_appendix_expressions() -> dict[int, list[AppendixExpression]]:
    """Parse appendix 4 (p096–p098). EN line followed by ZH line."""
    by_unit: dict[int, list[AppendixExpression]] = {i: [] for i in range(1, 7)}
    current = 1
    pending_en: str | None = None
    for fname in ("appendix-p096.html", "appendix-p097.html", "appendix-p098.html"):
        for line in plain_lines(READING_DIR / fname):
            if re.match(r"^Unit\s+\d+$", line, re.I):
                current = int(re.search(r"\d+", line).group())
                pending_en = None
                continue
            if line.startswith("—") or line == "Irregular Verbs 不规则动词":
                pending_en = None
                continue
            if re.search(r"[\u4e00-\u9fff]", line):
                if pending_en:
                    by_unit[current].append(AppendixExpression(pending_en, line, current))
                    pending_en = None
            elif len(line) > 2 and not line.startswith("（"):
                pending_en = line
    return by_unit


def words_for_part(unit: int, part_key: str) -> list[AppendixWord]:
    pages = part_abs_pages(unit, part_key)
    all_words = parse_appendix_words().get(unit, [])
    if part_key == "reading":
        return [w for w in all_words if w.page in pages] or all_words
    matched = [w for w in all_words if w.page in pages]
    return matched if matched else all_words[: max(8, len(all_words) // 2)]


def expressions_for_part(unit: int, part_key: str) -> list[AppendixExpression]:
    exprs = parse_appendix_expressions().get(unit, [])
    pages = part_abs_pages(unit, part_key)
    default_page = f"P.{min(pages)}" if pages else "P.—"
    if part_key in ("part-a", "part-c"):
        subset = exprs[: max(4, len(exprs) // 2)]
    elif part_key == "part-b":
        mid = len(exprs) // 2
        subset = exprs[mid : mid + max(4, len(exprs) // 3)] or exprs
    else:
        subset = exprs
    for e in subset:
        e.page = default_page
    return subset


def reading_sentence_pairs(unit: int, part_key: str) -> list[tuple[str, str]]:
    """Bilingual pairs from reading HTML for unit/part."""
    pm = load_page_map()
    u = pm.get("units", {}).get(str(unit), {})
    sec = u.get(part_key, {})
    pdf_pages = sec.get("pdfPages", [])
    pairs: list[tuple[str, str]] = []
    for png in pdf_pages:
        path = READING_DIR / f"u{unit}-p{png:03d}.html"
        if not path.exists():
            continue
        lines = plain_lines(path)
        i = 0
        while i < len(lines):
            en = lines[i]
            if i + 1 < len(lines) and re.search(r"[\u4e00-\u9fff]", lines[i + 1]) and not re.search(
                r"[\u4e00-\u9fff]", en
            ):
                if len(en) > 8 and "🔴" not in en and "💬" not in en[:3]:
                    pairs.append((en, lines[i + 1]))
                i += 2
            else:
                i += 1
    return pairs


def find_example_for_word(word: str, pairs: list[tuple[str, str]]) -> str:
    key = word.lower().split()[0]
    for en, _zh in pairs:
        if key in en.lower() or word.lower() in en.lower():
            return shorten_example(en)
    for en, _zh in pairs:
        if any(tok in en.lower() for tok in word.lower().split() if len(tok) > 3):
            return shorten_example(en)
    return shorten_example(pairs[0][0]) if pairs else "—"


def parse_catalog() -> dict[tuple[int, str], CatalogPart]:
    """目录一 (intro-p005) part focus per unit."""
    lines = plain_lines(INTRO_CATALOG)
    out: dict[tuple[int, str], CatalogPart] = {}
    unit = 0
    unit_grammar = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^Unit (\d+)", line, re.I)
        if m:
            unit = int(m.group(1))
            unit_grammar = ""
            i += 1
            continue
        if line.startswith("Grammar"):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            unit_grammar = nxt if re.search(r"[\u4e00-\u9fff]", nxt) else line
            for pk in ("part-a", "part-b", "part-c"):
                if (unit, pk) in out:
                    out[(unit, pk)].grammar_zh = unit_grammar
            i += 2
            continue
        for part_key, prefix in (("part-a", "Part A"), ("part-b", "Part B"), ("part-c", "Part C")):
            if line.startswith(prefix):
                focus = lines[i + 1] if i + 1 < len(lines) and re.search(r"[\u4e00-\u9fff]", lines[i + 1]) else ""
                out[(unit, part_key)] = CatalogPart("", "", focus, unit_grammar)
        i += 1
    return out
