#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Study Hub HTML document library — per-page reading/knowledge storage."""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARY_ROOT = ROOT / "data" / "study-hub" / "library"
MAP_PATH = ROOT / "data" / "study-hub" / "pdf-page-map.json"


def load_page_map() -> dict:
    if not MAP_PATH.exists():
        return {"printPageOffset": 7}
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))


def print_page_offset(page_map: dict | None = None) -> int:
    pm = page_map or load_page_map()
    return int(pm.get("printPageOffset", 7))


def printed_page_for_png(png: int, page_map: dict | None = None) -> int:
    n = int(png)
    if n <= 8:
        return n
    return n - print_page_offset(page_map)


def png_for_printed_page(printed: int, page_map: dict | None = None) -> int:
    p = int(printed)
    if p <= 8:
        return p
    return p + print_page_offset(page_map)


def reading_library_path(unit: int, png: int, scope: str = "unit") -> Path:
    sc = (scope or "unit").strip().lower()
    if sc in ("intro", "appendix"):
        return LIBRARY_ROOT / "reading" / f"{sc}-p{int(png):03d}.html"
    return LIBRARY_ROOT / "reading" / f"u{int(unit)}-p{int(png):03d}.html"


def read_reading_library(unit: int, png: int, scope: str = "unit") -> str | None:
    """Read reading HTML; migrate legacy appendix/intro files saved under u{N}-p{png}."""
    path = reading_library_path(unit, png, scope)
    body = read_library_html(path)
    if body or scope == "unit":
        return body
    legacy_glob = LIBRARY_ROOT / "reading" / f"u*-p{int(png):03d}.html"
    for legacy in sorted(legacy_glob.parent.glob(legacy_glob.name)):
        legacy_body = read_library_html(legacy)
        if legacy_body:
            write_library_html(path, legacy_body)
            return legacy_body
    return None


def knowledge_library_path(page_id: str) -> Path:
    safe = re.sub(r"[^\w\-]", "", page_id or "")
    if not safe:
        raise ValueError("invalid page id")
    return LIBRARY_ROOT / "knowledge" / f"{safe}.html"


def ensure_library_dirs() -> None:
    (LIBRARY_ROOT / "reading").mkdir(parents=True, exist_ok=True)
    (LIBRARY_ROOT / "knowledge").mkdir(parents=True, exist_ok=True)


def read_csv_text(raw: str | bytes | None = None, path: Path | None = None) -> str:
    """Read CSV as UTF-8 text; supports BOM and common Windows encodings."""
    if raw is not None and isinstance(raw, str):
        return raw.replace("\ufeff", "")
    if path is not None:
        data = path.read_bytes()
        for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", errors="replace")
    return ""


def sanitize_text(text: str) -> str:
    """Remove control chars that break JSON / HTML storage; keep emoji and CJK."""
    if not text:
        return ""
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)


def esc(text: str) -> str:
    """Escape only HTML syntax chars; emoji / CJK / symbols pass through unchanged."""
    return html.escape(sanitize_text(text or ""), quote=False)


