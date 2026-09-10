#!/usr/bin/env bash
# Run on Aliyun ECS (Ubuntu/Debian) as root or with sudo.
set -euo pipefail

APP_DIR="/opt/pep6-english"
ENV_DIR="/etc/pep6-english"
REPO_URL="${REPO_URL:-https://github.com/guoqingr2026/6th_grade_english_learn.git}"

echo "[1/8] Install packages"
apt-get update
apt-get install -y git python3 python3-pip nginx

echo "[2/8] Clone or update app"
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$APP_DIR"
fi

echo "[3/8] Python dependencies"
pip3 install -r "$APP_DIR/requirements-server.txt"

echo "[4/8] Environment"
mkdir -p "$ENV_DIR" "$APP_DIR/data/auth" "$APP_DIR/lan-sync"
if [ ! -f "$ENV_DIR/env" ]; then
  cp "$APP_DIR/deploy/ecs/env.example" "$ENV_DIR/env"
  echo "Edit $ENV_DIR/env if needed"
fi
chown -R www-data:www-data "$APP_DIR/data" "$APP_DIR/lan-sync"

set -a
# shellcheck disable=SC1090
source "$ENV_DIR/env"
set +a

if [ -n "${PEP6_WEB_PATH:-}" ] && [ "${PEP6_WEB_PATH}" != "/" ]; then
  echo "[5/8] Subpath: ${PEP6_WEB_PATH}"
  python3 "$APP_DIR/scripts/set_web_path.py" "${PEP6_WEB_PATH}"
else
  echo "[5/8] Web path: / (root)"
  python3 "$APP_DIR/scripts/set_web_path.py" ""
fi

echo "[6/8] Bootstrap default admin (admin / admin@123)"
python3 "$APP_DIR/scripts/bootstrap_ecs.py"
chown -R www-data:www-data "$APP_DIR/data" "$APP_DIR/lan-sync"

echo "[7/8] systemd"
cp "$APP_DIR/deploy/ecs/pep6-english.service" /etc/systemd/system/pep6-english.service
systemctl daemon-reload
systemctl enable pep6-english
systemctl restart pep6-english

echo "[8/8] nginx"
mkdir -p /etc/nginx/snippets
SNIP_DST="/etc/nginx/snippets/pep6-english-location.conf"
if [ "${PEP6_NGINX_MODE:-root}" = "subpath" ] && [ -n "${PEP6_WEB_PATH:-}" ]; then
  sed "s|__WEB_PATH__|${PEP6_WEB_PATH}|g" "$APP_DIR/deploy/ecs/nginx-subpath.snippet" > "$SNIP_DST"
  echo "Subpath nginx snippet written to $SNIP_DST"
  echo "Add this line inside your EXISTING site server { } block:"
  echo "  include $SNIP_DST;"
  echo "Then run: nginx -t && systemctl reload nginx"
  echo "Access URL: http://YOUR_ECS_IP${PEP6_WEB_PATH}/"
else
  cp "$APP_DIR/deploy/ecs/nginx.conf" /etc/nginx/sites-available/pep6-english
  ln -sf /etc/nginx/sites-available/pep6-english /etc/nginx/sites-enabled/pep6-english
  rm -f /etc/nginx/sites-enabled/default
  nginx -t
  systemctl reload nginx
  echo "Done. Open http://YOUR_ECS_IP/ and enter the license code."
fi

echo "Optional license: cd $APP_DIR && python3 scripts/gen_license.py --days 365 --label 班级授权"
