#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build glossary + reading/knowledge banks from textbook_catalog.py (UTF-8)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from textbook_catalog import UNITS  # noqa: E402

OUT = ROOT / "data" / "study-hub"
IMG = "assets/images/textbook/pages"

UNIT_FALLBACK = {
    1: "assets/images/unit1-travel.svg",
    2: "assets/images/unit2-festival.svg",
    3: "assets/images/unit3-health.svg",
    4: "assets/images/unit4-money.svg",
    5: "assets/images/unit5-space.svg",
    6: "assets/images/unit6-energy.svg",
}
PARTS = [
    ("unit-start", "单元起始页"),
    ("unit-next", "单元导入"),
    ("part-a", "Part A"),
    ("part-b", "Part B"),
    ("part-c", "Part C"),
    ("reading", "Reading 阅读"),
]

INTRO_SECTIONS = [
    ("cover", "封面"),
    ("inner-cover", "内封"),
    ("copyright", "版权页"),
    ("foreword", "致同学"),
    ("contents-1", "目录（一）"),
    ("contents-2", "目录（二）"),
    ("overview", "语法与拓展总览"),
]

APPENDIX_SECTIONS = [
    ("revision", "Revision 复习"),
    ("songs", "Appendix 1 歌曲"),
    ("words-by-unit", "Appendix 2 各单元词汇"),
    ("vocabulary", "Appendix 3 词汇表"),
    ("expressions", "Appendix 4 常用表达"),
    ("irregular-verbs", "Appendix 5 不规则动词"),
    ("afterword", "后记"),
]

FOREWORD_ZH = (
    "随着新学期的开始，你们将进入小学阶段的最后一年。"
    "在这本书里，你们将和老朋友们一起了解丰富多彩的中外文化，学习独立思考和多角度地看待事物。"
    "想学好英语，一定要多听、多说、多读、多看、多写。"
    "愿你们和书里的小主人公一起享受小学生活的美好时光。"
)

TEACHING_PROMPT = (
    "你作为具有200年教学经验的资深特级小学六年级英语老师，请将课文图片内容严格对应翻译成中文，"
    "并一步步开展教育指导，识别全新知识点，重点讲解并举一反三拓展；"
    "让孩子深刻掌握、灵活使用英语，能听说读写练应用；"
    "运用有趣、印象深刻的单词语法短语记忆法（歌曲、记忆宫殿、讲故事等），"
    "适合六年级孩子理解的教学方法。"
)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"—])", text)
    return [p.strip() for p in parts if p.strip()]


def clean_en(s: str) -> str:
    return re.sub(r"^—\s*", "", s).strip()


def clean_zh(s: str) -> str:
    return re.sub(r"^[—\-]\s*", "", s).strip()


def normalize_en_display(en: str) -> str:
    en = clean_en(en)
    return re.sub(r"\s+", " ", en).strip()


def expand_en_alternatives(en: str) -> list[str]:
    """Split 'A / B' into separate display lines."""
    en = clean_en(en)
    if " / " in en:
        return [normalize_en_display(p) for p in en.split(" / ") if p.strip()]
    return [normalize_en_display(en)] if en else []


def expand_zh_alternatives(zh: str) -> list[str]:
    zh = clean_zh(zh)
    if not zh:
        return [""]
    parts = re.split(r"\s*/\s*", zh)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()]
    return [zh]


def tts_text(en: str) -> str:
    opts = expand_en_alternatives(en)
    return opts[0] if opts else ""


def pair_list(items: list[tuple[str, str]]) -> list[dict]:
    rows = []
    for en, zh in items:
        en_opts = expand_en_alternatives(en)
        zh_opts = expand_zh_alternatives(zh)
        for i, en_c in enumerate(en_opts):
            if not en_c:
                continue
            z = zh_opts[i] if i < len(zh_opts) else (zh_opts[0] if zh_opts else "")
            rows.append({"en": en_c, "zh": z, "tts": tts_text(en_c)})
    return rows


