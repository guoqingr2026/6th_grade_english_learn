#!/usr/bin/env python3
"""Build release manifest, diff against previous version, update VERSION_HISTORY."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"
MANIFEST_DIR = ROOT / "manifests"
HISTORY_FILE = ROOT / "docs" / "VERSION_HISTORY.md"

TRACKED_GLOBS = [
    "index.html",
    "app.js",
    "study-hub.js",
    "styles.css",
    "mastery.js",
    "CHANGELOG.md",
    "VERSION",
    "启动.bat",
    "sync-release.bat",
    "发布打包.bat",
    "scripts/*.py",
    "data/study-hub/*.json",
    ".github/**/*",
]

SKIP_PARTS = {
    "data/study-hub/library",
    "data/study-hub/snip-index.json",
}


def read_version() -> str:
    if not VERSION_FILE.exists():
        return "1.0.0"
    text = VERSION_FILE.read_text(encoding="utf-8").strip()
    return text.splitlines()[0].strip() or "1.0.0"


def write_version(version: str) -> None:
    VERSION_FILE.write_text(f"{version}\n", encoding="utf-8")


def bump_version(version: str, kind: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
    if not m:
        raise ValueError(f"invalid version: {version}")
    major, minor, patch = map(int, m.groups())
    if kind == "major":
        major += 1
        minor = 0
        patch = 0
    elif kind == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def should_skip(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    for part in SKIP_PARTS:
        if rel.startswith(part):
            return True
    return False


def collect_tracked_files() -> list[Path]:
    found: set[Path] = set()
    for pattern in TRACKED_GLOBS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if should_skip(rel):
                continue
            found.add(path)
    return sorted(found, key=lambda p: str(p).lower())


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(version: str) -> dict:
    files: dict[str, dict] = {}
    for path in collect_tracked_files():
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        stat = path.stat()
        files[rel] = {
            "sha256": file_sha256(path),
            "size": stat.st_size,
        }
    tz = timezone(timedelta(hours=8))
    return {
        "version": version,
        "generatedAt": datetime.now(tz).isoformat(timespec="seconds"),
        "fileCount": len(files),
        "files": files,
    }


def load_previous_manifest() -> dict | None:
    latest = MANIFEST_DIR / "latest.json"
    if not latest.exists():
        return None
    try:
        return json.loads(latest.read_text(encoding="utf-8"))
    except Exception:
        return None


def diff_manifests(prev: dict | None, curr: dict) -> dict:
    prev_files = (prev or {}).get("files") or {}
    curr_files = curr.get("files") or {}
    added = sorted(set(curr_files) - set(prev_files))
    removed = sorted(set(prev_files) - set(curr_files))
    changed = sorted(
        rel
        for rel in set(prev_files) & set(curr_files)
        if prev_files[rel].get("sha256") != curr_files[rel].get("sha256")
    )
    unchanged = sorted(
        rel
        for rel in set(prev_files) & set(curr_files)
        if prev_files[rel].get("sha256") == curr_files[rel].get("sha256")
    )
    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
    }


def ensure_history_header() -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if HISTORY_FILE.exists():
        return
    HISTORY_FILE.write_text(
        "# 版本文件差异记录\n\n"
        "由 `scripts/release_pack.py` 在每次执行 `发布打包.bat` 时自动生成。\n"
        "记录相对上一版 manifest 的新增、删除与内容变更文件（SHA256）。\n\n"
        "---\n\n",
        encoding="utf-8",
    )


def append_history(version: str, diff: dict, prev_version: str | None) -> None:
    ensure_history_header()
    tz = timezone(timedelta(hours=8))
    stamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    lines = [
        f"## v{version} — {stamp}\n",
        f"- 上一版本：{prev_version or '（首次建档）'}",
        f"- 新增 {len(diff['added'])} · 删除 {len(diff['removed'])} · 变更 {len(diff['changed'])} · 未变 {len(diff['unchanged'])}\n",
    ]
    if diff["added"]:
        lines.append("### 新增")
        lines.extend(f"- `{p}`" for p in diff["added"])
        lines.append("")
    if diff["removed"]:
        lines.append("### 删除")
        lines.extend(f"- `{p}`" for p in diff["removed"])
        lines.append("")
    if diff["changed"]:
        lines.append("### 变更")
        lines.extend(f"- `{p}`" for p in diff["changed"])
        lines.append("")
    lines.append("---\n")
    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def save_manifest(manifest: dict) -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    version = manifest["version"]
    version_path = MANIFEST_DIR / f"v{version}.json"
    latest_path = MANIFEST_DIR / "latest.json"
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    version_path.write_text(text, encoding="utf-8")
    latest_path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Release pack manifest + diff")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="bump VERSION before pack")
    args = parser.parse_args()

    version = read_version()
    if args.bump:
        version = bump_version(version, args.bump)
        write_version(version)
        print(f"[版本] 已递增为 {version}")

    prev = load_previous_manifest()
    prev_version = prev.get("version") if prev else None
    manifest = build_manifest(version)
    diff = diff_manifests(prev, manifest)
    save_manifest(manifest)
    append_history(version, diff, prev_version)

    print(f"[完成] v{version} · 跟踪 {manifest['fileCount']} 个文件")
    print(f"  新增 {len(diff['added'])} · 删除 {len(diff['removed'])} · 变更 {len(diff['changed'])}")
    print(f"  manifest: manifests/v{version}.json")
    print(f"  差异记录: docs/VERSION_HISTORY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
