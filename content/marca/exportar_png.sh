#!/bin/bash
# Exporta los SVG principales a PNG en los tamaños que hacen falta de verdad.
# El SVG es el maestro; esto es sólo conveniencia para subir una foto de perfil
# o dejar un favicon.
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p png
# archivo-svg  tamaño  nombre-png
LISTA=(
  "cfdl-monograma-duo-ambar-negro     1080 perfil-instagram"
  "cfdl-monograma-duo-ambar-negro      512 monograma-512"
  "cfdl-monograma-plano-ambar-negro    180 favicon-180"
  "cfdl-monograma-plano-ambar-negro     32 favicon-32"
  "cfdl-monograma-duo-ninguno-negro    512 monograma-sin-campo"
  "cfdl-lockup-duo-ambar-negro        1080 lockup-1080"
  "cfdl-linea-duo-ninguno-negro        400 linea-400"
)
for fila in "${LISTA[@]}"; do
  set -- $fila
  svg="svg/$1.svg"; size=$2; nom=$3
  [ -f "$svg" ] || { echo "falta $svg"; continue; }
  # ancho proporcional: la línea es 3.4:1, las demás cuadradas
  W=$size; case "$1" in *linea*) W=$((size*34/10));; esac
  cat > /tmp/cfdlmarca.html <<EOF
<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:'FuturaStd';src:url('$PWD/../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}
html,body{margin:0;padding:0;width:${W}px;height:${size}px;background:transparent}
img,svg{display:block;width:${W}px;height:${size}px}
</style>$(cat "$svg")
EOF
  prof=$(mktemp -d /tmp/cfdlmarca.XXXXXX)
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run \
    --user-data-dir="$prof" --default-background-color=00000000 \
    --force-device-scale-factor=1 --window-size="$W,$size" \
    --virtual-time-budget=3000 \
    --screenshot="$PWD/png/$nom.png" "file:///tmp/cfdlmarca.html" >/dev/null 2>&1 &
  pid=$!; ( sleep 25; kill -9 $pid 2>/dev/null ) >/dev/null 2>&1 & k=$!
  wait $pid 2>/dev/null; kill -9 $k 2>/dev/null; rm -rf "$prof"
  echo "png/$nom.png  ${W}×${size}"
done
