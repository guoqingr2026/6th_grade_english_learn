#!/usr/bin/env bash
# Run on Aliyun ECS (Ubuntu/Debian) as root or with sudo.
set -euo pipefail

APP_DIR="/opt/pep6-english"
ENV_DIR="/etc/pep6-english"
REPO_URL="${REPO_URL:-https://github.com/guoqingr2026/6th_grade_english_learn.git}"

echo "[1/7] Install packages"
apt-get update
apt-get install -y git python3 python3-pip nginx

echo "[2/7] Clone or update app"
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$APP_DIR"
fi

echo "[3/7] Python dependencies"
pip3 install -r "$APP_DIR/requirements-server.txt"

echo "[4/7] Environment"
mkdir -p "$ENV_DIR" "$APP_DIR/data/auth" "$APP_DIR/lan-sync"
if [ ! -f "$ENV_DIR/env" ]; then
  cp "$APP_DIR/deploy/ecs/env.example" "$ENV_DIR/env"
  echo "Edit $ENV_DIR/env if needed"
fi
chown -R www-data:www-data "$APP_DIR/data" "$APP_DIR/lan-sync"

echo "[5/7] systemd"
cp "$APP_DIR/deploy/ecs/pep6-english.service" /etc/systemd/system/pep6-english.service
systemctl daemon-reload
systemctl enable pep6-english
systemctl restart pep6-english

echo "[6/7] nginx"
cp "$APP_DIR/deploy/ecs/nginx.conf" /etc/nginx/sites-available/pep6-english
ln -sf /etc/nginx/sites-available/pep6-english /etc/nginx/sites-enabled/pep6-english
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "[7/7] Generate first license (optional)"
echo "  cd $APP_DIR && python3 scripts/gen_license.py --days 365 --label 班级授权"
echo "Done. Open http://YOUR_ECS_IP/ and enter the license code."
