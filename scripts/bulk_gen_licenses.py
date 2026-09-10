#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-generate license codes and export to CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import license_auth  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch generate PEP6 licenses")
    parser.add_argument("--monthly", type=int, default=0, help="Count of 30-day licenses")
    parser.add_argument("--yearly", type=int, default=0, help="Count of 365-day licenses")
    parser.add_argument(
        "--export",
        type=str,
        default="",
        help="CSV export path (default: data/auth/licenses-export-YYYYMMDD-HHMM.csv)",
    )
    args = parser.parse_args()

    if args.monthly <= 0 and args.yearly <= 0:
        print("请指定 --monthly 或 --yearly 数量")
        return 1

    created: list[dict] = []
    for i in range(1, args.monthly + 1):
        created.append(license_auth.create_license(30, f"月卡-{i:03d}"))
    for i in range(1, args.yearly + 1):
        created.append(license_auth.create_license(365, f"年卡-{i:02d}"))

    export_path = Path(args.export) if args.export else (
        ROOT / "data" / "auth" / f"licenses-export-{datetime.now().strftime('%Y%m%d-%H%M')}.csv"
    )
    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["授权码", "标签", "有效天数", "到期时间", "ID"])
        for row in created:
            days = 30 if str(row.get("label", "")).startswith("月卡") else 365
            writer.writerow([row["code"], row["label"], days, row["expiresAt"], row["id"]])

    print(f"已生成 {len(created)} 个授权码（月卡 {args.monthly} + 年卡 {args.yearly}）")
    print(f"CSV 已保存: {export_path}")
    print("--- 授权码列表（请妥善保存）---")
    for row in created:
        print(f"{row['code']}  |  {row['label']}  |  到期 {row['expiresAt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
