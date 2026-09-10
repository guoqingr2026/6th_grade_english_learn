#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set PEP6 subpath in index.html meta tag for ECS subfolder deployment."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


def main() -> int:
    web_path = sys.argv[1] if len(sys.argv) > 1 else ""
    web_path = web_path.strip().rstrip("/")
    if web_path and not web_path.startswith("/"):
        web_path = f"/{web_path}"

    text = INDEX.read_text(encoding="utf-8")
    meta = f'<meta name="pep6-base" content="{web_path}" />'
    if 'name="pep6-base"' in text:
        text = re.sub(r'<meta name="pep6-base"[^>]*/>', meta, text, count=1)
    else:
        text = text.replace("<head>", f"<head>\n    {meta}", 1)
    INDEX.write_text(text, encoding="utf-8")
    print(f"pep6-base set to: {web_path or '(root)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
