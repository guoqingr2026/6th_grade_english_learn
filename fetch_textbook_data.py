# -*- coding: utf-8 -*-
"""从公开课本知识清单页面抓取并解析 PEP 六年级上册 Unit1-6 内容。"""
import json
import os
import re
import urllib.request

SOURCE_URL = (
    "https://max.book118.com/html/2026/0714/7066062122011132.shtm"
)
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "textbook_data.json")
LOCAL_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "课本", "六年级上册英语.docx"),
    os.path.join(os.path.dirname(__file__), "PEP六年级上册知识清单.docx"),
]


def fetch_preview_html():
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0 LearningCompanion/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def split_en_cn(text):
    """将粘连的 'climbtheGreatWall爬长城' 拆成 (en, cn)。"""
    text = re.sub(r"\s+", "", text.strip())
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9\s\-\.\'\"!?,:;()]+?)([\u4e00-\u9fff].*)$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
  # fallback: insert space before first Chinese char
    m2 = re.search(r"([\u4e00-\u9fff])", text)
    if m2:
        i = m2.start()
        return text[:i].strip(), text[i:].strip()
    return text, ""


def parse_units_from_html(html):
    """解析 book118 免费预览中的 Unit 知识清单。"""
    text = re.sub(r"<[^>]+>", "\n", html)
    text = re.sub(r"&nbsp;|&amp;|&lt;|&gt;", " ", text)
    text = re.sub(r"\n+", "\n", text)

    units = []
    chunks = re.split(r"Unit\s*(\d+)\s*([A-Za-z][^\n]*)", text)
    i = 1
    while i + 2 < len(chunks):
        num = int(chunks[i])
        title = chunks[i + 1].strip()
        body = chunks[i + 2]
        unit = _parse_unit_body(num, title, body)
        if unit:
            units.append(unit)
        i += 3
    return units


def _parse_unit_body(num, title, body):
    sections = {
        "vocab": [],
        "phrases": [],
        "sentences": [],
        "must_read": [],
    }
    current = None
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        if "重点单词" in line:
            current = "vocab"
            continue
        if "重点短语" in line:
            current = "phrases"
            continue
        if "重点句型" in line:
            current = "sentences"
            continue
        if "教材必背好句" in line:
            current = "must_read"
            continue
        if "单元核心语法" in line or line.startswith("2026"):
            break
        if current == "vocab":
            m = re.match(r"^([a-zA-Z][\w\s\-']+?)([\u4e00-\u9fff].+)$", re.sub(r"\s+", "", line))
            if m:
                sections["vocab"].append((m.group(1), m.group(2)))
        elif current in ("phrases", "must_read"):
            en, cn = split_en_cn(line)
            if en and cn:
                sections[current].append((en, cn))
        elif current == "sentences":
            en, cn = split_en_cn(line)
            if en and len(en) > 3:
                sections["sentences"].append((en, cn))
    if not sections["phrases"] and not sections["sentences"]:
        return None
    return {"num": num, "title": title, **sections}


def load_local_docx(path):
    try:
        from docx import Document
    except ImportError:
        return None
    if not os.path.isfile(path):
        return None
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs)
    return parse_units_from_html(text)


def main():
    units = None
    for path in LOCAL_CANDIDATES:
        units = load_local_docx(path)
        if units:
            print(f"Loaded from local: {path}")
            break

    if not units:
        print("Fetching online preview...")
        html = fetch_preview_html()
        units = parse_units_from_html(html)
        print(f"Parsed {len(units)} units from web preview")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(units, f, ensure_ascii=False, indent=2)
    print(f"Saved: {OUTPUT_JSON}")
    for u in units:
        print(
            f"  Unit {u['num']}: "
            f"{len(u.get('vocab', []))} words, "
            f"{len(u.get('phrases', []))} phrases, "
            f"{len(u.get('sentences', []))} sentences"
        )


if __name__ == "__main__":
    main()
