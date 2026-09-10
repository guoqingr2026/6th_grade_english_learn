#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static file server + LAN sync API (field-level merge + logs)."""

from __future__ import annotations

import base64
import json
import os
import re
import socket
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
SYNC_DIR = ROOT / "lan-sync"
MAX_LOGS = 100
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

sys.path.insert(0, str(ROOT / "scripts"))
try:
    import study_hub_library as hub_lib
except ImportError:
    hub_lib = None
try:
    import study_hub_admin as admin_lib
except ImportError:
    admin_lib = None
try:
    import license_auth
except ImportError:
    license_auth = None


def _is_private_ipv4(ip: str) -> bool:
    if not ip or ip.startswith("127."):
        return False
    if ip.startswith("192.168.") or ip.startswith("10."):
        return True
    if ip.startswith("172."):
        try:
            second = int(ip.split(".")[1])
            return 16 <= second <= 31
        except (ValueError, IndexError):
            return False
    return False


def get_lan_ipv4_addresses() -> list[str]:
    found: set[str] = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip and not ip.startswith("127."):
                found.add(ip)
    except OSError:
        pass
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(("8.8.8.8", 80))
        ip = probe.getsockname()[0]
        probe.close()
        if ip and not ip.startswith("127."):
            found.add(ip)
    except OSError:
        pass
    private = sorted(ip for ip in found if _is_private_ipv4(ip))
    if private:
        return private
    return sorted(ip for ip in found if not ip.startswith("127."))


def primary_mobile_url(port: int = PORT) -> tuple[str, list[str]]:
    ips = get_lan_ipv4_addresses()
    if not ips:
        return "", []
    return f"http://{ips[0]}:{int(port)}", ips


def run_study_hub_refresh() -> None:
    py = sys.executable
    scripts = ROOT / "scripts"
    subprocess.run([py, str(scripts / "import-word-study.py")], cwd=str(ROOT), check=True)
    subprocess.run([py, str(scripts / "build-study-hub.py")], cwd=str(ROOT), check=True)


def save_uploaded_word(unit: int, filename: str, raw: bytes) -> Path:
    word_dir = ROOT / "word-sources"
    word_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\u4e00-\u9fff.\-]", "_", filename or f"Unit{unit}.docx")
    if not any(low.endswith(ext) for ext in (".docx", ".doc", ".csv", ".txt")):
        safe_name += ".csv"
    if not re.search(r"unit\s*\d+", safe_name, re.I):
        safe_name = f"Unit{unit}_课文词汇重点句型_双语学习资料.docx"
    dest = word_dir / safe_name
    dest.write_bytes(raw)
    return dest


