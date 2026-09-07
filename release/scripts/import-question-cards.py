#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import question card packs from data/question-banks/import-cards/*.json into bank JSON files."""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_DIR = ROOT / "data" / "question-banks"
IMPORT_DIR = BANK_DIR / "import-cards"
DONE_DIR = IMPORT_DIR / "done"
TEMPLATE_DIR = IMPORT_DIR / "_templates"

TARGET_MAP = {
    "quiz": "quiz-bank.json",
    "fillblank": "fillblank-bank.json",
    "writing": "writing-bank.json",
}

ITEM_KEY = {
    "quiz": "questions",
    "fillblank": "questions",
    "writing": "samples",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_items(existing: list, incoming: list, action: str) -> tuple[list, int, int]:
    if action == "replace":
        return incoming, len(incoming), 0
    by_id = {str(item.get("id")): item for item in existing if item.get("id")}
    added = 0
    updated = 0
    for item in incoming:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            raise ValueError("题卡缺少 id 字段")
        if item_id in by_id:
            by_id[item_id] = item
            updated += 1
        else:
            by_id[item_id] = item
            added += 1
    merged = list(by_id.values())
    merged.sort(key=lambda x: str(x.get("id", "")))
    return merged, added, updated


def import_card_file(card_path: Path) -> tuple[bool, str]:
    payload = load_json(card_path)
    card_type = str(payload.get("cardType", "")).strip().lower()
    if card_type not in TARGET_MAP:
        return False, f"未知 cardType: {card_type}"

    items = payload.get("items")
    if not isinstance(items, list) or len(items) == 0:
        return False, "items 必须是非空数组"

    action = str(payload.get("action", "append")).strip().lower()
    if action not in {"append", "replace"}:
        return False, f"不支持 action: {action}"

    bank_path = BANK_DIR / TARGET_MAP[card_type]
    if not bank_path.exists():
        bank_data = {"version": 1, "description": f"由题卡导入生成 - {card_type}", ITEM_KEY[card_type]: []}
    else:
        bank_data = load_json(bank_path)

    key = ITEM_KEY[card_type]
    current = bank_data.get(key, [])
    if not isinstance(current, list):
        current = []

    merged, added, updated = merge_items(current, items, action)
    bank_data[key] = merged
    bank_data["version"] = bank_data.get("version", 1)
    bank_data["lastImportAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if payload.get("source"):
        bank_data["lastImportSource"] = str(payload.get("source"))

    save_json(bank_path, bank_data)
    return True, f"导入 {card_path.name}: 新增 {added}，更新 {updated}，合计 {len(merged)} 条"


def main() -> int:
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    card_files = sorted(
        p for p in IMPORT_DIR.glob("*.json")
        if p.is_file() and not p.name.startswith("_")
    )

    if not card_files:
        print("[导入] import-cards 目录暂无待导入题卡（可将 *.json 题卡包放入该目录）。")
        return 0

    print(f"[导入] 发现 {len(card_files)} 个题卡包 ...")
    errors: list[str] = []
    imported = 0

    for card_path in card_files:
        try:
            ok, message = import_card_file(card_path)
            if ok:
                print(f"  + {message}")
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                dest = DONE_DIR / f"{card_path.stem}-{stamp}{card_path.suffix}"
                shutil.move(str(card_path), str(dest))
                imported += 1
            else:
                errors.append(f"{card_path.name}: {message}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{card_path.name}: {exc}")

    if errors:
        print("[错误] 以下题卡导入失败：")
        for err in errors:
            print(f"  ! {err}")
        return 1

    print(f"[完成] 成功导入 {imported} 个题卡包。请刷新浏览器查看（Ctrl+F5）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
