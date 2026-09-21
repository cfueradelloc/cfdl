#!/bin/bash
# Renderiza cada src/<id>-NN.html a out/<id>-NN.png con Chrome sin cabeza.
#
# Cada carril reutiliza UN perfil temporal propio sobre su lote: aislado del
# navegador del usuario (sin bloqueo de instancia única), caliente (sin arranque
# en frío repetido) y en paralelo entre carriles. Es la parte del script de
# camisetas que hace que Chrome sin cabeza en paralelo no se cuelgue.
#
#   bash render.sh                 todo
#   bash render.sh 'src/2025-*'    sólo lo que case
#   SCALE=2 bash render.sh         maestro 2160×2700 (Instagram recorta a 1080)
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
shopt -s nullglob
LANES=4                  # menos que en camisetas: estas páginas pesan más
SCALE="${SCALE:-1}"      # 1 → PNG exacto de 1080×1350, el tamaño nativo del feed
mkdir -p out

PATTERN="${1:-src/*-[0-9][0-9].html}"
files=( $PATTERN )
if [ ${#files[@]} -eq 0 ]; then echo "nada que renderizar en $PATTERN"; exit 0; fi

lane() {
  local prof; prof=$(mktemp -d /tmp/cfdligchrome.XXXXXX)
  local f base pid killer
  for f in "$@"; do
    base=$(basename "$f" .html)
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
      --no-first-run --no-default-browser-check --disable-extensions \
      --disable-background-networking --disable-component-update --disable-sync \
      --disable-default-apps --metrics-recording-only \
      --disable-client-side-phishing-detection \
      --disable-features=Translate,OptimizationHints,MediaRouter \
      --user-data-dir="$prof" \
      --force-device-scale-factor="$SCALE" --window-size=1080,1350 \
      --virtual-time-budget=3000 --run-all-compositor-stages-before-draw \
      --screenshot="$PWD/out/$base.png" "file://$PWD/$f" >/dev/null 2>&1 &
    pid=$!
    ( sleep 20; kill -9 $pid 2>/dev/null ) >/dev/null 2>&1 &
    killer=$!
    wait $pid 2>/dev/null
    kill -9 $killer 2>/dev/null
  done
  rm -rf "$prof"
}

for ((L=0; L<LANES; L++)); do
  shard=()
  for ((i=L; i<${#files[@]}; i+=LANES)); do shard+=("${files[$i]}"); done
  [ ${#shard[@]} -gt 0 ] && lane "${shard[@]}" &
done
wait
echo "RENDER_DONE $(ls out/*.png 2>/dev/null | wc -l | tr -d ' ')"
