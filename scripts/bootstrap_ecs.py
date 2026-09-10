#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""First-run bootstrap for ECS: default admin user + study-hub admin PIN."""

from __future__ import annotations

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
    admin_user = license_auth.bootstrap_admin_user()
    admin_pin = license_auth.default_admin_password()

    if admin_lib:
        cfg = admin_lib.load_admin_config()
        if not cfg.get("adminPinHash"):
            admin_lib.setup_admin_pin(admin_pin, bool(cfg.get("requireRemoteApproval", True)))

    print("=== ECS 初始化完成 ===")
    print(f"管理员用户名: {admin_user.get('username', 'admin')}")
    print(f"管理员密码: {admin_pin}")
    print("（网页登录可用用户名+密码；侧边栏「远程密码控制」也用此密码）")
    print("学生请使用 PEP6 授权码登录，可用 scripts/gen_license.py 生成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
