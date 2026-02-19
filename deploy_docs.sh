#!/usr/bin/env bash
# Build the marketing+docs site with Astro and deploy to sites/assets/ifitwala_doc
# Usage: ./deploy_docs.sh
# Env overrides:
#   APP_ROOT=/home/.../apps/ifitwala_doc
#   DEST_ROOT=/home/.../sites/assets/ifitwala_doc

set -Eeuo pipefail

APP_ROOT="${APP_ROOT:-$HOME/frappe-bench/apps/ifitwala_doc}"
DEST_ROOT="${DEST_ROOT:-$HOME/frappe-bench/sites/assets/ifitwala_doc}"
SRC_ROOT="${SRC_ROOT:-$APP_ROOT/dist}"

echo "==> App root:    $APP_ROOT"
echo "==> Dest root:   $DEST_ROOT"
echo "==> Build output: $SRC_ROOT"
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

echo
echo "✅ Deployed:"
echo "   - dist  -> $DEST_ROOT"
