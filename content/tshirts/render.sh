#!/bin/bash
# Render every src/NN-*.html to PNG (2x) using N worker lanes.
# Each lane reuses ONE dedicated temp profile over its shard: isolated from the
# user's browser (no singleton hang), warm profile (no repeated cold start),
# and parallel across lanes. Optional arg = glob of files to render.
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
shopt -s nullglob
LANES=6

mapfile_compat() { files=( $1 ); }
PATTERN="${1:-src/[0-9]*.html}"
files=( $PATTERN )

lane() {
  local lane_id="$1"; shift
  local prof; prof=$(mktemp -d /tmp/cfdlchrome.XXXXXX)
  local i=0 f base pid killer
  for f in "$@"; do
    base=$(basename "$f" .html)
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
      --no-first-run --no-default-browser-check --disable-extensions \
      --disable-background-networking --disable-component-update --disable-sync \
      --disable-default-apps --metrics-recording-only --disable-client-side-phishing-detection \
      --disable-features=Translate,OptimizationHints,MediaRouter \
      --user-data-dir="$prof" \
      --force-device-scale-factor=2 --window-size=1200,800 \
      --screenshot="$PWD/$base.png" "file://$PWD/$f" >/dev/null 2>&1 &
    pid=$!
    ( sleep 14; kill -9 $pid 2>/dev/null ) >/dev/null 2>&1 &
    killer=$!
    wait $pid 2>/dev/null
    kill -9 $killer 2>/dev/null
  done
  rm -rf "$prof"
}

# shard files across lanes (round-robin) and launch lanes in parallel
for ((L=0; L<LANES; L++)); do
  shard=()
  for ((i=L; i<${#files[@]}; i+=LANES)); do shard+=("${files[$i]}"); done
  lane "$L" "${shard[@]}" &
done
wait
echo "RENDER_DONE $(ls [0-9]*.png 2>/dev/null | wc -l)"