def part_c_sentences(unit: dict) -> list[dict]:
    gd = unit.get("grammar_discover") or {}
    rows = pair_list(gd.get("observe", []))
    for hint in gd.get("hints", []):
        rows.append({"en": hint, "zh": "语法提示", "type": "hint", "tts": tts_text(hint)})
    for q in unit.get("mini_challenge", []):
        rows.append({"en": q, "zh": "挑战练习（请口头或书面完成）", "type": "challenge", "tts": tts_text(q)})
    return rows


READING_ZH: dict[int, str] = {
    1: (
        "去年夏天，陈洁和家人去了西安。他们吃了著名的西安面条，参观了兵马俑。"
        "那里有超过七千个陶俑。萨拉去了井冈山革命博物馆。那些故事非常鼓舞人心。"
    ),
    2: (
        "春节时，我们穿红衣、贴福字，等待春晚，倒计时迎新年。"
        "中秋时我们吃月饼。爸爸参加马拉松当志愿者，我们为选手加油。"
    ),
    3: (
        "保持健康很重要：健康饮食、经常锻炼、早睡早起。"
        "不舒服要看医生。多想想开心的事，和朋友视频聊天，让自己振作。"
    ),
    4: (
        "我写下花钱计划，把零花钱一部分存起来买书包。"
        "我们要分清商品和服务，谨慎用钱，可以等打折再买。"
    ),
    5: (
        "我们用望远镜探索太空。宇航员住在空间站。"
        "中国去年向火星发送了探测器。太空探索让我们自豪。"
    ),
    6: (
        "水来自江河湖泊，电来自发电站。我们要用太阳能、风能等绿色能源。"
        "遵守减少、重复使用、回收的 3R 原则，关灯、拔插头、快速淋浴。"
    ),
}


def reading_sentences(unit: dict) -> list[dict]:
    u = unit["num"]
    title = unit.get("reading_title", "Reading")
    text = unit.get("reading_text", "")
    zh_full = READING_ZH.get(u, "")
    rows = [{"en": title, "zh": "阅读篇目", "type": "title", "tts": title}]
    en_sents = split_sentences(text)
    zh_sents = [s.strip() for s in re.split(r"[。！？]", zh_full) if s.strip()]
    for i, en in enumerate(en_sents):
        zh = zh_sents[i] if i < len(zh_sents) else ""
        en_c = normalize_en_display(en)
        rows.append({"en": en_c, "zh": zh, "tts": tts_text(en_c)})
    return rows


def load_ocr_manifest() -> dict[int, dict]:
    path = OUT / "extracted" / "manifest.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["page"]: entry for entry in data if entry.get("page")}


def is_english_line(line: str) -> bool:
    line = line.strip()
    if len(line) < 4:
        return False
    if not re.search(r"[A-Za-z]", line):
        return False
    if re.match(r"^(Unit|Part|Page|p\.)\s", line, re.I):
        return False
    return True


def zh_lookup(en: str, catalog_pairs: list[tuple[str, str]]) -> str:
    key = normalize_en_display(en).lower()
    for a, b in catalog_pairs:
        for alt in expand_en_alternatives(a):
            if normalize_en_display(alt).lower() == key:
                return clean_zh(b)
            if key in normalize_en_display(alt).lower() or normalize_en_display(alt).lower() in key:
                return clean_zh(b)
    return ""


def sentences_from_ocr_pages(
    pdf_pages: list[int],
    catalog_pairs: list[tuple[str, str]],
    ocr: dict[int, dict],
) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for pg in pdf_pages:
        entry = ocr.get(pg, {})
        lines = entry.get("lines") or []
        if not lines and entry.get("text"):
            lines = split_english_lines(entry["text"])
        for line in lines:
            if not is_english_line(line):
                continue
            en = normalize_en_display(line)
            if en.lower() in seen:
                continue
            seen.add(en.lower())
            zh = zh_lookup(en, catalog_pairs)
            rows.append({"en": en, "zh": zh, "tts": tts_text(en), "page": pg})
    return rows


