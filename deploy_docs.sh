#!/usr/bin/env bash
# Build with Astro (yarn) and deploy static files to sites/assets/ifitwala_doc
# Usage: ./scripts/deploy_docs.sh
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
echo "==> Installing deps (yarn)…"
cd "$APP_ROOT"
yarn install --frozen-lockfile --check-files

echo "==> Building with Astro…"
yarn astro:build

# 2) Deploy (rsync docs/ and _astro/)
DOCS_SRC="$SRC_ROOT/docs"
ASTRO_SRC="$SRC_ROOT/_astro"

if [[ ! -d "$DOCS_SRC" ]]; then
  echo "ERROR: $DOCS_SRC not found. Did the build succeed?" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT/docs" "$DEST_ROOT/_astro"

echo "==> Rsync pages -> $DEST_ROOT/docs/"
rsync -a --delete "$DOCS_SRC/" "$DEST_ROOT/docs/"

if [[ -d "$ASTRO_SRC" ]]; then
  echo "==> Rsync assets -> $DEST_ROOT/_astro/"
  rsync -a --delete "$ASTRO_SRC/" "$DEST_ROOT/_astro/"
else
  echo "WARN: $ASTRO_SRC missing; skipping hashed assets"
fi

echo
echo "✅ Deployed:"
echo "   - docs  -> $DEST_ROOT/docs"
echo "   - _astro-> $DEST_ROOT/_astro"