ZH_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
P_BLOCK_RE = re.compile(r"<p(\s[^>]*)?>(.*?)</p>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def has_chinese(text: str) -> bool:
    return bool(ZH_RE.search(text or ""))


EMOJI_SYMBOL_RE = re.compile(
    r"[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE00-\U0000FE0F"
    r"\U0000200D\U000020E3\U0000E0020-\U0000E007F]"
)


def is_emoji_or_symbol_prefix(text: str) -> bool:
    """True when a line is only emoji / symbols (should stay on the same line as following zh)."""
    t = (text or "").strip()
    if not t or has_chinese(t):
        return False
    latin = len(re.findall(r"[A-Za-z]", t))
    if latin >= 4:
        return False
    if EMOJI_SYMBOL_RE.search(t):
        return True
    if latin == 0:
        return True
    return latin < 4 and not re.search(r"[A-Za-z]{2,}", t)


def combine_prefix_zh(prefix: str, zh: str) -> str:
    p = (prefix or "").strip()
    z = (zh or "").strip()
    if not p:
        return z
    if z.startswith(p):
        return z
    return f"{p} {z}".strip()


def merge_prefix_blocks(blocks: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    i = 0
    while i < len(blocks):
        row = blocks[i]
        kind = classify_text(row["text"], row["hint"] or None)
        if (
            i + 1 < len(blocks)
            and kind == "en"
            and is_emoji_or_symbol_prefix(row["text"])
            and classify_text(blocks[i + 1]["text"], blocks[i + 1]["hint"] or None) == "zh"
        ):
            merged.append(
                {
                    "text": combine_prefix_zh(row["text"], blocks[i + 1]["text"]),
                    "hint": "zh",
                }
            )
            i += 2
            continue
        merged.append(row)
        i += 1
    return merged


def strip_tags(text: str) -> str:
    return html.unescape(TAG_RE.sub("", text or "")).strip()


def classify_text(text: str, hint: str | None = None) -> str:
    if hint in ("en", "zh"):
        return hint
    text = (text or "").strip()
    if not text:
        return "en"
    if not has_chinese(text):
        return "en"
    latin = len(re.findall(r"[A-Za-z]", text))
    cjk = len(ZH_RE.findall(text))
    if cjk > 0 and latin < 4:
        return "zh"
    return "zh" if cjk >= latin else "en"


def extract_html_blocks(content: str) -> list[dict[str, str]]:
    content = sanitize_text((content or "").strip())
    if not content:
        return []
    blocks: list[dict[str, str]] = []
    if "<" in content:
        for m in P_BLOCK_RE.finditer(content):
            attrs = m.group(1) or ""
            text = strip_tags(m.group(2))
            if not text:
                continue
            hint = None
            cm = re.search(r'class=["\']([^"\']*)["\']', attrs, re.IGNORECASE)
            if cm:
                classes = cm.group(1).split()
                if "zh" in classes:
                    hint = "zh"
                elif "en" in classes:
                    hint = "en"
            blocks.append({"text": text, "hint": hint or ""})
    if not blocks:
        for line in re.split(r"\r?\n", content):
            line = line.strip()
            if line:
                blocks.append({"text": line, "hint": ""})
    return blocks


def html_to_sentence_pairs(content: str) -> list[dict[str, str]]:
    blocks = merge_prefix_blocks(extract_html_blocks(content))
    pairs: list[dict[str, str]] = []
    i = 0
    while i < len(blocks):
        row = blocks[i]
        kind = classify_text(row["text"], row["hint"] or None)
        if kind == "en":
            en = row["text"]
            zh = ""
            if i + 1 < len(blocks):
                nxt = blocks[i + 1]
                if classify_text(nxt["text"], nxt["hint"] or None) == "zh":
                    zh = nxt["text"]
                    if is_emoji_or_symbol_prefix(en):
                        zh = combine_prefix_zh(en, zh)
                        en = ""
                    i += 2
                    pairs.append({"en": en, "zh": zh})
                    continue
            pairs.append({"en": en, "zh": zh})
        else:
            pairs.append({"en": "", "zh": row["text"]})
        i += 1
    return pairs


def extract_zh_theme_from_html(content: str) -> tuple[str, bool]:
    color = "#b45309"
    bold = False
    m = re.search(
        r'<p[^>]*class=["\'][^"\']*zh[^"\']*["\'][^>]*style=["\'][^"\']*color:\s*([^;"\']+)',
        content,
        re.IGNORECASE,
    )
    if m:
        color = m.group(1).strip()
    if re.search(r"font-weight:\s*700", content, re.IGNORECASE):
        bold = True
    return color, bold


def normalize_page_html(
    content: str,
    zh_color: str = "#b45309",
    zh_bold: bool = False,
) -> str:
    """Normalize editor HTML: classify en/zh, strip stray inline styles, apply zh theme."""
    blocks = merge_prefix_blocks(extract_html_blocks(content))
    if not blocks:
        return ""
    zh_style = f' style="color:{zh_color};font-weight:{"700" if zh_bold else "400"}"'
    out: list[str] = []
    for row in blocks:
        kind = classify_text(row["text"], row["hint"] or None)
        text = esc(row["text"])
        if kind == "zh":
            out.append(f'<p class="zh"{zh_style}>{text}</p>')
        else:
            out.append(f'<p class="en">{text}</p>')
    return "\n".join(out)


def normalize_page_content(content: str) -> str:
    content = sanitize_text((content or "").strip())
    if not content:
        return ""
    if "<" not in content:
        return plain_text_to_html(content)
    zh_color, zh_bold = extract_zh_theme_from_html(content)
    return normalize_page_html(content, zh_color, zh_bold)


def unit_csv_path(unit: int) -> Path:
    word_dir = ROOT / "word-sources"
    word_dir.mkdir(parents=True, exist_ok=True)
    matches = sorted(word_dir.glob(f"Unit{unit}*.csv"))
    if matches:
        return matches[0]
    return word_dir / f"Unit{unit}_课文双语.csv"


def sync_reading_page_to_csv(unit: int, printed_page: int, body_html: str) -> Path | None:
    """Write this page's en/zh rows back into the unit CSV (other pages unchanged)."""
    pairs = html_to_sentence_pairs(body_html)
    if not pairs:
        return None
    csv_path = unit_csv_path(unit)
    by_page: dict[int, list[dict]] = {}
    if csv_path.exists():
        for row in parse_csv_rows(csv_path.read_text(encoding="utf-8-sig")):
            if row["printedPage"] == printed_page:
                continue
            by_page.setdefault(row["printedPage"], []).append(row)
    by_page[printed_page] = [{"printedPage": printed_page, **p} for p in pairs]
    lines = ["page,en,zh"]
    for page in sorted(by_page):
        for row in by_page[page]:
            en = (row.get("en") or "").replace('"', '""')
            zh = (row.get("zh") or "").replace('"', '""')
            if "," in en or '"' in en or "\n" in en:
                en = f'"{en}"'
            if "," in zh or '"' in zh or "\n" in zh:
                zh = f'"{zh}"'
            lines.append(f"{page},{en},{zh}")
    csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path


def plain_text_to_html(text: str) -> str:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]
    if not blocks:
        lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
        blocks = lines
    out: list[str] = []
    for block in blocks:
        for line in block.splitlines():
            line = line.strip()
            if line:
                out.append(f"<p>{esc(line)}</p>")
    return "\n".join(out)


def sentences_to_html(sentences: list[dict]) -> str:
    out: list[str] = []
    for row in sentences:
        en = (row.get("en") or "").strip()
        zh = (row.get("zh") or "").strip()
        if is_emoji_or_symbol_prefix(en) and zh:
            out.append(f'<p class="zh">{esc(combine_prefix_zh(en, zh))}</p>')
        elif en and zh:
            out.append(f'<p class="en">{esc(en)}</p>')
            out.append(f'<p class="zh">{esc(zh)}</p>')
        elif en:
            out.append(f'<p class="en">{esc(en)}</p>')
        elif zh:
            out.append(f'<p class="zh">{esc(zh)}</p>')
    return "\n".join(out)


def read_library_html(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def write_library_html(path: Path, body_html: str) -> Path:
    ensure_library_dirs()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body_html.strip() + "\n", encoding="utf-8")
    return path


def save_reading_page(unit: int, png: int, body_html: str, scope: str = "unit") -> Path:
    sc = (scope or "unit").strip().lower()
    path = write_library_html(reading_library_path(unit, png, sc), body_html)
    if sc == "unit":
        printed = printed_page_for_png(png)
        try:
            sync_reading_page_to_csv(unit, printed, body_html)
        except OSError:
            pass
    return path


def save_knowledge_page(page_id: str, body_html: str) -> Path:
    return write_library_html(knowledge_library_path(page_id), normalize_knowledge_content(body_html))


def media_library_dir() -> Path:
    path = LIBRARY_ROOT / "media"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_media_file(filename: str, raw: bytes) -> Path:
    safe = re.sub(r"[^\w.\-]", "_", filename or "upload.bin")
    if not safe:
        safe = "upload.bin"
    dest = media_library_dir() / safe
    stem = dest.stem
    suffix = dest.suffix
    n = 1
    while dest.exists():
        dest = media_library_dir() / f"{stem}-{n}{suffix}"
        n += 1
    dest.write_bytes(raw)
    return dest


def student_audio_dir() -> Path:
    path = ROOT / "assets" / "audios" / "student"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_student_audio(filename: str, raw: bytes) -> Path:
    """Save student reading MP3 under assets/audios/student/ (Unit-part_date_time.mp3)."""
    safe = re.sub(r"[^\w.\-]", "_", filename or "recording.mp3")
    if not safe.lower().endswith(".mp3"):
        safe = f"{safe}.mp3"
    dest = student_audio_dir() / safe
    dest.write_bytes(raw)
    return dest


SNIP_INDEX_PATH = ROOT / "data" / "study-hub" / "snip-index.json"


def snip_index_path() -> Path:
    return SNIP_INDEX_PATH


def load_snip_index() -> dict:
    if not SNIP_INDEX_PATH.exists():
        return {"version": 1, "items": []}
    try:
        data = json.loads(SNIP_INDEX_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"version": 1, "items": []}
        data.setdefault("version", 1)
        data.setdefault("items", [])
        return data
    except Exception:
        return {"version": 1, "items": []}


def save_snip_index(data: dict) -> None:
    SNIP_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNIP_INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def snip_category_dir(unit: int, category: str) -> Path:
    cat = "task" if category == "task" else "homework"
    path = ROOT / "assets" / "images" / "snip" / f"unit{int(unit)}" / cat
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_snip_image(
    unit: int,
    category: str,
    filename: str,
    raw: bytes,
    page_id: str = "",
    part: str = "",
) -> dict:
    """Save snip PNG under assets/images/snip/unit{N}/{task|homework}/ and update index."""
    safe = re.sub(r"[^\w.\-]", "_", filename or "snip.png")
    if not safe.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        safe = f"{safe}.png"
    dest = snip_category_dir(unit, category) / safe
    dest.write_bytes(raw)
    rel = str(dest.relative_to(ROOT)).replace("\\", "/")
    entry = {
        "id": f"snip_{unit}_{category}_{int(__import__('time').time() * 1000)}",
        "unit": int(unit),
        "pageId": page_id or "",
        "part": part or "",
        "category": "task" if category == "task" else "homework",
        "filename": safe,
        "path": rel,
        "createdAt": int(__import__("time").time() * 1000),
    }
    data = load_snip_index()
    data["items"].append(entry)
    save_snip_index(data)
    return entry


def list_snips(unit: int | None = None, page_id: str | None = None) -> list:
    items = load_snip_index().get("items") or []
    out = []
    for row in items:
        if unit is not None and int(row.get("unit", 0)) != int(unit):
            continue
        if page_id and row.get("pageId") and row.get("pageId") != page_id:
            continue
        path = ROOT / str(row.get("path", "")).replace("/", "\\")
        if path.exists():
            out.append(row)
    out.sort(key=lambda r: r.get("createdAt", 0), reverse=True)
    return out


def delete_snip(snip_id: str) -> bool:
    data = load_snip_index()
    items = data.get("items") or []
    kept = []
    removed = None
    for row in items:
        if row.get("id") == snip_id:
            removed = row
        else:
            kept.append(row)
    if not removed:
        return False
    path = ROOT / str(removed.get("path", "")).replace("/", "\\")
    if path.exists():
        path.unlink()
    data["items"] = kept
    save_snip_index(data)
    return True


def normalize_knowledge_content(content: str) -> str:
    """Preserve rich HTML for knowledge pages; strip scripts and unsafe attrs."""
    content = sanitize_text((content or "").strip())
    if not content:
        return ""
    content = re.sub(r"<script[\s\S]*?</script>", "", content, flags=re.I)
    content = re.sub(r"<style[\s\S]*?</style>", "", content, flags=re.I)
    content = re.sub(r"\s+on\w+\s*=\s*(['\"]).*?\1", "", content, flags=re.I)
    content = re.sub(r"javascript:", "", content, flags=re.I)
    return content.strip()


def split_en_zh_merged(text: str) -> tuple[str, str]:
    """When en and zh are in one column, split at first Chinese character."""
    text = (text or "").strip()
    if not text:
        return "", ""
    m = re.search(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]", text)
    if not m:
        return text, ""
    idx = m.start()
    return text[:idx].strip(), text[idx:].strip()


def parse_page_number(raw: str) -> int | None:
    text = (raw or "").strip()
    if text.isdigit():
        return int(text)
    m = re.search(r"\d+", text)
    return int(m.group(0)) if m else None


def detect_csv_rows(text: str) -> list[list[str]]:
    raw = text.replace("\ufeff", "")
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    if not lines:
        return []
    sample = lines[0]
    delimiter = ";"
    if sample.count(",") >= sample.count(";"):
        delimiter = ","
    return list(csv.reader(lines, delimiter=delimiter))


def parse_csv_rows(text: str) -> list[dict]:
    rows_in = detect_csv_rows(text)
    if not rows_in:
        return []
    header = [c.strip().lower() for c in rows_in[0]]
    has_header = header and header[0] in ("page", "页码", "pages")
    pi = header.index("page") if has_header and "page" in header else 0
    if has_header and "页码" in header and pi < 0:
        pi = header.index("页码")
    ei = 1
    zi = 2
    if has_header:
        for key in ("en", "english", "英文"):
            if key in header:
                ei = header.index(key)
                break
        for key in ("zh", "chinese", "中文"):
            if key in header:
                zi = header.index(key)
                break
    start = 1 if has_header else 0
    out: list[dict] = []
    for row in rows_in[start:]:
        if len(row) <= pi:
            continue
        printed = parse_page_number(row[pi])
        if printed is None:
            continue
        en = (row[ei] or "").strip() if len(row) > ei else ""
        zh = (row[zi] or "").strip() if len(row) > zi else ""
        if en and not zh:
            en, zh = split_en_zh_merged(en)
        if not en and not zh:
            continue
        out.append({"printedPage": printed, "en": en, "zh": zh})
    return out


def import_csv_to_library(text: str, unit: int = 1) -> dict:
    """Convert CSV rows to per-page HTML files. page column = global printed page."""
    text = read_csv_text(raw=text)
    page_map = load_page_map()
    rows = parse_csv_rows(text)
    if not rows:
        raise ValueError(
            "CSV 无法解析：请用 UTF-8 保存，第一列页码为纯数字（如 30），"
            "英文与中文分列或用英文+中文同一格（自动按汉字拆分）。"
            "推荐表头：page,en,zh"
        )
    by_png: dict[int, list[dict]] = {}
    for row in rows:
        png = png_for_printed_page(row["printedPage"], page_map)
        by_png.setdefault(png, []).append(row)
    written = 0
    for png, items in by_png.items():
        html_body = sentences_to_html(
            [{"en": r["en"], "zh": r["zh"]} for r in items if r.get("en") or r.get("zh")]
        )
        if html_body:
            save_reading_page(unit, png, html_body)
            written += 1
    return {"ok": True, "rows": len(rows), "pages": written, "unit": unit}
