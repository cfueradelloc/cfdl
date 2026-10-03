#!/usr/bin/env python3
"""Rehace index.md: un índice cronológico del archivo de Instagram.

Uso: index.py <carpeta del perfil>   (p. ej. …/CFDL/Instagram/cfueradelloc)

Lee sólo los nombres de archivo y los .txt de pie de foto que deja instaloader
con --filename-pattern "{date_utc:%Y-%m-%d}_{shortcode}", así que no depende de
la forma del JSON, que cambia entre versiones de la API.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

POST = re.compile(r"^(\d{4}-\d{2}-\d{2})_([A-Za-z0-9_-]+?)(?:_(\d+))?\.(jpg|jpeg|png|webp|mp4|txt|json)$")
MEDIA = {"jpg", "jpeg", "png", "webp", "mp4"}


def scan(folder):
    posts = defaultdict(lambda: {"files": [], "caption": ""})
    for f in sorted(folder.iterdir()):
        m = POST.match(f.name)
        if not m or "profile_pic" in f.name:
            continue
        date, code, _, ext = m.groups()
        p = posts[(date, code)]
        if ext in MEDIA:
            p["files"].append(f.name)
        elif ext == "txt":
            p["caption"] = f.read_text(encoding="utf-8", errors="replace").strip()
    return posts


def kind(files):
    videos = [f for f in files if f.endswith(".mp4")]
    if len(files) > 1 and not (len(files) == 2 and videos):
        return f"carrusel ({len(files)})"
    return "vídeo" if videos else "foto"


def first_line(text, n=110):
    line = next((l.strip() for l in text.splitlines() if l.strip()), "")
    return line if len(line) <= n else line[: n - 1].rstrip() + "…"


def main():
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"index.py: no existe {folder}; nada que indexar", file=sys.stderr)
        return
    posts = scan(folder)
    root = folder.parent
    subfolders = sorted(d for d in folder.iterdir() if d.is_dir())

    out = [
        f"# Archivo de Instagram — @{folder.name}",
        "",
        f"{len(posts)} publicaciones. Generado por `skills/instagram-archive` — no editar a mano.",
        "",
        "| fecha | tipo | texto | archivos |",
        "|---|---|---|---|",
    ]
    for (date, code), p in sorted(posts.items()):
        caption = first_line(p["caption"]).replace("|", "\\|") or "—"
        link = f"[{code}](https://www.instagram.com/p/{code}/)"
        out.append(f"| {date} | {kind(p['files'])} | {caption} | {link} · {len(p['files'])} |")

    if subfolders:
        out += ["", "## Destacadas", ""]
        for d in subfolders:
            n = sum(1 for f in d.iterdir() if f.suffix.lower().lstrip(".") in MEDIA)
            out.append(f"- `{d.name}/` — {n} archivos")

    (root / "index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"index.md: {len(posts)} publicaciones")


if __name__ == "__main__":
    main()
