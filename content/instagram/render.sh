#!/bin/bash
# Renderiza cada src/<base>.html a out/<base>.png con Chrome sin cabeza.
#
# El tamaño de ventana lo dicta src/_sizes.txt, que escribe build_posts.py:
# una línea «base ANCHO ALTO» por página. Así conviven 4:5, 1:1 y 9:16 en la
# misma tirada sin que este script tenga que leer JSON.
#
# Cada carril reutiliza UN perfil temporal propio: aislado del navegador del
# usuario (sin bloqueo de instancia única), caliente (sin arranque en frío
# repetido) y en paralelo entre carriles.
#
#   bash render.sh                  todo
#   bash render.sh 2025-12          sólo las páginas que contengan ese texto
#   SCALE=2 bash render.sh          maestro al doble (Instagram recorta a 1080)
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANES=4
SCALE="${SCALE:-1}"
mkdir -p out

if [ ! -f src/_sizes.txt ]; then
  echo "falta src/_sizes.txt — ejecuta antes: python3 build_posts.py"; exit 1
fi

FILTRO="${1:-}"
# _sizes.txt: «página destino ancho alto». La página vive plana en src/; el
# destino lleva subcarpeta, una por publicación.
mapa=()
while read -r plano dest W H; do
  [ -z "$plano" ] && continue
  [ -n "$FILTRO" ] && case "$dest" in *"$FILTRO"*) ;; *) continue ;; esac
  [ -f "src/$plano.html" ] && mapa+=("$plano|$dest|$W|$H")
done < src/_sizes.txt

if [ ${#mapa[@]} -eq 0 ]; then echo "nada que renderizar"; exit 0; fi

lane() {
  local prof; prof=$(mktemp -d /tmp/cfdligchrome.XXXXXX)
  local e plano dest W H pid killer rest
  for e in "$@"; do
    plano="${e%%|*}"; rest="${e#*|}"
    dest="${rest%%|*}"; rest="${rest#*|}"
    W="${rest%%|*}"; H="${rest##*|}"
    mkdir -p "out/$(dirname "$dest")"
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
      --no-first-run --no-default-browser-check --disable-extensions \
      --disable-background-networking --disable-component-update --disable-sync \
      --disable-default-apps --metrics-recording-only \
      --disable-client-side-phishing-detection \
      --disable-features=Translate,OptimizationHints,MediaRouter \
      --user-data-dir="$prof" \
      --force-device-scale-factor="$SCALE" --window-size="$W,$H" \
      --virtual-time-budget=3000 --run-all-compositor-stages-before-draw \
      --screenshot="$PWD/out/$dest.png" "file://$PWD/src/$plano.html" >/dev/null 2>&1 &
    pid=$!
    ( sleep 25; kill -9 $pid 2>/dev/null ) >/dev/null 2>&1 &
    killer=$!
    wait $pid 2>/dev/null
    kill -9 $killer 2>/dev/null
  done
  rm -rf "$prof"
}

# una función para un solo archivo, con vigilante propio
uno() {
  local plano="$1" dest="$2" W="$3" H="$4" espera="$5" prof pid killer
  prof=$(mktemp -d /tmp/cfdligchrome.XXXXXX)
  mkdir -p "out/$(dirname "$dest")"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --no-first-run --no-default-browser-check --disable-extensions \
    --disable-background-networking --disable-component-update --disable-sync \
    --disable-default-apps --metrics-recording-only \
    --disable-client-side-phishing-detection \
    --disable-features=Translate,OptimizationHints,MediaRouter \
    --user-data-dir="$prof" \
    --force-device-scale-factor="$SCALE" --window-size="$W,$H" \
    --virtual-time-budget=4000 --run-all-compositor-stages-before-draw \
    --screenshot="$PWD/out/$dest.png" "file://$PWD/src/$plano.html" >/dev/null 2>&1 &
  pid=$!
  ( sleep "$espera"; kill -9 $pid 2>/dev/null ) >/dev/null 2>&1 &
  killer=$!
  wait $pid 2>/dev/null
  kill -9 $killer 2>/dev/null
  rm -rf "$prof"
}

for ((L=0; L<LANES; L++)); do
  shard=()
  for ((i=L; i<${#mapa[@]}; i+=LANES)); do shard+=("${mapa[$i]}"); done
  [ ${#shard[@]} -gt 0 ] && lane "${shard[@]}" &
done
wait

# Segunda pasada, en serie y con más margen. Chrome sin cabeza falla de vez en
# cuando bajo carga en paralelo —una página con SVG externos se pasó de los 25s
# y se quedó sin PNG, en silencio—. Un PNG que falta no debe pasar inadvertido.
faltan=()
for e in "${mapa[@]}"; do
  rest="${e#*|}"; dest="${rest%%|*}"
  [ -f "out/$dest.png" ] || faltan+=("$e")
done
if [ ${#faltan[@]} -gt 0 ]; then
  echo "reintentando ${#faltan[@]} página(s) en serie…"
  for e in "${faltan[@]}"; do
    plano="${e%%|*}"; rest="${e#*|}"
    dest="${rest%%|*}"; rest="${rest#*|}"
    uno "$plano" "$dest" "${rest%%|*}" "${rest##*|}" 60
  done
fi

hechos=0; perdidos=()
for e in "${mapa[@]}"; do
  rest="${e#*|}"; dest="${rest%%|*}"
  if [ -f "out/$dest.png" ]; then hechos=$((hechos+1)); else perdidos+=("$dest"); fi
done
echo "RENDER_DONE $hechos/${#mapa[@]} páginas → out/*.png"
if [ ${#perdidos[@]} -gt 0 ]; then
  printf 'SIN RENDERIZAR: %s\n' "${perdidos[@]}"
  exit 1
fi
