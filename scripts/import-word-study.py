#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import bilingual study content from Word files:
  word-sources/Unit1_课文词汇重点句型_双语学习资料.docx

Primary format (recommended) — use Page markers, no manual part tags:
  Page 11
  EN: How was your weekend?
  ZH: 你周末过得怎么样?

  Page 12
  ...

Pages are auto-mapped to Part A/B/C/Reading via data/study-hub/pdf-page-map.json.

Legacy format still supported:
  === part-a ===
  @pages: 11, 12
  EN: ...
  ZH: ...

Run: python scripts/import-word-study.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORD_DIRS = [
    ROOT / "word-sources",
    ROOT / "data" / "study-hub" / "word-sources",
]
OUT = ROOT / "data" / "study-hub" / "word-import.json"
PAGE_MAP_PATH = ROOT / "data" / "study-hub" / "pdf-page-map.json"

SECTION_RE = re.compile(r"^===\s*(.+?)\s*===\s*$", re.I)
PAGES_RE = re.compile(r"^@pages?\s*[:：]\s*(.+)$", re.I)
EN_RE = re.compile(r"^(?:EN|英文)\s*[:：]\s*(.+)$", re.I)
ZH_RE = re.compile(r"^(?:ZH|中文)\s*[:：]\s*(.+)$", re.I)
# Page 11 | Page: 11 | PAGE 11 | P. 11 | P11 | 第11页 | 页11
PAGE_RE = re.compile(
    r"^(?:page|p\.?|页|第)\s*[:：]?\s*(\d{1,3})\s*(?:页)?\s*$",
    re.I,
)
PAGE_COMPACT_RE = re.compile(r"^page\s*(\d{1,3})\s*$", re.I)
HTML_LINE_RE = re.compile(r"</?(?:h\d|p|div|span|table|ul|ol|li|blockquote|br)\b", re.I)
KNOWLEDGE_HINT_RE = re.compile(r"知识点精讲|请在此编写精讲", re.I)
SKIP_LINE_RE = re.compile(
    r"^(说明[:：]|Unit\s+\d+\s+课文|保存后|系统按|无需手写)",
    re.I,
)
UNIT_PART_ORDER = ["unit-start", "unit-next", "part-a", "part-b", "part-c", "reading"]


def find_unit_sources() -> list[tuple[int, Path, str]]:
    """Return (unit, path, kind). CSV only — edit Word then Save As CSV."""
    found: dict[int, Path] = {}
    for d in WORD_DIRS:
        if not d.exists():
            continue
        for p in d.glob("Unit*.csv"):
            m = re.search(r"Unit\s*(\d+)", p.name, re.I)
            if m:
                found[int(m.group(1))] = p
    return sorted((u, p, "csv") for u, p in found.items())


def find_unit_files() -> list[tuple[int, Path]]:
    return [(u, p) for u, p, _ in find_unit_sources()]


def read_docx(path: Path) -> list[str]:
    from docx import Document

    doc = Document(str(path))
    lines: list[str] = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            lines.append(text)
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if not cells:
                continue
            if len(cells) >= 2 and re.search(r"[A-Za-z]", cells[0]):
                lines.append(f"EN: {cells[0]}")
                lines.append(f"ZH: {cells[1]}")
            else:
                lines.extend(cells)
    return lines


def parse_pages(raw: str) -> list[int]:
    nums = []
    for part in re.split(r"[,，\s]+", raw.strip()):
        part = part.strip()
        if part.isdigit():
            nums.append(int(part))
    return nums


def parse_page_marker(line: str) -> int | None:
    text = line.strip()
    m = PAGE_RE.match(text) or PAGE_COMPACT_RE.match(text)
    if m:
        return int(m.group(1))
    return None


def is_html_or_knowledge(line: str) -> bool:
    t = line.strip()
    if not t:
        return False
    if t.startswith("<") or HTML_LINE_RE.search(t):
        return True
    if KNOWLEDGE_HINT_RE.search(t):
        return True
    return False


def is_valid_reading_sentence(s: dict) -> bool:
    en = (s.get("en") or "").strip()
    zh = (s.get("zh") or "").strip()
    if is_html_or_knowledge(en):
        return False
    if not en and not zh:
        return False
    if en.startswith("说明：") or en.startswith("说明:"):
        return False
    return True


def clean_sentences(sentences: list[dict]) -> list[dict]:
    out = []
    for s in sentences:
        if not is_valid_reading_sentence(s):
            continue
        item = {k: v for k, v in s.items() if k != "tts"}
        out.append(item)
    return out


