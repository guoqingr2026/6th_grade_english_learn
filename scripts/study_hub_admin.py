#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Host admin approval for remote Study Hub content edits."""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADMIN_CONFIG_PATH = ROOT / "data" / "study-hub" / "admin-config.json"
PENDING_DIR = ROOT / "data" / "study-hub" / "pending"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def hash_admin_pin(pin: str) -> str:
    value = 5381
    text = f"pep6-admin-{pin}"
    for ch in text:
        value = ((value << 5) + value) ^ ord(ch)
    return str(value & 0xFFFFFFFF)


def load_admin_config() -> dict:
    if not ADMIN_CONFIG_PATH.exists():
        return {"requireRemoteApproval": True, "adminPinHash": ""}
    try:
        data = json.loads(ADMIN_CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("invalid config")
    except (json.JSONDecodeError, OSError, ValueError):
        return {"requireRemoteApproval": True, "adminPinHash": ""}
    return {
        "requireRemoteApproval": bool(data.get("requireRemoteApproval", True)),
        "adminPinHash": str(data.get("adminPinHash") or ""),
    }


def save_admin_config(config: dict) -> dict:
    ADMIN_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "requireRemoteApproval": bool(config.get("requireRemoteApproval", True)),
        "adminPinHash": str(config.get("adminPinHash") or ""),
        "updatedAt": now_iso(),
    }
    ADMIN_CONFIG_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def verify_admin_pin(pin: str) -> bool:
    cfg = load_admin_config()
    stored = cfg.get("adminPinHash") or ""
    if not stored or not pin:
        return False
    return hash_admin_pin(pin) == stored


def setup_admin_pin(pin: str, require_remote_approval: bool = True) -> dict:
    cfg = load_admin_config()
    cfg["adminPinHash"] = hash_admin_pin(pin)
    cfg["requireRemoteApproval"] = bool(require_remote_approval)
    return save_admin_config(cfg)


def is_local_client_ip(ip: str) -> bool:
    return ip in ("127.0.0.1", "::1", "localhost")


def should_queue_edit(client_ip: str, admin_pin: str = "") -> bool:
    cfg = load_admin_config()
    if is_local_client_ip(client_ip):
        return False
    if admin_pin and verify_admin_pin(admin_pin):
        return False
    if not cfg.get("requireRemoteApproval"):
        return False
    if not cfg.get("adminPinHash"):
        return False
    return True


def _pending_path(edit_id: str) -> Path:
    safe = re.sub(r"[^\w\-]", "_", edit_id)[:64]
    return PENDING_DIR / f"{safe}.json"


def queue_pending_edit(payload: dict) -> dict:
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    edit_id = str(payload.get("id") or uuid.uuid4().hex[:12])
    entry = {
        "id": edit_id,
        "status": "pending",
        "createdAt": now_iso(),
        **payload,
    }
    _pending_path(edit_id).write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry


def list_pending_edits() -> list:
    if not PENDING_DIR.exists():
        return []
    items: list[dict] = []
    for path in sorted(PENDING_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "pending":
                preview = str(data.get("summary") or data.get("kind") or "")
                data["preview"] = preview[:120]
                items.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    return items[:50]


def get_pending_edit(edit_id: str) -> dict | None:
    path = _pending_path(edit_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def mark_pending_edit(edit_id: str, status: str) -> dict | None:
    entry = get_pending_edit(edit_id)
    if not entry:
        return None
    entry["status"] = status
    entry["resolvedAt"] = now_iso()
    _pending_path(edit_id).write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry
