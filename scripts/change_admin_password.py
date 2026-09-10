#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Change PEP6 admin password (login + study-hub remote approval)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import license_auth  # noqa: E402

try:
    import study_hub_admin as admin_lib
except ImportError:
    admin_lib = None


def main() -> int:
    parser = argparse.ArgumentParser(description="Change PEP6 admin password")
    parser.add_argument("password", nargs="?", default="", help="New admin password")
    parser.add_argument("--from-env", action="store_true", help="Use PEP6_ADMIN_PIN from environment")
    parser.add_argument("--user", type=str, default="", help="Admin username (default from env)")
    args = parser.parse_args()

    password = str(args.password or "").strip()
    if args.from_env:
        password = license_auth.default_admin_password()
    if not password:
        print("请提供新密码，例如:")
        print("  python3 scripts/change_admin_password.py '你的新密码'")
        print("或先改 /etc/pep6-english/env 里的 PEP6_ADMIN_PIN，再执行:")
        print("  source /etc/pep6-english/env && python3 scripts/change_admin_password.py --from-env")
        return 1

    username = (args.user or license_auth.default_admin_user()).strip()
    license_auth.update_admin_password(password, username)

    if admin_lib:
        cfg = admin_lib.load_admin_config()
        admin_lib.setup_admin_pin(password, bool(cfg.get("requireRemoteApproval", True)))

    print("管理员密码已更新。")
    print(f"用户名（服务器内部）: {username}")
    print("网页登录：在「管理员密码」框输入新密码即可。")
    print("侧边栏「远程密码控制」也使用同一密码。")
    print("建议执行: sudo systemctl restart pep6-english")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