def read_csv(path: Path) -> list[str]:
    import csv

    lines: list[str] = []
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.strip():
        return lines
    rows = list(csv.reader(raw.splitlines()))
    if not rows:
        return lines

    def emit_page_lines(data_rows: list[list[str]], page_col: int, en_col: int, zh_col: int) -> None:
        last_page: int | None = None
        for row in data_rows:
            if len(row) <= page_col:
                continue
            pg_raw = (row[page_col] or "").strip()
            if not pg_raw.isdigit():
                continue
            pg = int(pg_raw)
            if pg != last_page:
                lines.append(f"Page {pg}")
                last_page = pg
            en = (row[en_col] or "").strip() if len(row) > en_col else ""
            zh = (row[zh_col] or "").strip() if len(row) > zh_col else ""
            if en:
                lines.append(f"EN: {en}")
            if zh:
                lines.append(f"ZH: {zh}")

    header = [c.strip().lower() for c in rows[0]]
    if header and header[0] in ("page", "页码", "pages"):
        fields = {h: i for i, h in enumerate(header)}
        pi = fields.get("page", fields.get("页码", fields.get("pages", 0)))
        ei = next((fields[k] for k in ("en", "english", "英文") if k in fields), 1)
        zi = next((fields[k] for k in ("zh", "chinese", "中文") if k in fields), 2)
        emit_page_lines(rows[1:], pi, ei, zi)
    else:
        emit_page_lines(rows, 0, 1, 2)
    return lines


def read_txt(path: Path) -> list[str]:
    return [ln.strip() for ln in path.read_text(encoding="utf-8-sig").splitlines() if ln.strip()]


def read_source(path: Path, kind: str) -> list[str]:
    if kind == "csv":
        return read_csv(path)
    if kind == "txt":
        return read_txt(path)
    return read_docx(path)


def flush_pending(pending_en: str, sentences: list[dict]) -> str:
    if pending_en and not is_html_or_knowledge(pending_en):
        sentences.append({"en": pending_en, "zh": ""})
    return ""


def parse_line_to_sentence(line: str, pending_en: str) -> tuple[str, dict | None]:
    if should_skip_line(line) or is_html_or_knowledge(line):
        return pending_en, None
    em = EN_RE.match(line)
    if em:
        out = None
        if pending_en:
            out = {"en": pending_en, "zh": ""}
        return em.group(1).strip(), out
    zm = ZH_RE.match(line)
    if zm:
        zh = zm.group(1).strip()
        if pending_en:
            return "", {"en": pending_en, "zh": zh}
        return "", {"en": "", "zh": zh, "type": "zh-only"}
    if "\t" in line:
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) >= 2 and re.search(r"[A-Za-z]", parts[0]):
            return "", {"en": parts[0], "zh": parts[1]}
    if is_chinese_line(line):
        if pending_en:
            return "", {"en": pending_en, "zh": line.strip()}
        return "", {"en": "", "zh": line.strip(), "type": "zh-only"}
    if is_english_line(line):
        out = None
        if pending_en:
            out = {"en": pending_en, "zh": ""}
        return line.strip(), out
    return pending_en, None


def parse_by_pages(lines: list[str]) -> dict[int, list[dict]]:
    """Parse document using Page N markers into page -> sentences."""
    by_page: dict[int, list[dict]] = {}
    current_page: int | None = None
    pending_en = ""

    for line in lines:
        pg = parse_page_marker(line)
        if pg is not None:
            if current_page is not None:
                pending_en = flush_pending(pending_en, by_page[current_page])
            current_page = pg
            by_page.setdefault(current_page, [])
            continue
        if SECTION_RE.match(line) or PAGES_RE.match(line) or should_skip_line(line):
            continue
        if current_page is None:
            continue
        pending_en, sent = parse_line_to_sentence(line, pending_en)
        if sent:
            by_page[current_page].append(sent)

    if current_page is not None:
        pending_en = flush_pending(pending_en, by_page[current_page])

    return {p: sents for p, sents in by_page.items() if sents}


def parse_sections(lines: list[str]) -> dict[str, dict]:
    sections: dict[str, dict] = {}
    current: str | None = None
    buf: list[str] = []
    pages: list[int] = []
    sentences: list[dict] = []
    pending_en = ""
    current_page: int | None = None

    def flush_sentences():
        nonlocal pending_en, sentences
        pending_en = flush_pending(pending_en, sentences)

    def save_section():
        nonlocal current, buf, pages, sentences, pending_en, current_page
        if not current:
            return
        flush_sentences()
        key = current.strip().lower()
        is_knowledge = key.startswith("knowledge-")
        body_key = key.replace("knowledge-", "") if is_knowledge else key
        entry = sections.setdefault(body_key, {"pages": pages, "sentences": [], "bodyHtml": ""})
        if pages:
            entry["pages"] = pages
        if is_knowledge:
            html = "\n".join(buf).strip()
            if html and not html.lstrip().startswith("<"):
                html = "".join(f"<p>{line}</p>" for line in buf if line.strip())
            entry["bodyHtml"] = html
        else:
            for s in sentences:
                if current_page and "page" not in s:
                    s = {**s, "page": current_page}
                entry["sentences"].append(s)
        buf = []
        pages = []
        sentences = []
        pending_en = ""
        current_page = None

    for line in lines:
        sm = SECTION_RE.match(line)
        if sm:
            save_section()
            current = sm.group(1).strip().lower()
            continue
        pm = PAGES_RE.match(line)
        if pm:
            pages = parse_pages(pm.group(1))
            continue
        pg = parse_page_marker(line)
        if pg is not None:
            flush_sentences()
            current_page = pg
            if pg not in pages:
                pages.append(pg)
            continue
        if current and current.startswith("knowledge-"):
            buf.append(line)
            continue
        pending_en, sent = parse_line_to_sentence(line, pending_en)
        if sent:
            if current_page:
                sent = {**sent, "page": current_page}
            sentences.append(sent)
    save_section()
    return sections


