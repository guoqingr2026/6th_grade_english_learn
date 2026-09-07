#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify textbook page PNGs exist per pdf-page-map.json (intro + units + appendix)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "data" / "study-hub" / "pdf-page-map.json"


def collect_pages(data: dict) -> list[tuple[str, str, int]]:
    out: list[tuple[str, str, int]] = []
    for key, sec in data.get("intro", {}).items():
        for num in sec.get("pdfPages", []):
            out.append(("intro", key, num))
    for unit, parts in data.get("units", {}).items():
        if not isinstance(parts, dict):
            continue
        for part, cfg in parts.items():
            if not isinstance(cfg, dict):
                continue
            for num in cfg.get("pdfPages", []):
                out.append((unit, part, num))
    for key, sec in data.get("appendix", {}).items():
        for num in sec.get("pdfPages", []):
            out.append(("appendix", key, num))
    return out


def main() -> None:
    if not MAP_PATH.exists():
        print("[WARN] pdf-page-map.json not found")
        sys.exit(0)
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    missing = []
    ok = 0
    for section, part, num in collect_pages(data):
        rel = f"assets/images/textbook/pages/page-{num:03d}.png"
        path = ROOT / rel.replace("/", "\\") if sys.platform == "win32" else ROOT / rel
        if path.exists():
            ok += 1
        else:
            missing.append((section, part, num, rel))
    print(f"[OK] {ok} images found")
    if missing:
        print(f"[WARN] {len(missing)} missing:")
        for section, part, num, rel in missing[:20]:
            print(f"  {section} {part} page {num}: {rel}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")
        sys.exit(1)
    print("[DONE] All mapped textbook images present.")


if __name__ == "__main__":
    main()
