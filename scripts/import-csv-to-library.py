#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import word-sources/Unit*.csv into data/study-hub/library/reading/*.html"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import study_hub_library as lib

WORD_DIR = ROOT / "word-sources"


def main() -> None:
    files = sorted(WORD_DIR.glob("Unit*.csv"))
    if not files:
        print("[SKIP] no Unit*.csv in word-sources/")
        return
    total_pages = 0
    for path in files:
        m = re.search(r"unit\s*(\d+)", path.stem, re.I)
        unit = int(m.group(1)) if m else 1
        text = lib.read_csv_text(path=path)
        try:
            result = lib.import_csv_to_library(text, unit)
            total_pages += result.get("pages", 0)
            print(f"  [CSV→HTML] Unit {unit}: {path.name} → {result.get('pages', 0)} pages")
        except ValueError as e:
            print(f"  [WARN] {path.name}: {e}")
    print(f"[OK] HTML library: {total_pages} page file(s) in data/study-hub/library/reading/")


if __name__ == "__main__":
    main()
