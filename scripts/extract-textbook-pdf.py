#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract textbook PDF pages to PNG + text manifest.
Requires: pip install pymupdf

Place PDF in project root (filename contains pep or 六上).
Edit data/study-hub/pdf-page-map.json then run build-study-hub.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_IMG = ROOT / "assets" / "images" / "textbook" / "pages"
OUT_META = ROOT / "data" / "study-hub" / "extracted"
DPI = 180


def find_pdf() -> Path | None:
    for p in ROOT.glob("*.pdf"):
        name = p.name.lower()
        if "pep" in name or "六上" in p.name or "英语" in p.name:
            return p
    return None


def extract(pdf_path: Path) -> list[dict]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[ERROR] Install PyMuPDF: python -m pip install pymupdf")
        sys.exit(1)

    OUT_IMG.mkdir(parents=True, exist_ok=True)
    OUT_META.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    manifest = []
    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)

    for i in range(len(doc)):
        page = doc[i]
        num = i + 1
        pix = page.get_pixmap(matrix=mat, alpha=False)
        png = OUT_IMG / f"page-{num:03d}.png"
        pix.save(str(png))
        text = page.get_text("text") or ""
        entry = {"page": num, "image": f"assets/images/textbook/pages/page-{num:03d}.png", "text": text.strip()}
        manifest.append(entry)
        (OUT_META / f"page-{num:03d}.json").write_text(
            json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  page {num:3d} -> {png.name} ({len(text)} chars)")

    doc.close()
    (OUT_META / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def auto_detect_units(manifest: list[dict]) -> dict:
    """Heuristic: find pages containing Unit N and Part A/B/C."""
    units: dict[str, dict] = {}
    current_unit = None
    for entry in manifest:
        text = entry.get("text", "")
        m = re.search(r"Unit\s*(\d+)", text, re.I)
        if m:
            current_unit = m.group(1)
            if current_unit not in units:
                units[current_unit] = {"part-a": [], "part-b": [], "part-c": [], "reading": []}
        if not current_unit:
            continue
        page = entry["page"]
        if re.search(r"Part\s*A", text, re.I):
            units[current_unit]["part-a"].append(page)
        if re.search(r"Part\s*B", text, re.I):
            units[current_unit]["part-b"].append(page)
        if re.search(r"Part\s*C", text, re.I):
            units[current_unit]["part-c"].append(page)
        if re.search(r"Reading|Read and", text, re.I):
            units[current_unit]["reading"].append(page)
    return {"pdf": "auto", "units": units}


def main() -> None:
    pdf = find_pdf()
    if not pdf:
        print("[WARN] No PDF found in project root.")
        sys.exit(0)
    print(f"[PDF] {pdf.name}")
    manifest = extract(pdf)
    detected = auto_detect_units(manifest)
    map_path = ROOT / "data" / "study-hub" / "pdf-page-map.json"
    if not map_path.exists():
        map_path.write_text(json.dumps(detected, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] Wrote auto page map -> {map_path}")
    print(f"[OK] {len(manifest)} pages extracted. Run: python scripts/build-study-hub.py")


if __name__ == "__main__":
    main()