def load_page_map() -> dict:
    if not PAGE_MAP_PATH.exists():
        return {}
    return json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8"))


def unit_png_sequence(unit_num: int, page_map: dict) -> list[int]:
    unit = (page_map.get("units") or {}).get(str(unit_num)) or {}
    pages: list[int] = []
    for key in UNIT_PART_ORDER:
        sec = unit.get(key)
        if isinstance(sec, dict):
            pages.extend(sec.get("pdfPages") or [])
    return pages


def book_page_start(unit_num: int, page_map: dict) -> int:
    unit = (page_map.get("units") or {}).get(str(unit_num)) or {}
    return int(unit.get("bookPageStart") or page_map.get("bookPageStart") or 2)


def book_page_to_png(unit_num: int, book_page: int, page_map: dict) -> int | None:
    """课本印刷页码 → PNG 图册页码。Unit1 的 Page 2 → page-009.png"""
    seq = unit_png_sequence(unit_num, page_map)
    if not seq:
        return book_page
    start = book_page_start(unit_num, page_map)
    idx = book_page - start
    if 0 <= idx < len(seq):
        return seq[idx]
    if book_page in seq:
        return book_page
    return None


def png_to_book_page(unit_num: int, png_page: int, page_map: dict) -> int | None:
    seq = unit_png_sequence(unit_num, page_map)
    start = book_page_start(unit_num, page_map)
    try:
        return start + seq.index(png_page)
    except ValueError:
        return None


def print_page_offset(page_map: dict) -> int:
    return int(page_map.get("printPageOffset", 7))


def printed_page_to_png(printed: int, page_map: dict) -> int:
    """Global textbook printed page → PNG file number (page-NNN.png)."""
    p = int(printed)
    if p <= 8:
        return p
    return p + print_page_offset(page_map)


def resolve_page_ref(unit_num: int, page_ref: int, page_map: dict) -> tuple[int | None, int | None]:
    """Accept unit book page (2–13), PNG index, or global printed page from CSV."""
    seq = unit_png_sequence(unit_num, page_map)
    if not seq:
        return page_ref, page_ref
    start = book_page_start(unit_num, page_map)
    if page_ref in seq:
        return page_ref, start + seq.index(page_ref)
    png = book_page_to_png(unit_num, page_ref, page_map)
    if png is not None:
        return png, page_ref
    # CSV「page」列 = 课本全局印刷页（如 42 → page-049.png）
    png_from_printed = printed_page_to_png(page_ref, page_map)
    if png_from_printed in seq:
        book_pg = png_to_book_page(unit_num, png_from_printed, page_map)
        return png_from_printed, book_pg
    return None, None


def convert_book_pages_to_png(
    by_book: dict[int, list[dict]], unit_num: int, page_map: dict
) -> dict[int, list[dict]]:
    by_png: dict[int, list[dict]] = {}
    for page_ref, sents in by_book.items():
        png, book_pg = resolve_page_ref(unit_num, page_ref, page_map)
        if png is None:
            print(f"         [WARN] Unit {unit_num}: Page {page_ref} 无法映射，已跳过")
            continue
        cleaned = clean_sentences(sents)
        for s in cleaned:
            s = {**s, "page": png, "bookPage": book_pg}
            by_png.setdefault(png, []).append(s)
    return by_png


def is_chinese_line(line: str) -> bool:
    t = line.strip()
    cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
    latin = len(re.findall(r"[A-Za-z]", t))
    return cjk >= 2 and cjk >= latin


def is_english_line(line: str) -> bool:
    t = line.strip()
    if is_chinese_line(t):
        return False
    if re.match(r"^[\d]+[.)]\s", t):
        return True
    if re.match(r"^[A-D][.)]\s", t, re.I):
        return True
    return bool(re.search(r"[A-Za-z]{2,}", t))


