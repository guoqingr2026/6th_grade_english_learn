#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download CC-licensed Wikimedia images for Unit 1 study-hub page thumbnails."""

from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "images" / "textbook" / "pages"
OUT.mkdir(parents=True, exist_ok=True)

# Wikimedia Commons — educational landmark photos (CC / public domain)
IMAGES = {
    "page-009.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/960px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg",
    "page-010.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Full_View_Of_The_Terracotta_Army.JPG/960px-Full_View_Of_The_Terracotta_Army.JPG",
    "page-011.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Great_Wall_at_Mutianyu.jpg/960px-Great_Wall_at_Mutianyu.jpg",
    "page-013.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Terracotta_Army%2C_View_of_Terracotta_Army_pits%2C_Xian.jpg/960px-Terracotta_Army%2C_View_of_Terracotta_Army_pits%2C_Xian.jpg",
    "page-017.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Xian_City_Wall_South_Gate.jpg/960px-Xian_City_Wall_South_Gate.jpg",
    "page-019.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Oamaru_Railway_Station_01.jpg/960px-Oamaru_Railway_Station_01.jpg",
}


def fetch(name: str, url: str) -> None:
    dest = OUT / name
    print(f"Fetching {name} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "PEP6-StudyHub/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    print(f"  -> {dest} ({dest.stat().st_size // 1024} KB)")


def main() -> None:
    for name, url in IMAGES.items():
        try:
            fetch(name, url)
        except Exception as e:
            print(f"  [WARN] {name}: {e}")
    print("[OK] Unit 1 page images ready under assets/images/textbook/pages/")


if __name__ == "__main__":
    main()
