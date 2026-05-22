#!/usr/bin/env bash
# Build the marketing+docs site with Astro and deploy to sites/assets/ifitwala_doc
# Usage:
#   ./deploy_docs.sh
#   ./deploy_docs.sh --with-nginx   # refresh Nginx static routes after route/config changes
#   ./deploy_docs.sh --auto-nginx   # refresh only if route config is missing/stale
#   ./deploy_docs.sh --no-nginx     # explicit content-only deploy
#
# Env overrides:
#   APP_ROOT=/home/.../apps/ifitwala_doc
#   DEST_ROOT=/home/.../sites/assets/ifitwala_doc
#   BENCH_ROOT=/home/.../frappe-bench
#   OUT_CONF=/etc/nginx/conf.d/ifitwala_doc_static.inc
#   INSTALL_NGINX=0|1|auto

set -Eeuo pipefail

APP_ROOT="${APP_ROOT:-$HOME/frappe-bench/apps/ifitwala_doc}"
DEST_ROOT="${DEST_ROOT:-$HOME/frappe-bench/sites/assets/ifitwala_doc}"
SRC_ROOT="${SRC_ROOT:-$APP_ROOT/dist}"
BENCH_ROOT="${BENCH_ROOT:-$(cd "$APP_ROOT/../.." && pwd)}"
OUT_CONF="${OUT_CONF:-/etc/nginx/conf.d/ifitwala_doc_static.inc}"
INSTALL_NGINX="${INSTALL_NGINX:-0}"

usage() {
  sed -n '1,16p' "$0" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-nginx|--install-nginx)
      INSTALL_NGINX=1
      shift
      ;;
    --auto-nginx)
      INSTALL_NGINX=auto
      shift
      ;;
    --no-nginx)
      INSTALL_NGINX=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

echo "==> App root:    $APP_ROOT"
echo "==> Dest root:   $DEST_ROOT"
echo "==> Build output: $SRC_ROOT"
echo "==> Nginx routes: $INSTALL_NGINX ($OUT_CONF)"
echo

# 1) Build (yarn only)
cd "$APP_ROOT"

if [[ -f ".env" ]]; then
  set -a
  source ".env"
  set +a
fi

API_BASE="${PUBLIC_SITE_API:-${SITE_API_BASE:-${PUBLIC_DOCS_API:-${DOCS_API_BASE:-<unset>}}}}"
echo "==> Content API base: $API_BASE"
echo "==> Installing deps (yarn)…"
yarn install --frozen-lockfile --check-files

echo "==> Cleaning previous build outputs…"
yarn clean

echo "==> Building with Astro…"
yarn build:marketing
yarn build:docs

# 2) Deploy (rsync entire dist/)
DIST_SRC="$SRC_ROOT"

if [[ ! -d "$DIST_SRC" ]]; then
  echo "ERROR: $DIST_SRC not found. Did the build succeed?" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"

echo "==> Rsync dist/ -> $DEST_ROOT/"
rsync -a --delete "$DIST_SRC/" "$DEST_ROOT/"

should_install_nginx=0
case "$INSTALL_NGINX" in
  1|true|yes)
    should_install_nginx=1
    ;;
  0|false|no)
    should_install_nginx=0
    ;;
  auto)
    if [[ ! -f "$OUT_CONF" ]]; then
      should_install_nginx=1
      echo "==> Nginx static route config is missing; will install it."
    elif [[ "$APP_ROOT/install_ifitwala_nginx.sh" -nt "$OUT_CONF" ]]; then
      should_install_nginx=1
      echo "==> Nginx static route script changed; will refresh the config."
    fi
    ;;
  *)
    echo "ERROR: INSTALL_NGINX must be auto, 1, or 0; got '$INSTALL_NGINX'" >&2
    exit 1
    ;;
esac

if [[ "$should_install_nginx" == "1" ]]; then
  echo "==> Installing/reloading Nginx static routes..."
  BENCH_ROOT="$BENCH_ROOT" \
    ASSETS_ROOT="$DEST_ROOT" \
    OUT_CONF="$OUT_CONF" \
    STRICT_INCLUDE=1 \
    "$APP_ROOT/install_ifitwala_nginx.sh"
else
  echo "==> Nginx static routes unchanged."
  echo "    Use ./deploy_docs.sh --with-nginx after route/config changes."
fi

echo
echo "✅ Deployed:"
echo "   - dist  -> $DEST_ROOT"
if [[ "$should_install_nginx" == "1" ]]; then
  echo "   - nginx -> $OUT_CONF"
fi
