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
    parser.add_argument("--weekly", type=int, default=0, help="Count of 7-day licenses (周卡)")
    parser.add_argument("--monthly", type=int, default=0, help="Count of 30-day licenses (月卡)")
    parser.add_argument("--quarterly", type=int, default=0, help="Count of 90-day licenses (季卡)")
    parser.add_argument("--yearly", type=int, default=0, help="Count of 365-day licenses (年卡)")
    parser.add_argument(
        "--export",
        type=str,
        default="",
        help="CSV export path (default: data/auth/licenses-export-YYYYMMDD-HHMM.csv)",
    )
    args = parser.parse_args()

    batches: list[tuple[int, str, int]] = [
        (args.weekly, "周卡", 7),
        (args.monthly, "月卡", 30),
        (args.quarterly, "季卡", 90),
        (args.yearly, "年卡", 365),
    ]
    total = sum(n for n, _, _ in batches)
    if total <= 0:
        print("请指定数量，例如: --weekly 100 --monthly 100 --quarterly 100 --yearly 10")
        return 1

    created: list[dict] = []
    for count, prefix, days in batches:
        width = 3 if count >= 100 else 2
        for i in range(1, count + 1):
            row = license_auth.create_license(days, f"{prefix}-{i:0{width}d}")
            row["days"] = days
            created.append(row)

    export_path = Path(args.export) if args.export else (
        ROOT / "data" / "auth" / f"licenses-export-{datetime.now().strftime('%Y%m%d-%H%M')}.csv"
    )
    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["授权码", "标签", "类型", "有效天数", "到期时间", "ID"])
        for row in created:
            label = str(row.get("label") or "")
            kind = label.split("-", 1)[0] if label else ""
            writer.writerow([row["code"], label, kind, row["days"], row["expiresAt"], row["id"]])

    print(
        f"已生成 {len(created)} 个授权码"
        f"（周卡 {args.weekly} + 月卡 {args.monthly} + 季卡 {args.quarterly} + 年卡 {args.yearly}）"
    )
    print(f"CSV 已保存: {export_path}")
    print("--- 授权码列表（请妥善保存）---")
    for row in created:
        print(f"{row['code']}  |  {row['label']}  |  {row['days']}天  |  到期 {row['expiresAt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