def should_skip_line(line: str) -> bool:
    t = line.strip()
    if not t:
        return True
    if SKIP_LINE_RE.match(t):
        return True
    if t == "Unit 1 课文词汇重点句型 双语学习资料" or re.match(r"^Unit\s+\d+\s+课文词汇", t, re.I):
        return True
    return False


def assign_parts_from_map(unit_num: int, by_page: dict[int, list[dict]], page_map: dict) -> dict[str, dict]:
    """Map page-keyed sentences to part-a / part-b / ... using pdf-page-map."""
    sections: dict[str, dict] = {}
    unit_map = (page_map.get("units") or {}).get(str(unit_num)) or {}
    for part_key, sec in unit_map.items():
        if part_key == "bookPageStart" or not isinstance(sec, dict):
            continue
        pdf_pages = sec.get("pdfPages") or []
        if not pdf_pages:
            continue
        sentences: list[dict] = []
        for pg in pdf_pages:
            for s in by_page.get(pg, []):
                sentences.append({**s, "page": pg})
        sentences = clean_sentences(sentences)
        if sentences:
            sections[part_key] = {
                "pages": pdf_pages,
                "sentences": sentences,
                "bodyHtml": "",
            }
    return sections


def merge_unit_sections(
    unit_num: int,
    by_page: dict[int, list[dict]],
    legacy: dict[str, dict],
    page_map: dict,
) -> dict[str, dict]:
    auto = assign_parts_from_map(unit_num, by_page, page_map) if by_page else {}
    merged: dict[str, dict] = {}
    all_keys = set(auto) | set(legacy)
    for key in all_keys:
        auto_sec = auto.get(key) or {}
        leg_sec = legacy.get(key) or {}
        sentences = leg_sec.get("sentences") or auto_sec.get("sentences") or []
        sentences = clean_sentences(sentences)
        pages = leg_sec.get("pages") or auto_sec.get("pages") or []
        body_html = leg_sec.get("bodyHtml") or auto_sec.get("bodyHtml") or ""
        if sentences or body_html:
            merged[key] = {
                "pages": pages,
                "sentences": sentences,
                "bodyHtml": body_html,
            }
    if by_page:
        merged["_byPage"] = {str(k): v for k, v in by_page.items()}
    return merged


def parse_unit_document(lines: list[str], unit_num: int, page_map: dict) -> dict[str, dict]:
    by_book = parse_by_pages(lines)
    by_page = convert_book_pages_to_png(by_book, unit_num, page_map) if by_book else {}
    legacy = parse_sections(lines)
    if by_page:
        knowledge = {k: v for k, v in legacy.items() if k.startswith("knowledge-") or v.get("bodyHtml")}
        auto = assign_parts_from_map(unit_num, by_page, page_map)
        merged = {**auto}
        merged.update(knowledge)
        merged["_byPage"] = {str(k): v for k, v in by_page.items()}
        return merged
    return legacy


def import_all() -> dict:
    page_map = load_page_map()
    units: dict[str, dict] = {}
    intro: dict[str, dict] = {}
    appendix: dict[str, dict] = {}
    files = find_unit_sources()
    for unit_num, path, kind in files:
        print(f"  [{kind.upper()}] Unit {unit_num}: {path.name}")
        lines = read_source(path, kind)
        page_count = sum(1 for ln in lines if parse_page_marker(ln) is not None)
        sections = parse_unit_document(lines, unit_num, page_map)
        for key in list(sections.keys()):
            if key.startswith("_"):
                continue
            sec = sections[key]
            if sec.get("sentences"):
                sec["sentences"] = clean_sentences(sec["sentences"])
        print(f"         Page markers: {page_count}, parts: {len([k for k in sections if not k.startswith('_')])}")
        for key, data in sections.items():
            if key.startswith("_"):
                units.setdefault(str(unit_num), {})[key] = data
                continue
            if key.startswith("intro-"):
                intro[key] = data
            elif key.startswith("appendix-"):
                appendix[key] = data
            else:
                units.setdefault(str(unit_num), {})[key] = data
    return {
        "version": 2,
        "source": "word",
        "units": units,
        "intro": intro,
        "appendix": appendix,
        "files": [f"{kind}:{p}" for _, p, kind in files],
    }


def main() -> None:
    sources = find_unit_sources()
    if not sources:
        print("[WARN] No CSV files in word-sources/")
        print("       Expected: word-sources/Unit1_课文双语.csv  (page,en,zh)")
        if OUT.exists():
            print("[OK] Keeping existing word-import.json")
            sys.exit(0)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"version": 2, "units": {}, "intro": {}, "appendix": {}}, indent=2), encoding="utf-8")
        sys.exit(0)
    data = import_all()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {len(sources)} file(s) -> {OUT}")


if __name__ == "__main__":
    main()
