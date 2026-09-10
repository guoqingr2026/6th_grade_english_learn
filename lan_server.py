#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static file server + LAN sync API (last-write-wins merge + logs)."""

from __future__ import annotations

import base64
import json
import re
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
    client_ts = parse_ts(str(client_payload.get("updatedAt", "")))
    client_device = device or "未知设备"
    file_path = data_path(sync_id)

    if not file_path.exists():
        file_path.write_text(json.dumps(client_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        entry = make_log(
            "initialized",
            client_device,
            "首次同步，已建立班级数据副本",
            str(client_payload.get("updatedAt", "")),
        )
        recent = append_log(sync_id, entry)
        return {"action": "initialized", "payload": client_payload, "log": entry, "logs": recent}

    server_payload = json.loads(file_path.read_text(encoding="utf-8"))
    server_ts = parse_ts(str(server_payload.get("updatedAt", "")))

    if client_ts > server_ts:
        file_path.write_text(json.dumps(client_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        entry = make_log(
            "local_wins",
            client_device,
            "本机数据较新，已更新班级副本（其他端点同步即可获取）",
            str(client_payload.get("updatedAt", "")),
        )
        recent = append_log(sync_id, entry)
        return {"action": "local_wins", "payload": client_payload, "log": entry, "logs": recent}

    if server_ts > client_ts:
        entry = make_log(
            "remote_wins",
            client_device,
            "班级数据较新，已下发到本机",
            str(server_payload.get("updatedAt", "")),
        )
        recent = append_log(sync_id, entry)
        return {"action": "remote_wins", "payload": server_payload, "log": entry, "logs": recent}

    entry = make_log(
        "same",
        client_device,
        "两端数据时间一致，无需变更",
        str(server_payload.get("updatedAt", "")),
    )
    recent = append_log(sync_id, entry)
    return {"action": "same", "payload": server_payload, "log": entry, "logs": recent}


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

    def handle_save_page(self, kind: str, content: str, unit: int = 1, png: int = 0, page_id: str = "") -> dict:
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
            path = hub_lib.save_reading_page(unit, png, content)
            csv_path = hub_lib.unit_csv_path(unit)
            return {
                "ok": True,
                "path": str(path.relative_to(ROOT)),
                "printedPage": hub_lib.printed_page_for_png(png),
                "csvSynced": csv_path.exists(),
                "csvPath": str(csv_path.relative_to(ROOT)) if csv_path.exists() else "",
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
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/ping":
            self.send_json(
                200,
                {
                    "ok": True,
                    "service": "lan-sync",
                    "studyHubApi": 3,
                    "features": ["save-page", "save-page-raw", "import-csv", "library-page", "upload-media"],
                },
            )
            return
        if parsed.path == "/api/sync/logs":
            sync_id = safe_sync_id(parse_qs(parsed.query).get("syncId", [""])[0])
            if not sync_id:
                self.send_json(400, {"error": "missing syncId"})
                return
            logs = load_logs(sync_id)
            self.send_json(200, {"logs": logs[-20:]})
            return
        if parsed.path == "/api/sync":
            sync_id = safe_sync_id(parse_qs(parsed.query).get("syncId", [""])[0])
            if not sync_id:
                self.send_json(400, {"error": "missing syncId"})
                return
            file_path = data_path(sync_id)
            if not file_path.exists():
                self.send_json(404, {"error": "not found"})
                return
            data = json.loads(file_path.read_text(encoding="utf-8"))
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
                path = hub_lib.reading_library_path(unit, png)
                body = hub_lib.read_library_html(path)
                printed = hub_lib.printed_page_for_png(png)
                self.send_json(200, {"ok": True, "exists": body is not None, "html": body or "", "printedPage": printed})
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
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/sync/merge":
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
            SYNC_DIR.mkdir(parents=True, exist_ok=True)
            data_path(sync_id).write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
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
                if kind == "reading":
                    result = self.handle_save_page(
                        "reading", content, unit=int(body.get("unit") or 1), png=int(body.get("png") or 0)
                    )
                elif kind == "knowledge":
                    result = self.handle_save_page(
                        "knowledge", content, page_id=str(body.get("pageId") or "").strip()
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
            try:
                content = self.read_raw_body()
                if kind == "reading":
                    result = self.handle_save_page(
                        "reading",
                        content,
                        unit=int(qs.get("unit", ["1"])[0]),
                        png=int(qs.get("png", ["0"])[0]),
                    )
                elif kind == "knowledge":
                    result = self.handle_save_page(
                        "knowledge", content, page_id=str(qs.get("pageId", [""])[0]).strip()
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
            if not csv_text:
                self.send_json(400, {"error": "no csv data"})
                return
            try:
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
        self.send_error(404)


def main() -> None:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), LanHandler)
    print(f"[LAN] Static + sync server: http://0.0.0.0:{PORT}")
    print(f"[LAN] Study Hub API v3 (save-page / import-csv / library / upload-media)")
    print(f"[LAN] Sync folder: {SYNC_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[LAN] Server stopped.")


if __name__ == "__main__":
    main()
