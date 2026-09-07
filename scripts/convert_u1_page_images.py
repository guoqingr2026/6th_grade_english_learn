#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert Unit 1 textbook JPG scans to page-XXX.png (pages 009–019)."""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("[ERROR] Install Pillow: python -m pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "assets" / "images" / "textbook" / "pages"
BACKUP_DIR = PAGES_DIR / "_backup" / datetime.now().strftime("%Y%m%d-%H%M%S")
RELEASE_PAGES = ROOT / "release" / "assets" / "images" / "textbook" / "pages"


def collect_jpg_sources() -> list[tuple[int, Path]]:
    """Map JPG files to textbook page numbers 009–019."""
    named: dict[int, Path] = {}
    img_series: list[tuple[int, Path]] = []

    for p in PAGES_DIR.iterdir():
        if not p.is_file():
            continue
        lower = p.name.lower()
        if not lower.endswith(".jpg"):
            continue
        m = re.match(r"page-(\d{3})\.png\.jpg$", lower)
        if m:
            named[int(m.group(1))] = p
            continue
        m = re.match(r"img_(\d+)\.png\.jpg$", lower)
        if m:
            img_series.append((int(m.group(1)), p))

    img_series.sort(key=lambda x: x[0])
    start = 11
    for idx, (_, path) in enumerate(img_series):
        named.setdefault(start + idx, path)

    pages = sorted(named.keys())
    return [(n, named[n]) for n in pages if 9 <= n <= 19]


def convert_and_install() -> None:
    sources = collect_jpg_sources()
    if not sources:
        print("[ERROR] No JPG sources found in", PAGES_DIR)
        raise SystemExit(1)

    print(f"[INFO] Converting {len(sources)} files:")
    for page_num, src in sources:
        print(f"  page-{page_num:03d}.png  <=  {src.name}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    jpg_backup = BACKUP_DIR / "source-jpg"
    jpg_backup.mkdir(exist_ok=True)

    for page_num, src in sources:
        dest = PAGES_DIR / f"page-{page_num:03d}.png"
        if dest.exists():
            shutil.copy2(dest, BACKUP_DIR / dest.name)

        img = Image.open(src)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(dest, "PNG", optimize=True)
        print(f"[OK] {dest.name} ({dest.stat().st_size // 1024} KB)")

        RELEASE_PAGES.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, RELEASE_PAGES / dest.name)

        shutil.move(str(src), jpg_backup / src.name)

    last = sources[-1][0]
    print(f"\n[DONE] Unit 1 pages updated: page-009.png – page-{last:03d}.png")
    print(f"[DONE] Backups: {BACKUP_DIR}")
    if last < 20:
        print("[NOTE] page-020.png was not uploaded; existing file kept.")


if __name__ == "__main__":
    convert_and_install()
