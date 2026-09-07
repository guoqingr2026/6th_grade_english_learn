#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync question bank JSON from Markdown bank-json blocks, then validate."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_DIR = ROOT / "data" / "question-banks"

BANK_PAIRS = [
    ("quiz-bank.md", "quiz-bank.json"),
    ("fillblank-bank.md", "fillblank-bank.json"),
    ("writing-bank.md", "writing-bank.json"),
]

BLOCK_RE = re.compile(r"```bank-json\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)


def extract_bank_json(md_text: str) -> dict | None:
    match = BLOCK_RE.search(md_text)
    if not match:
        return None
    return json.loads(match.group(1))


def validate_bank(name: str, data: dict) -> list[str]:
    errors: list[str] = []
    if "version" not in data:
        errors.append(f"{name}: 缺少 version 字段")
    if name.startswith("writing"):
        samples = data.get("samples")
        if not isinstance(samples, list):
            errors.append(f"{name}: samples 必须是数组")
        else:
            for i, item in enumerate(samples):
                for key in ("id", "unit", "title", "en", "zh", "fillPrompt", "fillAnswer"):
                    if key not in item:
                        errors.append(f"{name}: samples[{i}] 缺少 {key}")
    else:
        questions = data.get("questions")
        if not isinstance(questions, list):
            errors.append(f"{name}: questions 必须是数组")
        else:
            for i, item in enumerate(questions):
                if "id" not in item:
                    errors.append(f"{name}: questions[{i}] 缺少 id")
    return errors


def main() -> int:
    print("[同步] 检查题库 Markdown -> JSON ...")
    updated = 0
    skipped = 0

    for md_name, json_name in BANK_PAIRS:
        md_path = BANK_DIR / md_name
        json_path = BANK_DIR / json_name
        if not md_path.exists():
            print(f"  - 跳过 {md_name}（文件不存在）")
            skipped += 1
            continue

        md_text = md_path.read_text(encoding="utf-8")
        payload = extract_bank_json(md_text)
        if payload is None:
            if json_path.exists():
                print(f"  - 保持 {json_name}（{md_name} 无 bank-json 代码块，未改动）")
            else:
                print(f"  - 警告 {json_name} 不存在，且 {md_name} 无 bank-json 块")
            skipped += 1
            continue

        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  + 已更新 {json_name} <- {md_name}")
        updated += 1

    print("[校验] 验证 JSON 题库 ...")
    all_errors: list[str] = []
    for _, json_name in BANK_PAIRS:
        json_path = BANK_DIR / json_name
        if not json_path.exists():
            all_errors.append(f"缺少文件: {json_name}")
            continue
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            all_errors.append(f"{json_name}: JSON 解析失败 - {exc}")
            continue
        all_errors.extend(validate_bank(json_name, data))

    if all_errors:
        print("[错误] 题库校验未通过：")
        for err in all_errors:
            print(f"  ! {err}")
        return 1

    print(f"[完成] 同步 {updated} 个，保持 {skipped} 个；全部 JSON 校验通过。")
    print("[提示] 刷新浏览器即可看到最新题库（Ctrl+F5 强制刷新）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