def split_english_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if line and is_english_line(line):
            lines.append(line)
    return lines


def catalog_pairs_for_part(unit: dict, part_key: str) -> list[tuple[str, str]]:
    if part_key == "part-a":
        return unit.get("part_a_sentences", [])
    if part_key == "part-b":
        return unit.get("part_b_sentences", [])
    if part_key == "part-c":
        gd = unit.get("grammar_discover") or {}
        return gd.get("observe", [])
    if part_key == "reading":
        text = unit.get("reading_text", "")
        return [(s, "") for s in split_sentences(text)]
    return []


def unit_start_sentences(unit: dict) -> list[dict]:
    u = unit["num"]
    title = unit.get("title", "")
    title_cn = unit.get("title_cn", "")
    theme = unit.get("theme", "")
    rows = [
        {"en": f"Unit {u} {title}", "zh": f"第{u}单元 {title_cn}", "type": "title", "tts": f"Unit {u} {title}"},
        {"en": theme, "zh": theme, "type": "hint"},
    ]
    for g in unit.get("goals", []):
        rows.append({"en": g, "zh": g, "type": "goal"})
    return rows


def unit_next_sentences(unit: dict) -> list[dict]:
    return [
        {"en": "Share and explain", "zh": "分享并说明", "type": "section"},
        {"en": "Name a famous place.", "zh": "说出一个著名的地方。", "tts": "Name a famous place."},
        {"en": "Explain what is special about it.", "zh": "解释它特别在哪里。", "tts": "Explain what is special about it."},
        {"en": "Look and think", "zh": "看一看，想一想", "type": "section"},
        {"en": "Listen and sing", "zh": "听一听，唱一唱", "type": "section"},
    ]


def intro_sentences(key: str) -> list[dict]:
    if key == "foreword":
        return [{"en": "致同学", "zh": FOREWORD_ZH, "type": "title"}]
    if key == "cover":
        return [
            {"en": "English", "zh": "英语", "type": "title"},
            {"en": "Grade 6", "zh": "六年级", "type": "line"},
            {"en": "Book 1", "zh": "上册", "type": "line"},
        ]
    if key.startswith("contents"):
        return [{"en": "Contents", "zh": "目录", "type": "title"}]
    if key == "overview":
        return [{"en": "Grammar and Extended Reading Overview", "zh": "语法与拓展阅读总览", "type": "title"}]
    return [{"en": key, "zh": "见左侧课本图", "type": "title"}]


def appendix_sentences(key: str) -> list[dict]:
    labels = dict(APPENDIX_SECTIONS)
    label = labels.get(key, key)
    rows = [{"en": label, "zh": label, "type": "title"}]
    if key == "vocabulary":
        for unit in UNITS:
            for w, ipa, pos, zh in unit.get("part_a_vocab", [])[:6]:
                rows.append({"en": w, "zh": f"{ipa} {zh}", "type": "vocab"})
            for w, ipa, pos, zh in unit.get("part_b_vocab", [])[:4]:
                rows.append({"en": w, "zh": f"{ipa} {zh}", "type": "vocab"})
    elif key == "expressions":
        for unit in UNITS:
            for en, zh in unit.get("part_a_phrases", [])[:3]:
                rows.append({"en": en, "zh": zh, "type": "phrase", "tts": tts_text(en)})
            for en, zh in unit.get("part_b_phrases", [])[:3]:
                rows.append({"en": en, "zh": zh, "type": "phrase", "tts": tts_text(en)})
    elif key == "songs":
        rows.append({"en": "Travelling around", "zh": "四处旅行（歌曲）", "type": "song"})
        rows.append({"en": "Getting together", "zh": "相聚在一起（歌曲）", "type": "song"})
    return rows


