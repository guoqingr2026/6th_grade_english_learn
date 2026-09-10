#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract text from textbook PDF (text layer) into data/study-hub/extracted/.
Does NOT re-export PNG images. Run: python scripts/ocr-textbook-pages.py
Optional: pip install pymupdf
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "study-hub" / "extracted"
IMG_DIR = ROOT / "assets" / "images" / "textbook" / "pages"


def find_pdf() -> Path | None:
    for p in ROOT.glob("*.pdf"):
        name = p.name.lower()
        if "pep" in name or "六上" in p.name or "英语" in p.name:
            return p
    return None


def split_english_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^[\d\.\s]+$", line):
            continue
        if len(line) < 3:
            continue
        if re.search(r"[\u4e00-\u9fff]", line) and not re.search(r"[A-Za-z]{3,}", line):
            continue
        lines.append(line)
    return lines


def extract_pdf_text(pdf_path: Path) -> list[dict]:
    import fitz  # PyMuPDF

    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    manifest = []
    for i in range(len(doc)):
        page = doc[i]
        num = i + 1
        text = (page.get_text("text") or "").strip()
        lines = split_english_lines(text)
        entry = {
            "page": num,
            "image": f"assets/images/textbook/pages/page-{num:03d}.png",
            "text": text,
            "lines": lines,
        }
        manifest.append(entry)
        (OUT / f"page-{num:03d}.json").write_text(
            json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  page {num:3d}: {len(lines)} lines, {len(text)} chars")
    doc.close()
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def build_stub_from_images() -> list[dict]:
    """When no PDF: create empty stubs so build-study-hub can fall back to catalog."""
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    if not IMG_DIR.exists():
        return manifest
    for png in sorted(IMG_DIR.glob("page-*.png")):
        num = int(png.stem.split("-")[1])
        entry = {"page": num, "image": f"assets/images/textbook/pages/{png.name}", "text": "", "lines": []}
        manifest.append(entry)
        (OUT / f"page-{num:03d}.json").write_text(
            json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    pdf = find_pdf()
    if pdf:
        print(f"[PDF] {pdf.name}")
        manifest = extract_pdf_text(pdf)
    else:
        print("[WARN] No PDF in project root. Creating image stubs (catalog fallback).")
        print("       Place PDF and re-run for OCR text layer extraction.")
        manifest = build_stub_from_images()
    print(f"[OK] {len(manifest)} pages -> {OUT}")


if __name__ == "__main__":
    main()
