#!/bin/bash
# Enlaza con Google Drive el material del repo que no va en git.
#
# Cada ruta de PATHS vive de verdad en Drive (CFDL/Contenido/GitHub, misma ruta
# relativa que en el repo) y en el repo es un enlace simbólico, ignorado por git.
# Los generadores escriben a través del enlace y Drive sincroniza solo.
#
# Idempotente. Por cada ruta:
#   - ya es un enlace a Drive          → nada
#   - no existe en el repo             → crea el enlace (máquina nueva)
#   - es carpeta/archivo real y Drive
#     no la tiene                      → la copia a Drive, verifica y la enlaza
#   - existe en los dos lados          → no toca nada y avisa (resolver a mano)
#
# Uso:  scripts/link-drive.sh            (DRIVE_GITHUB=… para otra ruta de Drive)
set -euo pipefail

DRIVE_GITHUB="${DRIVE_GITHUB:-$HOME/Library/CloudStorage/GoogleDrive-miquelduranfrigola@gmail.com/My Drive/Documents/Writing/CFDL/Contenido/GitHub}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"

PATHS=(
  studio/tshirts/out
  studio/tshirts/assets/photos
  studio/tshirts/assets/Manifesto_Fuera_De_Lugar.pdf
  studio/instagram/out
  studio/instagram/assets/retratos
  studio/instagram/assets/portadas
  studio/brand/bocetos
  studio/brand/png
)

[ -d "$DRIVE_GITHUB" ] || { echo "No encuentro la carpeta de Drive: $DRIVE_GITHUB" >&2; exit 1; }

status=0
for p in "${PATHS[@]}"; do
  local_p="$REPO/$p"; drive_p="$DRIVE_GITHUB/$p"
  if [ -L "$local_p" ]; then
    echo "ok      $p"
  elif [ ! -e "$local_p" ]; then
    if [ ! -e "$drive_p" ]; then
      # Carpeta nueva y vacía en los dos lados (p. ej. retratos/): créala en Drive.
      case "$p" in *.*) echo "falta   $p (no está ni en el repo ni en Drive)"; status=1; continue;; esac
      mkdir -p "$drive_p"
    fi
    mkdir -p "$(dirname "$local_p")"
    ln -s "$drive_p" "$local_p"
    echo "enlace  $p"
  elif [ -e "$drive_p" ]; then
    echo "CONFLICTO $p — existe en el repo y en Drive; no toco nada" >&2; status=1
  else
    mkdir -p "$(dirname "$drive_p")"
    if [ -d "$local_p" ]; then
      rsync -a --exclude .DS_Store "$local_p/" "$drive_p/"
      diff -rq -x .DS_Store "$local_p" "$drive_p" >/dev/null \
        || { echo "ERROR   $p — la copia en Drive no coincide; no borro nada" >&2; status=1; continue; }
    else
      cp -p "$local_p" "$drive_p"
      cmp -s "$local_p" "$drive_p" \
        || { echo "ERROR   $p — la copia en Drive no coincide; no borro nada" >&2; status=1; continue; }
    fi
    rm -rf "$local_p"
    ln -s "$drive_p" "$local_p"
    echo "movido  $p → Drive"
  fi
done
exit $status