def safe_sync_id(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    cleaned = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", text)
    return cleaned[:64]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_ts(value: str) -> float:
    if not value:
        return 0.0
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def data_path(sync_id: str) -> Path:
    return SYNC_DIR / f"{sync_id}.json"


def load_sync_payload(sync_id: str) -> dict | None:
    path = data_path(sync_id)
    if license_auth:
        return license_auth.read_encrypted_json(path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def save_sync_payload(sync_id: str, payload: dict) -> None:
    path = data_path(sync_id)
    if license_auth:
        license_auth.write_encrypted_json(path, payload)
        return
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def log_path(sync_id: str) -> Path:
    return SYNC_DIR / f"{sync_id}-logs.json"


def load_logs(sync_id: str) -> list:
    path = log_path(sync_id)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_logs(sync_id: str, logs: list) -> None:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    trimmed = logs[-MAX_LOGS:]
    log_path(sync_id).write_text(json.dumps(trimmed, ensure_ascii=False, indent=2), encoding="utf-8")


def append_log(sync_id: str, entry: dict) -> list:
    logs = load_logs(sync_id)
    logs.append(entry)
    save_logs(sync_id, logs)
    return logs[-20:]


STAT_NUM_KEYS = (
    "correct",
    "wrong",
    "attempts",
    "points",
    "highestPoints",
    "highestAccumulated",
    "accumulatedPoints",
    "behaviorPointsTotal",
    "redeemedTotal",
)


def _as_int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def merge_stats(a: dict | None, b: dict | None) -> dict:
    left = dict(a or {})
    right = dict(b or {})
    out = {**left, **right}
    for key in STAT_NUM_KEYS:
        out[key] = max(_as_int(left.get(key)), _as_int(right.get(key)))
    for key in ("lastPracticeAt", "lastCompoundDate", "lastSpendDate"):
        left_val = str(left.get(key) or "")
        right_val = str(right.get(key) or "")
        out[key] = max(left_val, right_val) if left_val and right_val else (left_val or right_val)
    return out


def dashboard_reset_at(payload: dict | None) -> str:
    return str((payload or {}).get("dashboardResetAt") or "")


def apply_dashboard_reset_slice(merged: dict, source: dict, reset_at: str) -> None:
    merged["dashboardResetAt"] = reset_at
    merged["stats"] = dict(source.get("stats") or {})
    merged["wrongQuizIds"] = list(source.get("wrongQuizIds") or [])
    merged["wrongBookItems"] = list(source.get("wrongBookItems") or [])
    merged["rewarded"] = dict(source.get("rewarded") or {})
    merged["challengeLogs"] = list(source.get("challengeLogs") or [])
    merged["behaviorLogs"] = list(source.get("behaviorLogs") or [])
    merged["redeemLogs"] = list(source.get("redeemLogs") or [])
    merged["badges"] = list(source.get("badges") or [])
    merged["leaderboard"] = list(source.get("leaderboard") or [])


def merge_unique_strings(items_a, items_b) -> list:
    seen: set[str] = set()
    out: list = []
    for item in list(items_a or []) + list(items_b or []):
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def merge_rewarded(a: dict | None, b: dict | None) -> dict:
    left = a or {}
    right = b or {}
    cats = set(left.keys()) | set(right.keys())
    return {cat: merge_unique_strings(left.get(cat), right.get(cat)) for cat in cats}


def merge_by_id(items_a, items_b, id_key: str = "id") -> list:
    merged: dict[str, dict] = {}
    for item in list(items_a or []) + list(items_b or []):
        if not isinstance(item, dict):
            continue
        key = str(item.get(id_key) or item.get("time") or json.dumps(item, sort_keys=True, ensure_ascii=False))
        merged[key] = {**merged.get(key, {}), **item}
    return list(merged.values())


def merge_wrong_book_items(items_a, items_b) -> list:
    merged: dict[str, dict] = {}
    for item in list(items_a or []) + list(items_b or []):
        if not isinstance(item, dict):
            continue
        key = f"{item.get('module', '')}|{item.get('prompt', '')}"
        merged[key] = {**merged.get(key, {}), **item}
    return list(merged.values())


def merge_custom_banks(a: dict | None, b: dict | None) -> dict:
    left = a or {}
    right = b or {}
    return {
        "quiz": merge_by_id(left.get("quiz"), right.get("quiz")),
        "fillblank": merge_by_id(left.get("fillblank"), right.get("fillblank")),
        "writing": merge_by_id(left.get("writing"), right.get("writing")),
    }


def merge_knowledge_pages(pages_a, pages_b) -> list:
    merged: dict[str, dict] = {}
    for item in list(pages_a or []) + list(pages_b or []):
        if not isinstance(item, dict):
            continue
        page_id = str(item.get("id") or "")
        if not page_id:
            continue
        prev = merged.get(page_id, {})
        body_prev = str(prev.get("bodyHtml") or "")
        body_new = str(item.get("bodyHtml") or "")
        winner = item if len(body_new) >= len(body_prev) else prev
        merged[page_id] = {**prev, **item, **winner}
    return list(merged.values())


def merge_knowledge_custom(a: dict | None, b: dict | None) -> dict | None:
    if not a and not b:
        return None
    left = dict(a or {})
    right = dict(b or {})
    out = {**left, **right}
    unit_map: dict[int, dict] = {}
    for bank in (left, right):
        for unit in bank.get("units") or []:
            if not isinstance(unit, dict):
                continue
            unit_num = _as_int(unit.get("unit"))
            entry = unit_map.setdefault(unit_num, {"unit": unit_num, "pages": []})
            entry["pages"] = merge_knowledge_pages(entry.get("pages"), unit.get("pages"))
    out["units"] = sorted(unit_map.values(), key=lambda item: _as_int(item.get("unit")))
    appendix_pages: list = []
    for bank in (left, right):
        appendix = bank.get("appendix") or {}
        appendix_pages = merge_knowledge_pages(appendix_pages, appendix.get("pages"))
    if appendix_pages:
        out["appendix"] = {**(left.get("appendix") or right.get("appendix") or {}), "pages": appendix_pages}
    return out


def merge_mastery_progress(a: dict | None, b: dict | None) -> dict:
    left = dict(a or {})
    right = dict(b or {})
    out = {**left, **right}
    parts: dict[str, dict] = {}
    for bank in (left, right):
        for part_id, record in (bank.get("parts") or {}).items():
            if not isinstance(record, dict):
                continue
            prev = parts.get(part_id, {})
            parts[part_id] = {**prev, **record}
            if record.get("passed"):
                parts[part_id]["passed"] = True
            parts[part_id]["bestScore"] = max(_as_int(prev.get("bestScore")), _as_int(record.get("bestScore")))
    out["parts"] = parts
    return out


def merge_logs(items_a, items_b, limit: int = 200) -> list:
    merged = list(items_a or []) + list(items_b or [])
    seen: set[str] = set()
    out: list = []
    for item in reversed(merged):
        if not isinstance(item, dict):
            continue
        key = f"{item.get('time', '')}|{item.get('type', item.get('action', ''))}|{item.get('message', item.get('result', ''))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if len(out) >= limit:
            break
    return list(reversed(out))


def payload_body(payload: dict | None) -> dict:
    body = dict(payload or {})
    body.pop("updatedAt", None)
    return body


def payloads_equal(left: dict | None, right: dict | None) -> bool:
    return json.dumps(payload_body(left), sort_keys=True, ensure_ascii=False) == json.dumps(
        payload_body(right), sort_keys=True, ensure_ascii=False
    )


def merge_sync_payload(client_payload: dict, server_payload: dict | None) -> dict:
    if not server_payload:
        out = dict(client_payload)
        if dashboard_reset_at(out):
            apply_dashboard_reset_slice(out, out, dashboard_reset_at(out))
        return out
    server = server_payload
    client = client_payload
    client_reset = dashboard_reset_at(client)
    server_reset = dashboard_reset_at(server)
    merged = {
        "version": max(_as_int(client.get("version")), _as_int(server.get("version"))),
        "updatedAt": str(server.get("updatedAt") or client.get("updatedAt") or now_iso()),
        "stats": merge_stats(client.get("stats"), server.get("stats")),
        "studentProfile": {**(server.get("studentProfile") or {}), **(client.get("studentProfile") or {})},
        "wrongQuizIds": merge_unique_strings(client.get("wrongQuizIds"), server.get("wrongQuizIds")),
        "challengeLogs": merge_logs(client.get("challengeLogs"), server.get("challengeLogs")),
        "redeemLogs": merge_logs(client.get("redeemLogs"), server.get("redeemLogs")),
        "journalEntries": merge_by_id(client.get("journalEntries"), server.get("journalEntries"), "time"),
        "wrongBookItems": merge_wrong_book_items(client.get("wrongBookItems"), server.get("wrongBookItems")),
        "leaderboard": merge_by_id(client.get("leaderboard"), server.get("leaderboard"), "name"),
        "behaviorLogs": merge_logs(client.get("behaviorLogs"), server.get("behaviorLogs")),
        "badges": merge_by_id(client.get("badges"), server.get("badges"), "id"),
        "rewarded": merge_rewarded(client.get("rewarded"), server.get("rewarded")),
        "customBanks": merge_custom_banks(client.get("customBanks"), server.get("customBanks")),
        "studyHubNotes": {**(server.get("studyHubNotes") or {}), **(client.get("studyHubNotes") or {})},
        "studyHubState": {**(server.get("studyHubState") or {}), **(client.get("studyHubState") or {})},
        "studyHubKnowledgeCustom": merge_knowledge_custom(
            client.get("studyHubKnowledgeCustom"),
            server.get("studyHubKnowledgeCustom"),
        ),
        "masteryProgress": merge_mastery_progress(client.get("masteryProgress"), server.get("masteryProgress")),
        "dashboardResetAt": max(client_reset, server_reset) if client_reset or server_reset else "",
    }
    if client_reset and client_reset > server_reset:
        apply_dashboard_reset_slice(merged, client, client_reset)
    elif server_reset and server_reset > client_reset:
        apply_dashboard_reset_slice(merged, server, server_reset)
    return merged


def make_log(action: str, device: str, message: str, winner_at: str) -> dict:
    return {
        "time": now_iso(),
        "device": device or "未知设备",
        "action": action,
        "message": message,
        "updatedAt": winner_at,
    }


def merge_payload(sync_id: str, client_payload: dict, device: str) -> dict:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    client_device = device or "未知设备"
    file_path = data_path(sync_id)

    if not file_path.exists():
        payload = dict(client_payload)
        payload["updatedAt"] = payload.get("updatedAt") or now_iso()
        save_sync_payload(sync_id, payload)
        entry = make_log(
            "initialized",
            client_device,
            "首次同步，已建立班级数据副本",
            str(payload.get("updatedAt", "")),
        )
        recent = append_log(sync_id, entry)
        return {"action": "initialized", "payload": payload, "log": entry, "logs": recent}

    server_payload = load_sync_payload(sync_id) or {}
    merged = merge_sync_payload(client_payload, server_payload)
    if payloads_equal(merged, server_payload):
        action = "same"
        entry = make_log(
            "same",
            client_device,
            "数据已是最新，无需变更",
            str(server_payload.get("updatedAt", "")),
        )
        recent = append_log(sync_id, entry)
        return {"action": action, "payload": server_payload, "log": entry, "logs": recent}
    merged["updatedAt"] = now_iso()
    save_sync_payload(sync_id, merged)
    entry = make_log(
        "merged",
        client_device,
        "已合并本机与班级数据（积分、错题、精讲等双向同步）",
        str(merged.get("updatedAt", "")),
    )
    recent = append_log(sync_id, entry)
    return {"action": "merged", "payload": merged, "log": entry, "logs": recent}


class LanHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        path = urlparse(self.path).path
        if (
            path.startswith("/data/study-hub/")
            or path.endswith("/study-hub.js")
            or path.startswith("/assets/images/textbook/pages/")
            or path.startswith("/data/study-hub/library/media/")
        ):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        if str(args[0]).startswith("GET /api/"):
            return
        super().log_message(fmt, *args)

    def send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        text = raw.decode("utf-8-sig", errors="replace")
        return json.loads(text)

    def read_raw_body(self) -> str:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        text = raw.decode("utf-8-sig", errors="replace")
        return hub_lib.sanitize_text(text) if hub_lib else text

    def client_ip(self) -> str:
        return self.client_address[0] or ""

    def admin_pin_from_request(self, qs: dict | None = None) -> str:
        header_pin = (self.headers.get("X-Admin-Pin") or "").strip()
        if header_pin:
            return header_pin
        if qs:
            return str(qs.get("adminPin", [""])[0]).strip()
        return ""

    def bearer_token(self) -> str:
        auth = (self.headers.get("Authorization") or "").strip()
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        return (self.headers.get("X-Auth-Token") or "").strip()

    def auth_required(self) -> bool:
        return bool(license_auth and license_auth.auth_enabled())

    def local_auth_bypass(self) -> bool:
        return bool(
            license_auth
            and license_auth.allow_local_without_auth()
            and admin_lib
            and admin_lib.is_local_client_ip(self.client_ip())
        )

    def expose_lan_urls(self) -> bool:
        flag = os.environ.get("PEP6_EXPOSE_LAN_URLS", "").strip().lower()
        if flag in ("0", "false", "no", "off"):
            return False
        if flag in ("1", "true", "yes", "on"):
            return True
        return not self.auth_required()

    def ensure_license_auth(self) -> dict | None:
        if not self.auth_required() or self.local_auth_bypass():
            return {}
        token = self.bearer_token()
        claims = license_auth.verify_token(token) if token and license_auth else None
        if not claims:
            self.send_json(401, {"error": "需要有效授权码登录", "authRequired": True})
            return None
        return claims

    def ensure_admin_auth(self) -> dict | None:
        claims = self.ensure_license_auth()
        if claims is None:
            return None
        if self.auth_required() and not self.local_auth_bypass():
            if str(claims.get("role") or "") != "admin":
                self.send_json(403, {"error": "需要管理员权限"})
                return None
        return claims

    def queue_or_apply_save(
        self,
        kind: str,
        content: str,
        meta: dict,
        admin_pin: str = "",
        device: str = "",
    ) -> dict:
        if not admin_lib:
            return self.handle_save_page(kind, content, **meta)
        if admin_lib.should_queue_edit(self.client_ip(), admin_pin):
            summary = f"{kind} · {meta.get('pageId') or meta.get('scope', '')} p{meta.get('png', '')}"
            entry = admin_lib.queue_pending_edit(
                {
                    "kind": kind,
                    "content": content,
                    "meta": meta,
                    "device": device or self.headers.get("User-Agent", "")[:80],
                    "clientIp": self.client_ip(),
                    "summary": summary,
                }
            )
            return {
                "ok": True,
                "pending": True,
                "pendingId": entry.get("id"),
                "message": "已提交主机管理员审核，批准后将写入数据库",
            }
        return self.handle_save_page(kind, content, **meta)

    def apply_pending_edit(self, entry: dict) -> dict:
        if not hub_lib:
            raise RuntimeError("library module missing")
        kind = str(entry.get("kind") or "")
        content = str(entry.get("content") or "")
        meta = entry.get("meta") if isinstance(entry.get("meta"), dict) else {}
        if kind == "reading":
            return self.handle_save_page(
                "reading",
                content,
                unit=int(meta.get("unit") or 1),
                png=int(meta.get("png") or 0),
                scope=str(meta.get("scope") or "unit"),
            )
        if kind == "knowledge":
            return self.handle_save_page(
                "knowledge",
                content,
                page_id=str(meta.get("page_id") or meta.get("pageId") or "").strip(),
            )
        if kind == "import-csv":
            return hub_lib.import_csv_to_library(content, int(meta.get("unit") or 1))
        raise ValueError("unsupported pending kind")

    def handle_save_page(
        self,
        kind: str,
        content: str,
        unit: int = 1,
        png: int = 0,
        page_id: str = "",
        scope: str = "unit",
    ) -> dict:
        if not hub_lib:
            raise RuntimeError("library module missing")
        if kind == "reading":
            content = hub_lib.normalize_knowledge_content(content)
        elif kind == "knowledge":
            content = hub_lib.normalize_knowledge_content(content)
        else:
            raise ValueError("invalid kind")
        if not content:
            raise ValueError("empty content")
        if kind == "reading":
            if png <= 0:
                raise ValueError("png required")
            path = hub_lib.save_reading_page(unit, png, content, scope=scope)
            csv_path = hub_lib.unit_csv_path(unit) if scope == "unit" else None
            return {
                "ok": True,
                "path": str(path.relative_to(ROOT)),
                "printedPage": hub_lib.printed_page_for_png(png),
                "scope": scope,
                "csvSynced": bool(csv_path and csv_path.exists()),
                "csvPath": str(csv_path.relative_to(ROOT)) if csv_path and csv_path.exists() else "",
            }
        if kind == "knowledge":
            if not page_id:
                raise ValueError("pageId required")
            path = hub_lib.save_knowledge_page(page_id, content)
            return {"ok": True, "path": str(path.relative_to(ROOT))}
        raise ValueError("invalid kind")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Pin, Authorization, X-Auth-Token")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/ping":
            expose_lan = self.expose_lan_urls()
            mobile_url, lan_ips = primary_mobile_url(PORT) if expose_lan else ("", [])
            if expose_lan:
                lan_ips = [ip for ip in lan_ips if _is_private_ipv4(ip)]
                if not lan_ips:
                    mobile_url = ""
            self.send_json(
                200,
                {
                    "ok": True,
                    "service": "lan-sync",
                    "studyHubApi": 3,
                    "port": PORT,
                    "exposeLanUrls": expose_lan,
                    "lanIps": lan_ips if expose_lan else [],
                    "mobileUrl": mobile_url if expose_lan else "",
                    "features": [
                        "save-page",
                        "save-page-raw",
                        "import-csv",
                        "library-page",
                        "upload-media",
                        "save-student-audio",
                        "save-snip",
                        "list-snips",
                        "admin-approval",
                        "license-auth",
                    ],
                    "authRequired": self.auth_required() and not self.local_auth_bypass(),
                    "isLocalClient": admin_lib.is_local_client_ip(self.client_ip()) if admin_lib else False,
                },
            )
            return
        if parsed.path == "/api/auth/status":
            token = self.bearer_token()
            claims = license_auth.verify_token(token) if token and license_auth else None
            expires_at = ""
            role = ""
            if claims:
                role = str(claims.get("role") or "")
                if role == "admin":
                    expires_at = ""
                elif claims.get("exp"):
                    lic_id = str(claims.get("lic") or "")
                    lic = next((x for x in license_auth.load_licenses() if x.get("id") == lic_id), None)
                    expires_at = str(lic.get("expiresAt") or "") if lic else ""
                    if not expires_at:
                        expires_at = (
                            datetime.fromtimestamp(int(claims["exp"]), tz=timezone.utc)
                            .astimezone()
                            .isoformat(timespec="seconds")
                        )
            student_login = license_auth.student_login_enabled() if license_auth else False
            self.send_json(
                200,
                {
                    "ok": True,
                    "authRequired": self.auth_required() and not self.local_auth_bypass(),
                    "loggedIn": bool(claims),
                    "role": role,
                    "licenseLabel": claims.get("label", "") if claims else "",
                    "expiresAt": expires_at,
                    "permanent": role == "admin",
                    "studentLoginEnabled": student_login,
                },
            )
            return
        if parsed.path == "/api/admin/licenses":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            if self.ensure_admin_auth() is None:
                return
            qs = parse_qs(parsed.query)
            pin = self.admin_pin_from_request(qs)
            if not admin_lib.is_local_client_ip(self.client_ip()) and not admin_lib.verify_admin_pin(pin):
                self.send_json(403, {"error": "需要主机管理员密码"})
                return
            rows = license_auth.public_license_rows() if license_auth else []
            self.send_json(200, {"ok": True, "items": rows})
            return
        if parsed.path == "/api/study-hub/admin/config":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            cfg = admin_lib.load_admin_config()
            self.send_json(
                200,
                {
                    "ok": True,
                    "requireRemoteApproval": bool(cfg.get("requireRemoteApproval")),
                    "hasAdminPin": bool(cfg.get("adminPinHash")),
                    "isLocalClient": admin_lib.is_local_client_ip(self.client_ip()),
                },
            )
            return
        if parsed.path == "/api/study-hub/admin/pending":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            qs = parse_qs(parsed.query)
            pin = self.admin_pin_from_request(qs)
            if not admin_lib.is_local_client_ip(self.client_ip()) and not admin_lib.verify_admin_pin(pin):
                self.send_json(403, {"error": "需要主机管理员密码"})
                return
            self.send_json(200, {"ok": True, "items": admin_lib.list_pending_edits()})
            return
        if parsed.path == "/api/sync/logs":
            if self.ensure_license_auth() is None:
                return
            sync_id = safe_sync_id(parse_qs(parsed.query).get("syncId", [""])[0])
            if not sync_id:
                self.send_json(400, {"error": "missing syncId"})
                return
            logs = load_logs(sync_id)
            self.send_json(200, {"logs": logs[-20:]})
            return
        if parsed.path == "/api/sync":
            if self.ensure_license_auth() is None:
                return
            sync_id = safe_sync_id(parse_qs(parsed.query).get("syncId", [""])[0])
            if not sync_id:
                self.send_json(400, {"error": "missing syncId"})
                return
            data = load_sync_payload(sync_id)
            if not data:
                self.send_json(404, {"error": "not found"})
                return
            self.send_json(200, data)
            return
        if parsed.path == "/api/study-hub/refresh":
            try:
                run_study_hub_refresh()
                self.send_json(200, {"ok": True, "message": "已从 word-sources CSV 刷新讲读与精讲内容"})
            except subprocess.CalledProcessError as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/library-page":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            qs = parse_qs(parsed.query)
            kind = str(qs.get("kind", ["reading"])[0])
            if kind == "reading":
                unit = int(qs.get("unit", ["1"])[0])
                png = int(qs.get("png", ["0"])[0])
                scope = str(qs.get("scope", ["unit"])[0])
                body = hub_lib.read_reading_library(unit, png, scope=scope)
                printed = hub_lib.printed_page_for_png(png)
                self.send_json(200, {"ok": True, "exists": body is not None, "html": body or "", "printedPage": printed, "scope": scope})
                return
            if kind == "knowledge":
                page_id = str(qs.get("pageId", [""])[0]).strip()
                if not page_id:
                    self.send_json(400, {"error": "pageId required"})
                    return
                path = hub_lib.knowledge_library_path(page_id)
                body = hub_lib.read_library_html(path)
                self.send_json(200, {"ok": True, "exists": body is not None, "html": body or ""})
                return
            self.send_json(400, {"error": "invalid kind"})
            return
        if parsed.path == "/api/study-hub/list-snips":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            qs = parse_qs(parsed.query)
            unit_raw = qs.get("unit", [""])[0]
            page_id = str(qs.get("pageId", [""])[0]).strip() or None
            unit = int(unit_raw) if str(unit_raw).strip() else None
            try:
                items = hub_lib.list_snips(unit=unit, page_id=page_id)
                self.send_json(200, {"ok": True, "items": items})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/auth/login":
            if not license_auth:
                self.send_json(500, {"error": "license module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            username = str(body.get("username") or "").strip()
            password = str(body.get("password") or body.get("adminPassword") or "").strip()
            code = str(body.get("license") or body.get("code") or "").strip()
            try:
                if password and not code:
                    if not username:
                        username = license_auth.default_admin_user()
                    result = license_auth.login_with_password(username, password)
                elif code:
                    if not license_auth.student_login_enabled():
                        self.send_json(403, {"error": "学生授权码登录未开放，请联系管理员"})
                        return
                    result = license_auth.login_with_license(code)
                else:
                    self.send_json(400, {"error": "请输入管理员密码或授权码"})
                    return
                self.send_json(200, result)
            except ValueError as e:
                self.send_json(403, {"error": str(e)})
            return
        if parsed.path == "/api/admin/student-login":
            if not license_auth:
                self.send_json(500, {"error": "license module missing"})
                return
            if self.ensure_admin_auth() is None:
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            enabled = bool(body.get("enabled"))
            cfg = license_auth.set_student_login_enabled(enabled)
            self.send_json(200, {"ok": True, "studentLoginEnabled": cfg.get("studentLoginEnabled", False)})
            return
        if parsed.path == "/api/admin/licenses/generate":
            if not license_auth or not admin_lib:
                self.send_json(500, {"error": "module missing"})
                return
            if self.ensure_admin_auth() is None:
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            pin = str(body.get("adminPin") or self.headers.get("X-Admin-Pin") or "").strip()
            if not admin_lib.is_local_client_ip(self.client_ip()) and not admin_lib.verify_admin_pin(pin):
                self.send_json(403, {"error": "需要主机管理员密码"})
                return
            days = int(body.get("days") or 365)
            label = str(body.get("label") or "").strip()
            max_users = int(body.get("maxUsers") or 0)
            created = license_auth.create_license(days, label, max_users)
            self.send_json(200, {"ok": True, "license": created})
            return
        if parsed.path == "/api/sync/merge":
            if self.ensure_license_auth() is None:
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            sync_id = safe_sync_id(str(body.get("syncId", "")))
            payload = body.get("payload")
            if not sync_id or not isinstance(payload, dict):
                self.send_json(400, {"error": "syncId and payload required"})
                return
            device = str(body.get("device", "")).strip()
            result = merge_payload(sync_id, payload, device)
            self.send_json(200, result)
            return
        if parsed.path == "/api/sync":
            if self.ensure_license_auth() is None:
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            sync_id = safe_sync_id(str(body.get("syncId", "")))
            payload = body.get("payload")
            if not sync_id or not isinstance(payload, dict):
                self.send_json(400, {"error": "syncId and payload required"})
                return
            save_sync_payload(sync_id, payload)
            self.send_json(200, {"ok": True, "syncId": sync_id, "updatedAt": payload.get("updatedAt", "")})
            return
        if parsed.path == "/api/study-hub/refresh":
            try:
                run_study_hub_refresh()
                self.send_json(200, {"ok": True, "message": "已从 word-sources CSV 刷新讲读与精讲内容"})
            except subprocess.CalledProcessError as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/upload-word":
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            unit = int(body.get("unit") or 1)
            filename = str(body.get("filename") or "").strip()
            data_b64 = str(body.get("data") or "").strip()
            if not data_b64:
                self.send_json(400, {"error": "no file data"})
                return
            try:
                raw = base64.b64decode(data_b64)
            except Exception:
                self.send_json(400, {"error": "invalid base64"})
                return
            try:
                dest = save_uploaded_word(unit, filename, raw)
                run_study_hub_refresh()
                self.send_json(200, {"ok": True, "message": f"已导入 {dest.name} 并刷新", "path": str(dest)})
            except subprocess.CalledProcessError as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/fetch-url":
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            url = str(body.get("url", "")).strip()
            if not url.startswith(("http://", "https://")):
                self.send_json(400, {"error": "invalid url"})
                return
            req = urllib.request.Request(url, headers={"User-Agent": "StudyHub/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            text = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
            text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
            text = re.sub(r"<[^>]+>", "\n", text)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            paras = [f"<p>{line.strip()}</p>" for line in text.split("\n") if line.strip()][:80]
            self.send_json(200, {"ok": True, "bodyHtml": "\n".join(paras)})
            return
        if parsed.path == "/api/study-hub/save-page":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "请求 JSON 无法解析，请用 启动.bat 重启服务后重试"})
                return
            try:
                kind = str(body.get("kind", "reading"))
                content = str(body.get("html") or body.get("text") or "")
                admin_pin = str(body.get("adminPin") or self.headers.get("X-Admin-Pin") or "").strip()
                device = str(body.get("device") or "").strip()
                if kind == "reading":
                    result = self.queue_or_apply_save(
                        "reading",
                        content,
                        {
                            "unit": int(body.get("unit") or 1),
                            "png": int(body.get("png") or 0),
                            "scope": str(body.get("scope") or "unit"),
                        },
                        admin_pin=admin_pin,
                        device=device,
                    )
                elif kind == "knowledge":
                    result = self.queue_or_apply_save(
                        "knowledge",
                        content,
                        {"page_id": str(body.get("pageId") or "").strip()},
                        admin_pin=admin_pin,
                        device=device,
                    )
                else:
                    self.send_json(400, {"error": "invalid kind"})
                    return
                self.send_json(200, result)
            except ValueError as e:
                self.send_json(400, {"ok": False, "error": str(e)})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/save-page-raw":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            qs = parse_qs(parsed.query)
            kind = str(qs.get("kind", ["reading"])[0])
            admin_pin = self.admin_pin_from_request(qs)
            device = str(qs.get("device", [""])[0]).strip()
            try:
                content = self.read_raw_body()
                if kind == "reading":
                    result = self.queue_or_apply_save(
                        "reading",
                        content,
                        {
                            "unit": int(qs.get("unit", ["1"])[0]),
                            "png": int(qs.get("png", ["0"])[0]),
                            "scope": str(qs.get("scope", ["unit"])[0]),
                        },
                        admin_pin=admin_pin,
                        device=device,
                    )
                elif kind == "knowledge":
                    result = self.queue_or_apply_save(
                        "knowledge",
                        content,
                        {"page_id": str(qs.get("pageId", [""])[0]).strip()},
                        admin_pin=admin_pin,
                        device=device,
                    )
                else:
                    self.send_json(400, {"error": "invalid kind"})
                    return
                self.send_json(200, result)
            except ValueError as e:
                self.send_json(400, {"ok": False, "error": str(e)})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/import-csv":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            unit = int(body.get("unit") or 1)
            csv_text = str(body.get("csv") or body.get("text") or "").strip()
            admin_pin = str(body.get("adminPin") or self.headers.get("X-Admin-Pin") or "").strip()
            if not csv_text:
                self.send_json(400, {"error": "no csv data"})
                return
            try:
                if admin_lib and admin_lib.should_queue_edit(self.client_ip(), admin_pin):
                    entry = admin_lib.queue_pending_edit(
                        {
                            "kind": "import-csv",
                            "content": csv_text,
                            "meta": {"unit": unit},
                            "device": str(body.get("device") or ""),
                            "clientIp": self.client_ip(),
                            "summary": f"CSV 导入 Unit {unit}",
                        }
                    )
                    self.send_json(
                        200,
                        {
                            "ok": True,
                            "pending": True,
                            "pendingId": entry.get("id"),
                            "message": "CSV 已提交审核，批准后写入数据库",
                        },
                    )
                    return
                result = hub_lib.import_csv_to_library(csv_text, unit)
                self.send_json(200, result)
            except ValueError as e:
                self.send_json(400, {"ok": False, "error": str(e)})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/upload-media":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            name = str(body.get("filename") or "upload.bin")
            b64 = str(body.get("data") or "")
            if not b64:
                self.send_json(400, {"error": "no data"})
                return
            try:
                raw = base64.b64decode(b64)
            except Exception:
                self.send_json(400, {"error": "invalid base64"})
                return
            if len(raw) > 12 * 1024 * 1024:
                self.send_json(400, {"error": "file too large (max 12MB)"})
                return
            try:
                path = hub_lib.save_media_file(name, raw)
                rel = str(path.relative_to(ROOT)).replace("\\", "/")
                self.send_json(200, {"ok": True, "url": f"/{rel}", "path": rel})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/save-student-audio":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            name = str(body.get("filename") or "recording.mp3")
            b64 = str(body.get("data") or "")
            if not b64:
                self.send_json(400, {"error": "no data"})
                return
            try:
                raw = base64.b64decode(b64)
            except Exception:
                self.send_json(400, {"error": "invalid base64"})
                return
            if len(raw) > 24 * 1024 * 1024:
                self.send_json(400, {"error": "file too large (max 24MB)"})
                return
            try:
                path = hub_lib.save_student_audio(name, raw)
                rel = str(path.relative_to(ROOT)).replace("\\", "/")
                self.send_json(200, {"ok": True, "url": f"/{rel}", "path": rel})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/save-snip":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            unit = int(body.get("unit") or 1)
            category = str(body.get("category") or "task").strip()
            if category not in ("task", "homework"):
                self.send_json(400, {"error": "category must be task or homework"})
                return
            name = str(body.get("filename") or "snip.png")
            b64 = str(body.get("data") or "")
            page_id = str(body.get("pageId") or "").strip()
            part = str(body.get("part") or "").strip()
            if not page_id:
                self.send_json(400, {"error": "pageId required"})
                return
            if not b64:
                self.send_json(400, {"error": "no data"})
                return
            try:
                raw = base64.b64decode(b64)
            except Exception:
                self.send_json(400, {"error": "invalid base64"})
                return
            if len(raw) > 12 * 1024 * 1024:
                self.send_json(400, {"error": "file too large (max 12MB)"})
                return
            if hub_lib.count_snips(unit, page_id, category) >= 4:
                label = "作业布置" if category == "task" else "作业提交"
                self.send_json(400, {"error": f"本 Part 的{label}已满（最多 4 张）"})
                return
            try:
                entry = hub_lib.save_snip_image(unit, category, name, raw, page_id, part)
                rel = str(entry.get("path", "")).replace("\\", "/")
                self.send_json(200, {"ok": True, "item": entry, "url": f"/{rel}", "path": rel})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/delete-snip":
            if not hub_lib:
                self.send_json(500, {"error": "library module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            snip_id = str(body.get("id") or "").strip()
            if not snip_id:
                self.send_json(400, {"error": "id required"})
                return
            try:
                ok = hub_lib.delete_snip(snip_id)
                if not ok:
                    self.send_json(404, {"ok": False, "error": "not found"})
                    return
                self.send_json(200, {"ok": True})
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
            return
        if parsed.path == "/api/study-hub/admin/setup":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            pin = str(body.get("adminPin") or "").strip()
            if len(pin) < 4:
                self.send_json(400, {"error": "管理员密码至少 4 位"})
                return
            cfg = admin_lib.load_admin_config()
            if cfg.get("adminPinHash") and not admin_lib.is_local_client_ip(self.client_ip()):
                old = str(body.get("currentAdminPin") or "").strip()
                if not admin_lib.verify_admin_pin(old):
                    self.send_json(403, {"error": "当前管理员密码错误"})
                    return
            saved = admin_lib.setup_admin_pin(pin, bool(body.get("requireRemoteApproval", True)))
            self.send_json(200, {"ok": True, "requireRemoteApproval": saved.get("requireRemoteApproval")})
            return
        if parsed.path == "/api/study-hub/admin/approve":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            pin = str(body.get("adminPin") or self.headers.get("X-Admin-Pin") or "").strip()
            if not admin_lib.verify_admin_pin(pin):
                self.send_json(403, {"error": "管理员密码错误"})
                return
            edit_id = str(body.get("id") or "").strip()
            entry = admin_lib.get_pending_edit(edit_id)
            if not entry or entry.get("status") != "pending":
                self.send_json(404, {"error": "待审核项不存在"})
                return
            result = self.apply_pending_edit(entry)
            admin_lib.mark_pending_edit(edit_id, "approved")
            self.send_json(200, {"ok": True, "result": result})
            return
        if parsed.path == "/api/study-hub/admin/reject":
            if not admin_lib:
                self.send_json(500, {"error": "admin module missing"})
                return
            try:
                body = self.read_json_body()
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return
            pin = str(body.get("adminPin") or self.headers.get("X-Admin-Pin") or "").strip()
            if not admin_lib.verify_admin_pin(pin):
                self.send_json(403, {"error": "管理员密码错误"})
                return
            edit_id = str(body.get("id") or "").strip()
            if not admin_lib.mark_pending_edit(edit_id, "rejected"):
                self.send_json(404, {"error": "待审核项不存在"})
                return
            self.send_json(200, {"ok": True})
            return
        self.send_error(404)


def main() -> None:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), LanHandler)
    print(f"[LAN] Static + sync server: http://0.0.0.0:{PORT}")
    print(f"[LAN] Study Hub API v3 (save-page / import-csv / library / upload-media)")
    print(f"[LAN] Sync folder: {SYNC_DIR}")
    if license_auth and license_auth.auth_enabled():
        print("[LAN] License auth: ENABLED (encrypted sync storage)")
    else:
        print("[LAN] License auth: disabled (set PEP6_AUTH_REQUIRED=1 on ECS)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[LAN] Server stopped.")


if __name__ == "__main__":
    main()
