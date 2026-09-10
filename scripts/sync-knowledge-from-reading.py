#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deprecated: use generate_u12_knowledge.py instead. Strips reading-excerpt only."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BANK = ROOT / "data" / "study-hub" / "knowledge-bank.json"
LIBRARY = ROOT / "data" / "study-hub" / "library" / "knowledge"


def strip_excerpt(html: str) -> str:
    return re.sub(
        r'<section class="reading-excerpt">[\s\S]*?</section>\s*',
        "",
        html or "",
    ).strip()


def main() -> None:
    bank = json.loads(KNOWLEDGE_BANK.read_text(encoding="utf-8"))
    n = 0
    for unit in bank.get("units") or []:
        for page in unit.get("pages") or []:
            old = page.get("bodyHtml") or ""
            new = strip_excerpt(old)
            if new != old:
                page["bodyHtml"] = new
                pid = page.get("id")
                if pid:
                    LIBRARY.joinpath(f"{pid}.html").write_text(new, encoding="utf-8")
                n += 1
    KNOWLEDGE_BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] stripped reading-excerpt from {n} page(s). Use generate_u12_knowledge.py for content.")


if __name__ == "__main__":
    main()
