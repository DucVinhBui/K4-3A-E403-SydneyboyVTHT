#!/usr/bin/env bash
# Dựng demo-slides.pdf từ slides/demo-slides.html bằng Chrome headless.
# Chạy từ gốc repo:  bash slides/build.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

[ -x "$CHROME" ] || { echo "Không tìm thấy Google Chrome ở $CHROME" >&2; exit 1; }

"$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="$ROOT/demo-slides.pdf" \
  "file://$ROOT/slides/demo-slides.html" 2>/dev/null

echo "→ $ROOT/demo-slides.pdf"