def part_sentences(unit: dict, part_key: str, pdf_pages: list[int], ocr: dict[int, dict]) -> list[dict]:
    catalog = catalog_pairs_for_part(unit, part_key)
    if part_key == "unit-start":
        return unit_start_sentences(unit)
    if part_key == "unit-next":
        return unit_next_sentences(unit)
    if part_key == "part-c":
        rows = part_c_sentences(unit)
        ocr_rows = sentences_from_ocr_pages(pdf_pages, catalog, ocr)
        return ocr_rows if len(ocr_rows) >= 3 else rows
    if part_key == "reading":
        rows = reading_sentences(unit)
        ocr_rows = sentences_from_ocr_pages(pdf_pages, catalog, ocr)
        return ocr_rows if len(ocr_rows) >= 3 else rows
    rows = pair_list(catalog)
    ocr_rows = sentences_from_ocr_pages(pdf_pages, catalog, ocr)
    if len(ocr_rows) >= max(3, len(rows) // 2):
        return ocr_rows
    return rows


def page_image(unit: int, part_key: str, page_index: int = 0) -> str:
    return f"{IMG}/u{unit}-{part_key}-{page_index + 1}.png"


def build_glossary() -> dict:
    words: set[str] = set()
    phrases: set[str] = set()
    for unit in UNITS:
        for key in ("part_a_vocab", "part_b_vocab"):
            for row in unit.get(key, []):
                if row:
                    words.add(str(row[0]).strip().lower())
        for key in ("part_a_phrases", "part_b_phrases"):
            for en, _ in unit.get(key, []):
                phrases.add(en.lower())
    return {
        "version": 2,
        "description": "仅附录 Part A/B 一二级词汇与必背短语",
        "words": sorted(words),
        "phrases": sorted(phrases, key=len, reverse=True),
    }


def build_appendix_words_index() -> dict:
    """Appendix 2 vocabulary indexed by textbook page (P.x)."""
    from appendix_parser import parse_appendix_words

    by_page: dict[str, list[str]] = {}
    entries: list[dict] = []
    seen: set[tuple[int, str]] = set()
    for unit, word_list in parse_appendix_words().items():
        for w in word_list:
            word = w.word.strip()
            key = (w.page, word.lower())
            if key in seen:
                continue
            seen.add(key)
            page_key = str(w.page)
            by_page.setdefault(page_key, [])
            if word.lower() not in {x.lower() for x in by_page[page_key]}:
                by_page[page_key].append(word)
            entries.append(
                {
                    "word": word,
                    "page": w.page,
                    "unit": unit,
                    "gloss": w.gloss,
                    "level2": w.level2,
                }
            )
    for page_key in by_page:
        by_page[page_key] = sorted(by_page[page_key], key=lambda x: (-len(x), x.lower()))
    return {"version": 1, "description": "附录2 词汇（按课本 P.x 页码）", "words": entries, "byPage": by_page}


def resolve_page_image(u: int, part_key: str, page_map: dict | None) -> tuple[str, list]:
    pdf_pages: list = []
    if page_map:
        sec = (page_map.get("units", {}).get(str(u)) or {}).get(part_key, {})
        pdf_pages = sec.get("pdfPages", [])
    if pdf_pages:
        return f"{IMG}/page-{pdf_pages[0]:03d}.png", pdf_pages
    return page_image(u, part_key), pdf_pages


def vocab_rows(unit: dict, part_key: str) -> str:
    key = "part_a_vocab" if part_key in ("part-a", "reading") else "part_b_vocab"
    if part_key == "part-c":
        key = "part_a_vocab"
    rows = []
    for w, ipa, pos, zh in unit.get(key, [])[:12]:
        rows.append(f"<tr><td><strong>{w}</strong></td><td>{ipa}</td><td>{pos}</td><td>{zh}</td></tr>")
    return "".join(rows) or "<tr><td colspan=\"4\">见附录词汇表</td></tr>"


def phrase_rows(unit: dict, part_key: str) -> str:
    key = "part_a_phrases" if part_key in ("part-a", "part-c") else "part_b_phrases"
    return "".join(
        f"<tr><td>{en}</td><td>{zh}</td></tr>" for en, zh in unit.get(key, [])[:8]
    )


def goals_html(unit: dict) -> str:
    return "<ul>" + "".join(f"<li>{g}</li>" for g in unit.get("goals", [])) + "</ul>"


def load_word_import() -> dict | None:
    path = OUT / "word-import.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if data.get("units") else None


def word_sentences(word_data: dict | None, unit: int, part_key: str) -> list[dict] | None:
    if not word_data:
        return None
    sec = (word_data.get("units", {}).get(str(unit)) or {}).get(part_key)
    if not sec or not sec.get("sentences"):
        return None
    out = []
    for s in sec["sentences"]:
        en = (s.get("en") or "").strip()
        if en.startswith("<") or "知识点精讲" in en:
            continue
        out.append({k: v for k, v in s.items() if k != "tts"})
    return out if out else None


def word_pages_override(word_data: dict | None, unit: int, part_key: str, default: list[int]) -> list[int]:
    """Page image list always comes from pdf-page-map; word import only supplies text."""
    return default


def word_knowledge_html(word_data: dict | None, unit: int, part_key: str) -> str | None:
    if not word_data:
        return None
    sec = (word_data.get("units", {}).get(str(unit)) or {}).get(f"knowledge-{part_key}")
    if sec and sec.get("bodyHtml"):
        return sec["bodyHtml"]
    return None


def knowledge_body(unit: dict, part_key: str, word_html: str | None = None) -> str:
    if word_html:
        return word_html.strip()
    u = unit["num"]
    title = unit.get("title", "")
    title_cn = unit.get("title_cn", "")
    theme = unit.get("theme", "")
    gd = unit.get("grammar_discover") or {}
    hints_html = "".join(f"<li>{h}</li>" for h in gd.get("hints", []))
    observe_rows = "".join(
        f"<tr><td>{clean_en(a)}</td><td>{clean_zh(b)}</td></tr>" for a, b in gd.get("observe", [])
    )
    challenges = "".join(f"<li>{c}</li>" for c in unit.get("mini_challenge", []))
    reading_kw = ", ".join(unit.get("reading_keywords", []))
    part_label = dict(PARTS).get(part_key, part_key)
    vocab_tbl = vocab_rows(unit, part_key)
    phrase_tbl = phrase_rows(unit, part_key)

    focus_map = {
        "part-a": "听说入门：认读核心词汇，模仿对话，能问答交流",
        "part-b": "读写拓展：读懂语篇，能复述并写简单句",
        "part-c": "语法发现：归纳规则，举一反三完成练习",
        "reading": f"阅读精讲：{unit.get('reading_title', 'Reading')} 全文理解与写作",
    }
    focus = focus_map.get(part_key, "")

    story_map = {
        1: "记忆宫殿：客厅墙上贴着长城照片→桌上西安面条→抽屉里兵马俑明信片，边走边说英语。",
        2: "讲故事：春节红包里藏着 mooncake 和 zongzi，倒计时喊 Happy New Year!",
        3: "歌曲法：用《健康歌》旋律唱 Exercise every day, see a doctor when ill.",
        4: "情景剧：开「小超市」用 pocket money 买 goods，练 spending plan。",
        5: "想象火箭：从 telescope 到 space station 再到 Mars rover。",
        6: "3R 手势舞：Reduce-Reuse-Recycle 三个动作记绿色能源。",
    }
    story = story_map.get(u, "把本单元短语画成思维导图，每天复述一遍。")

    return f"""
<h3>Unit {u} {title}（{title_cn}）— {part_label}</h3>
<p class="teaching-focus"><strong>单元主题：</strong>{theme}</p>
<p class="teaching-focus"><strong>本讲目标：</strong>{focus}</p>
<h4>第一步：课文图片严格对照（左图右学）</h4>
<p>请对照左侧课本图片，一句一句跟读。黄色高亮为附录必背词/短语。</p>
<h4>第二步：学习目标</h4>
{goals_html(unit)}
<h4>第三步：核心词汇（{part_label}）</h4>
<table class="rich-table"><thead><tr><th>单词</th><th>音标</th><th>词性</th><th>释义</th></tr></thead><tbody>{vocab_tbl}</tbody></table>
<h4>第四步：必背短语</h4>
<table class="rich-table"><thead><tr><th>英文</th><th>中文</th></tr></thead><tbody>{phrase_tbl}</tbody></table>
<h4>第五步：语法发现 — {gd.get('title', '本单元语法')}</h4>
<table class="rich-table"><thead><tr><th>英文例句</th><th>中文</th></tr></thead><tbody>{observe_rows}</tbody></table>
<ul class="grammar-hints">{hints_html}</ul>
<h4>举一反三 · 挑战练习</h4>
<ol>{challenges}</ol>
<h4>阅读关键词</h4><p><code>{reading_kw}</code></p>
<p class="tip-box">🏰 <strong>记忆宫殿/故事法：</strong>{story}</p>
<p class="tip-box">🎵 <strong>歌曲记忆：</strong>把核心句型编成 4 句小歌谣，每天睡前哼一遍。</p>
<p class="tip-box">✍️ <strong>活学活用：</strong>用本 Part 3 个短语写 5 句英语日记，家长签字打卡。</p>
<p class="tip-box">🎯 <strong>冲满分：</strong>完成「Part 通关测验」达 80% 解锁下一 Part；错题自动进错题本。</p>
""".strip()


def build_page_contents(sentences: list[dict], pdf_pages: list[int]) -> list[dict]:
    """Split sentences by textbook page for image flip sync."""
    if not pdf_pages:
        return []
    by_page: dict[int, list] = {p: [] for p in pdf_pages}
    unassigned = []
    for s in sentences:
        pg = s.get("page")
        if pg and pg in by_page:
            by_page[pg].append({k: v for k, v in s.items() if k != "page"})
        else:
            unassigned.append(s)
    if unassigned:
        per = max(1, (len(unassigned) + len(pdf_pages) - 1) // len(pdf_pages))
        for i, pg in enumerate(pdf_pages):
            chunk = unassigned[i * per : (i + 1) * per]
            by_page[pg].extend(chunk)
    out = []
    for p in pdf_pages:
        if not by_page[p]:
            continue
        book_pg = next((s.get("bookPage") for s in sentences if s.get("page") == p and s.get("bookPage")), None)
        out.append({"page": p, "bookPage": book_pg, "sentences": by_page[p]})
    return out


def unit_book_meta(u: int, page_map: dict | None) -> dict:
    if not page_map:
        return {}
    unit = (page_map.get("units") or {}).get(str(u)) or {}
    seq: list[int] = []
    for key in ("unit-start", "unit-next", "part-a", "part-b", "part-c", "reading"):
        sec = unit.get(key) or {}
        seq.extend(sec.get("pdfPages") or [])
    start = int(unit.get("bookPageStart") or page_map.get("bookPageStart") or 2)
    return {
        "bookPageStart": start,
        "pngSequence": seq,
        "bookPageMap": {str(png): start + i for i, png in enumerate(seq)},
    }


def build_reading_bank(page_map: dict | None, ocr: dict[int, dict], word_data: dict | None) -> dict:
    units_out = []
    for unit in UNITS:
        u = unit["num"]
        pages = []
        for part_key, label in PARTS:
            sec = (page_map.get("units", {}).get(str(u)) or {}).get(part_key, {}) if page_map else {}
            pdf_pages = word_pages_override(word_data, u, part_key, sec.get("pdfPages", []))
            image = f"{IMG}/page-{pdf_pages[0]:03d}.png" if pdf_pages else page_image(u, part_key)
            ws = word_sentences(word_data, u, part_key)
            sentences = ws if ws else part_sentences(unit, part_key, pdf_pages, ocr)
            pages.append({
                "id": f"u{u}-{part_key}",
                "label": sec.get("label", label),
                "part": part_key,
                "image": image,
                "fallbackImage": UNIT_FALLBACK.get(u, "assets/images/unit1-travel.svg"),
                "pdfPages": pdf_pages,
                "pageContents": build_page_contents(sentences, pdf_pages),
                "sentences": sentences,
            })
        units_out.append({
            "unit": u,
            "title": f"Unit {u} {unit.get('title', '')}",
            "titleZh": unit.get("title_cn", ""),
            **unit_book_meta(u, page_map),
            "pages": pages,
        })
    intro_pages = []
    if page_map and page_map.get("intro"):
        for key, label in INTRO_SECTIONS:
            sec = page_map["intro"].get(key, {})
            pdf_pages = sec.get("pdfPages", [])
            if not pdf_pages:
                continue
            sents = intro_sentences(key)
            intro_pages.append({
                "id": f"intro-{key}",
                "label": sec.get("label", label),
                "part": "intro",
                "image": f"{IMG}/page-{pdf_pages[0]:03d}.png",
                "pdfPages": pdf_pages,
                "pageContents": build_page_contents(sents, pdf_pages),
                "sentences": sents,
            })
    appendix_pages = []
    if page_map and page_map.get("appendix"):
        for key, label in APPENDIX_SECTIONS:
            sec = page_map["appendix"].get(key, {})
            pdf_pages = sec.get("pdfPages", [])
            if not pdf_pages:
                continue
            sents = appendix_sentences(key)
            appendix_pages.append({
                "id": f"appendix-{key}",
                "label": sec.get("label", label),
                "part": "appendix",
                "image": f"{IMG}/page-{pdf_pages[0]:03d}.png",
                "pdfPages": pdf_pages,
                "pageContents": build_page_contents(sents, pdf_pages),
                "sentences": sents,
            })
    return {
        "version": 3,
        "title": "课文中英文讲读",
        "description": "内容来自 word-sources Word 资料 · 页码与课本图一一对应",
        "intro": {"title": "开篇与目录", "pages": intro_pages},
        "units": units_out,
        "appendix": {"title": "附录", "pages": appendix_pages},
    }


def appendix_knowledge_body(key: str, label: str) -> str:
    focus_map = {
        "revision": "复习全册语法、词汇与句型，查漏补缺。",
        "songs": "通过歌曲巩固单元主题与核心句型，培养语感。",
        "words-by-unit": "按单元梳理附录词汇，区分听说与读写词汇。",
        "vocabulary": "查音标、词性与释义，掌握全书词汇表用法。",
        "expressions": "背诵常用表达，能在口语与写作中灵活运用。",
        "irregular-verbs": "熟记不规则动词三态，为时态写作打基础。",
        "afterword": "回顾学习历程，规划持续英语学习方法。",
    }
    focus = focus_map.get(key, "对照课本附录逐页精讲。")
    return f"""
<h3>{label} 精讲</h3>
<p class="teaching-focus"><strong>本讲目标：</strong>{focus}</p>
<h4>第一步：课文图片严格对照（左图右学）</h4>
<p>请对照左侧课本图片，逐页理解附录内容。黄色高亮为必背词/短语。</p>
<h4>第二步：学习建议</h4>
<ul>
<li>先通读全文，圈出不懂的单词</li>
<li>对照中文，理解每句含义</li>
<li>大声朗读 2–3 遍，注意发音</li>
<li>完成自我检测，标记薄弱环节</li>
</ul>
<p class="tip-box">🎯 <strong>冲满分：</strong>对照左侧课本图逐页精讲，可编辑保存本页笔记。</p>
""".strip()


def word_appendix_knowledge_html(word_data: dict | None, key: str) -> str | None:
    if not word_data:
        return None
    sec = (word_data.get("appendix") or {}).get(f"knowledge-{key}")
    if sec and sec.get("bodyHtml"):
        return sec["bodyHtml"]
    return None


def build_knowledge_bank(page_map: dict | None, word_data: dict | None) -> dict:
    units_out = []
    for unit in UNITS:
        u = unit["num"]
        pages = []
        for part_key, label in PARTS:
            if part_key in ("unit-start", "unit-next"):
                continue
            image, pdf_pages = resolve_page_image(u, part_key, page_map)
            wh = word_knowledge_html(word_data, u, part_key)
            pages.append({
                "id": f"u{u}-k-{part_key}",
                "label": f"{label} 精讲",
                "part": part_key,
                "image": image,
                "fallbackImage": UNIT_FALLBACK.get(u, "assets/images/unit1-travel.svg"),
                "pdfPages": pdf_pages,
                "videoUrl": "",
                "videoTitle": f"Unit {u} {label} 视频精讲（可编辑链接）",
                "bodyHtml": knowledge_body(unit, part_key, wh),
            })
        units_out.append({
            "unit": u,
            "title": f"Unit {u} {unit.get('title', '')}",
            "titleZh": unit.get("title_cn", ""),
            "pages": pages,
        })
    appendix_pages = []
    if page_map and page_map.get("appendix"):
        for key, label in APPENDIX_SECTIONS:
            sec = page_map["appendix"].get(key, {})
            pdf_pages = sec.get("pdfPages", [])
            if not pdf_pages:
                continue
            sec_label = sec.get("label", label)
            wh = word_appendix_knowledge_html(word_data, key)
            appendix_pages.append({
                "id": f"appendix-k-{key}",
                "label": f"{sec_label} 精讲",
                "part": "appendix",
                "image": f"{IMG}/page-{pdf_pages[0]:03d}.png",
                "fallbackImage": "assets/images/unit1-travel.svg",
                "pdfPages": pdf_pages,
                "videoUrl": "",
                "videoTitle": f"{sec_label} 视频精讲（可编辑链接）",
                "bodyHtml": wh or appendix_knowledge_body(key, sec_label),
            })
    return {
        "version": 2,
        "title": "知识点精讲",
        "units": units_out,
        "appendix": {"title": "附录", "pages": appendix_pages},
    }


def load_page_map() -> dict | None:
    path = OUT / "pdf-page-map.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    page_map = load_page_map()
    ocr = load_ocr_manifest()
    word_data = load_word_import()
    glossary = build_glossary()
    appendix_words = build_appendix_words_index()
    reading = build_reading_bank(page_map, ocr, word_data)
    knowledge = build_knowledge_bank(page_map, word_data)
    (OUT / "glossary.json").write_text(json.dumps(glossary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "appendix-words.json").write_text(
        json.dumps(appendix_words, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "reading-bank.json").write_text(json.dumps(reading, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "knowledge-bank.json").write_text(json.dumps(knowledge, ensure_ascii=False, indent=2), encoding="utf-8")
    ocr_n = len(ocr)
    print(f"[OK] glossary: {len(glossary['words'])} words, {len(glossary['phrases'])} phrases (Part A/B only)")
    print(f"[OK] appendix-words: {len(appendix_words['words'])} entries, {len(appendix_words['byPage'])} pages")
    print(f"[OK] reading: intro {len(reading.get('intro', {}).get('pages', []))} + "
          f"{len(reading['units'])} units x {len(PARTS)} parts + "
          f"appendix {len(reading.get('appendix', {}).get('pages', []))}")
    print(f"[OK] Word import: {'yes' if word_data else 'no (use word-sources/*.docx)'}")
    print(f"[OK] knowledge: {len(knowledge['units'])} units + appendix {len(knowledge.get('appendix', {}).get('pages', []))}")


if __name__ == "__main__":
    main()
