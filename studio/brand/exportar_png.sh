#!/bin/bash
# Exporta los SVG principales a PNG en los tamaños que hacen falta de verdad.
# El SVG es el maestro; esto es sólo conveniencia para subir una foto de perfil
# o dejar un favicon.
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p png
LISTA=(
  "cfdl-perfil-grande-ambar-negro          1080 perfil-instagram"
  "cfdl-monograma-grande-ambar-negro        512 monograma-512"
  "cfdl-monograma-grande-ninguno-negro      512 monograma-negro"
  "cfdl-monograma-grande-ninguno-blanco     512 monograma-blanco"
  "cfdl-monograma-pequeno-ambar-negro      180 favicon-180"
  "cfdl-monograma-pequeno-ambar-negro       32 favicon-32"
  "cfdl-linea-medio-ninguno-negro         200 linea-negro"
  "cfdl-linea-medio-ninguno-blanco        200 linea-blanco"
  "cfdl-linea-medio-ninguno-zafiro        200 linea-zafiro"
  "cfdl-nombre-medio-ninguno-negro        200 nombre-negro"
  "cfdl-nombre-medio-ninguno-blanco       200 nombre-blanco"
  "cfdl-nombre-medio-ninguno-zafiro       200 nombre-zafiro"
  "cfdl-hoja-grande-ambar-negro             900 hoja"
)
for fila in "${LISTA[@]}"; do
  set -- $fila
  svg="svg/$1.svg"; size=$2; nom=$3
  [ -f "$svg" ] || { echo "falta $svg"; continue; }
  # El ancho sale del viewBox del propio SVG. Antes se codificaba a mano
  # (3,4 para la línea) y dejó de coincidir en cuanto cambió la separación:
  # el PNG salía 680 de ancho donde tocaban 613.
  W=$(python3 - "$svg" "$size" <<'PY'
import re, sys
d = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', d)
vw, vh = float(m.group(1)), float(m.group(2))
print(round(int(sys.argv[2]) * vw / vh))
PY
)
  cat > /tmp/cfdlmarca.html <<EOF
<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:'FuturaStd';src:url('$PWD/../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}
html,body{margin:0;padding:0;width:${W}px;height:${size}px;background:transparent}
svg{display:block;width:${W}px;height:${size}px}
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
