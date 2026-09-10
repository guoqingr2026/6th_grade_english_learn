#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate time-limited license codes for PEP6 English Trainer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import license_auth  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PEP6 license code")
    parser.add_argument("--days", type=int, default=365, help="Valid days (default 365)")
    parser.add_argument("--label", type=str, default="", help="Label, e.g. Class 6-1")
    parser.add_argument("--max-users", type=int, default=0, help="0 = unlimited sync users")
    parser.add_argument("--list", action="store_true", help="List existing licenses")
    parser.add_argument("--revoke", type=str, default="", help="Revoke license by id")
    args = parser.parse_args()

    if args.list:
        for row in license_auth.public_license_rows():
            status = "有效" if row["valid"] and row["active"] else "无效"
            print(f"{row['id']} | {row['label']} | 到期 {row['expiresAt']} | {status}")
        return 0

    if args.revoke:
        ok = license_auth.revoke_license(args.revoke.strip())
        print("已停用" if ok else "未找到授权")
        return 0 if ok else 1

    created = license_auth.create_license(args.days, args.label, args.max_users)
    print("=== 新授权码（请妥善保存，仅显示一次）===")
    print(created["code"])
    print(f"标签: {created['label']}")
    print(f"到期: {created['expiresAt']}")
    print(f"ID: {created['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
