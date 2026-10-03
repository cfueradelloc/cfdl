#!/usr/bin/env bash
# Archiva el contenido público de @cfueradelloc en el Drive sincronizado.
#
#   archive.sh                 # anónimo (Instagram suele cortar hacia el post 12)
#   archive.sh chrome          # con las cookies de tu cuenta personal en ese navegador
#                              # (chrome | safari | firefox | brave | edge …)
#
# Incremental: --fast-update se detiene en el primer post que ya existe.
set -euo pipefail

PROFILE="cfueradelloc"
DRIVE="${CFDL_DRIVE:-/Users/mduranfrigola/Library/CloudStorage/GoogleDrive-miquelduranfrigola@gmail.com/My Drive/Documents/Writing/CFDL}"
DEST="$DRIVE/Instagram"
BROWSER="${1:-}"

# Venv propio: el instaloader de Homebrew no trae browser_cookie3 y no puede leer cookies.
VENV="${INSTALOADER_VENV:-$HOME/.local/venvs/instaloader}"
INSTALOADER="$VENV/bin/instaloader"
if [ ! -x "$INSTALOADER" ]; then
  echo "Falta instaloader. Instálalo con:" >&2
  echo "  python3 -m venv \"$VENV\" && \"$VENV/bin/pip\" install instaloader browser_cookie3" >&2
  exit 2
fi
[ -d "$DRIVE" ] || { echo "No encuentro el Drive en: $DRIVE" >&2; exit 2; }
mkdir -p "$DEST"

ARGS=(
  --dirname-pattern "$DEST/{target}"
  --filename-pattern "{date_utc:%Y-%m-%d}_{shortcode}"
  --fast-update
  --no-compress-json
  --sanitize-paths
)

if [ -n "$BROWSER" ]; then
  # Sesión de tu cuenta personal, no la del colectivo: desbloquea paginación completa y destacadas.
  ARGS+=(--load-cookies "$BROWSER" --highlights --reels)
else
  # Anónimo: abortar en seco ante un bloqueo en lugar de esperar horas.
  ARGS+=(--abort-on 302,400,401,403,429)
fi

set +e
"$INSTALOADER" "${ARGS[@]}" -- "$PROFILE"
status=$?
set -e

python3 "$(dirname "$0")/index.py" "$DEST/$PROFILE"

if [ $status -ne 0 ]; then
  echo >&2
  echo "instaloader terminó con código $status." >&2
  [ -z "$BROWSER" ] && echo "Si Instagram cortó el acceso anónimo, repite con tu navegador: archive.sh chrome" >&2
  exit $status
fi
