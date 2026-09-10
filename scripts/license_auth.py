#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""License-based auth, session tokens, and encrypted sync storage for ECS deployment."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTH_DIR = ROOT / "data" / "auth"
LICENSES_FILE = AUTH_DIR / "licenses.json"
MASTER_KEY_FILE = AUTH_DIR / ".master_key"
JWT_SECRET_FILE = AUTH_DIR / ".jwt_secret"

TOKEN_TTL_SECONDS = int(os.environ.get("PEP6_TOKEN_TTL", str(7 * 24 * 3600)))
LICENSE_SEGMENT = 4


def auth_enabled() -> bool:
    return os.environ.get("PEP6_AUTH_REQUIRED", "0").strip() in ("1", "true", "yes", "on")


def allow_local_without_auth() -> bool:
    return os.environ.get("PEP6_AUTH_ALLOW_LOCAL", "1").strip() in ("1", "true", "yes", "on")


def _ensure_auth_dir() -> None:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)


def _load_secret_file(path: Path) -> bytes:
    if path.exists():
        return path.read_bytes()
    _ensure_auth_dir()
    secret = secrets.token_bytes(32)
    path.write_bytes(secret)
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return secret


def master_key() -> bytes:
    return _load_secret_file(MASTER_KEY_FILE)


def jwt_secret() -> bytes:
    return _load_secret_file(JWT_SECRET_FILE)


def hash_license(code: str) -> str:
    normalized = normalize_license_code(code)
    return hashlib.sha256(f"pep6-lic-{normalized}".encode("utf-8")).hexdigest()


def normalize_license_code(code: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", (code or "").upper())


def format_license_code(raw: str) -> str:
    body = normalize_license_code(raw)
    if len(body) < 12:
        body = (body + secrets.token_hex(8).upper())[:12]
    chunks = [body[i : i + LICENSE_SEGMENT] for i in range(0, 12, LICENSE_SEGMENT)]
    return "PEP6-" + "-".join(chunks)


def load_licenses() -> list[dict]:
    if not LICENSES_FILE.exists():
        return []
    try:
        data = json.loads(LICENSES_FILE.read_text(encoding="utf-8"))
        return data.get("licenses", []) if isinstance(data, dict) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_licenses(licenses: list[dict]) -> None:
    _ensure_auth_dir()
    LICENSES_FILE.write_text(
        json.dumps({"licenses": licenses}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def find_license_by_code(code: str) -> dict | None:
    digest = hash_license(code)
    for item in load_licenses():
        if item.get("hash") == digest and item.get("active", True):
            return item
    return None


def license_is_valid(item: dict) -> bool:
    if not item or not item.get("active", True):
        return False
    expires = str(item.get("expiresAt") or "").strip()
    if not expires:
        return True
    try:
        exp_dt = datetime.fromisoformat(expires.replace("Z", "+00:00"))
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        return exp_dt > datetime.now(timezone.utc)
    except ValueError:
        return False


def create_license(days: int, label: str = "", max_users: int = 0) -> dict:
    code = format_license_code(secrets.token_hex(6).upper())
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=max(1, int(days)))
    entry = {
        "id": f"lic_{secrets.token_hex(8)}",
        "hash": hash_license(code),
        "label": (label or "未命名授权").strip(),
        "expiresAt": expires.astimezone().isoformat(timespec="seconds"),
        "createdAt": now.astimezone().isoformat(timespec="seconds"),
        "maxUsers": int(max_users or 0),
        "active": True,
    }
    licenses = load_licenses()
    licenses.append(entry)
    save_licenses(licenses)
    return {"code": code, **entry}


def revoke_license(license_id: str) -> bool:
    licenses = load_licenses()
    changed = False
    for item in licenses:
        if item.get("id") == license_id:
            item["active"] = False
            changed = True
    if changed:
        save_licenses(licenses)
    return changed


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> bytes:
    pad = "=" * ((4 - len(text) % 4) % 4)
    return base64.urlsafe_b64decode(text + pad)


def sign_token(payload: dict) -> str:
    body = _b64url(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    sig = hmac.new(jwt_secret(), body.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def verify_token(token: str) -> dict | None:
    if not token or "." not in token:
        return None
    body, sig = token.rsplit(".", 1)
    expected = hmac.new(jwt_secret(), body.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return None
    try:
        payload = json.loads(_b64url_decode(body).decode("utf-8"))
    except (json.JSONDecodeError, ValueError):
        return None
    exp = int(payload.get("exp") or 0)
    if exp and time.time() > exp:
        return None
    lic_id = str(payload.get("lic") or "")
    lic = next((x for x in load_licenses() if x.get("id") == lic_id), None)
    if not lic or not license_is_valid(lic):
        return None
    return payload


def issue_session(license_item: dict) -> dict:
    now = int(time.time())
    payload = {
        "lic": license_item.get("id"),
        "label": license_item.get("label", ""),
        "iat": now,
        "exp": now + TOKEN_TTL_SECONDS,
    }
    token = sign_token(payload)
    return {
        "token": token,
        "expiresAt": datetime.fromtimestamp(payload["exp"], tz=timezone.utc).astimezone().isoformat(timespec="seconds"),
        "licenseLabel": license_item.get("label", ""),
        "licenseExpiresAt": license_item.get("expiresAt", ""),
    }


def login_with_license(code: str) -> dict:
    item = find_license_by_code(code)
    if not item:
        raise ValueError("授权码无效")
    if not license_is_valid(item):
        raise ValueError("授权码已过期或已停用")
    session = issue_session(item)
    return {"ok": True, **session}


def _fernet():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        return None
    key = base64.urlsafe_b64encode(hashlib.sha256(master_key()).digest())
    return Fernet(key)


def encrypt_bytes(raw: bytes) -> bytes:
    f = _fernet()
    if not f:
        return base64.b64encode(raw)
    return b"F1:" + f.encrypt(raw)


def decrypt_bytes(blob: bytes) -> bytes:
    if blob.startswith(b"F1:"):
        f = _fernet()
        if not f:
            raise RuntimeError("cryptography package required for encrypted data")
        return f.decrypt(blob[3:])
    try:
        return base64.b64decode(blob)
    except Exception:
        return blob


def read_encrypted_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    raw = path.read_bytes()
    if not raw:
        return None
    try:
        if auth_enabled():
            text = decrypt_bytes(raw).decode("utf-8")
        else:
            text = raw.decode("utf-8")
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError, ValueError):
        return None


def write_encrypted_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    if auth_enabled():
        path.write_bytes(encrypt_bytes(text))
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def public_license_rows() -> list[dict]:
    rows = []
    for item in load_licenses():
        rows.append(
            {
                "id": item.get("id"),
                "label": item.get("label"),
                "expiresAt": item.get("expiresAt"),
                "createdAt": item.get("createdAt"),
                "maxUsers": item.get("maxUsers", 0),
                "active": bool(item.get("active", True)),
                "valid": license_is_valid(item),
            }
        )
    return rows
