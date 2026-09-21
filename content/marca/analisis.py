#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — análisis del dibujo. Mide en vez de opinar.

Tres cosas que en una marca geométrica no se pueden dejar al ojo:

  centro de masa   dónde está de verdad la tinta. Una espiral hacia dentro
                   reparte su peso de forma asimétrica; centrar la CAJA no es
                   centrar el DIBUJO.
  aire perimetral  cuánto respira por cada lado. Si los cuatro márgenes no son
                   iguales, la marca se ve descolgada aunque la caja cuadre.
  hueco interior   el vacío central contra el ritmo trazo/hueco. Si no guarda
                   relación con el paso, se ve como un agujero, no como el
                   final de la espiral.
"""
import math
from espiral import espiral, U


def segmentos(P):
    return [(P[i], P[i+1]) for i in range(len(P)-1)
            if P[i] != P[i+1]]


def centro_masa(P, gr):
    """Centroide de la tinta: cada segmento pesa su longitud por el grosor."""
    mx = my = m = 0.0
    for a, b in segmentos(P):
        L = math.hypot(b[0]-a[0], b[1]-a[1])
        w = L * gr
        mx += w * (a[0]+b[0]) / 2
        my += w * (a[1]+b[1]) / 2
        m += w
    return (mx/m, my/m) if m else (0, 0)


def caja(P, gr):
    """Caja real de la tinta.

    No vale restar medio grosor en los dos ejes: un remate a hueso termina
    EXACTO en su punto, y sólo se ensancha en perpendicular. En las esquinas,
    el inglete rellena hasta el vértice exterior. Medirlo mal hacía creer que
    el dibujo se salía media unidad por la izquierda."""
    c = gr / 2
    xs, ys = [], []
    for a, b in segmentos(P):
        if abs(a[1]-b[1]) < 1e-9:            # horizontal
            xs += [a[0], b[0]]; ys += [a[1]-c, a[1]+c]
        else:                                # vertical
            ys += [a[1], b[1]]; xs += [a[0]-c, a[0]+c]
    for (x, y) in P[1:-1]:                   # el inglete llena la esquina
        xs += [x-c, x+c]; ys += [y-c, y+c]
    return min(xs), min(ys), max(xs), max(ys)


def hueco_interior(P, gr):
    """Lado del vacío que queda en el centro, en módulos."""
    c = gr / 2
    ult = P[-4:] if len(P) >= 4 else P
    xs = [x for x, _ in ult]; ys = [y for _, y in ult]
    return (max(xs)-min(xs)) - gr, (max(ys)-min(ys)) - gr


def informe(nombre, **kw):
    P, N, M, gr = espiral(**kw)
    cm = centro_masa(P, gr)
    x0, y0, x1, y1 = caja(P, gr)
    hx, hy = hueco_interior(P, gr)
    paso = kw.get("gr", 1) + kw.get("hu", 1)
    return dict(
        nombre=nombre, N=N, M=M, gr=gr, P=P,
        cm=cm,
        d_cm=(cm[0]-N/2, cm[1]-M/2),
        margenes=(x0, y0, N-x1, M-y1),
        hueco=(hx, hy), paso=paso,
    )


CASOS = [
    ("actual · 16 · 3½",        dict(N=16, vueltas=3.5)),
    ("actual · 16 · 3¾ corte 8", dict(N=16, vueltas=3.75, corte=8)),
    ("20 · 4½ corte 10",        dict(N=20, vueltas=4.5, corte=10)),
    ("12 · 2¾ corte 6",         dict(N=12, vueltas=2.75, corte=6)),
    ("16 · 4 entera",           dict(N=16, vueltas=4)),
    ("10 · 2¼",                 dict(N=10, vueltas=2.25)),
]

if __name__ == "__main__":
    print(f"{'caso':26} {'centro de masa Δ':>18}  {'márgenes i/s/d/b':>22}  "
          f"{'hueco':>11}  paso")
    print("-" * 92)
    for n, kw in CASOS:
        r = informe(n, **kw)
        dx, dy = r["d_cm"]
        mi, ms, md, mb = r["margenes"]
        hx, hy = r["hueco"]
        print(f"{n:26} {dx:+7.2f},{dy:+7.2f} mód  "
              f"{mi:5.2f}/{ms:4.2f}/{md:4.2f}/{mb:4.2f}  "
              f"{hx:4.1f}×{hy:4.1f}  {r['paso']}")


# ── vista anotada ──────────────────────────────────────────────────────────
def anotada(kw, size=420, mostrar=("retícula", "ejes", "caja", "masa")):
    P, N, M, gr = espiral(**kw)
    k = U / N
    W, H = U, U * M / N
    cm = centro_masa(P, gr)
    x0, y0, x1, y1 = caja(P, gr)
    g = []
    if "retícula" in mostrar:
        g += [f'<line x1="{i*k}" y1="0" x2="{i*k}" y2="{H}" stroke="#ff00a0" '
              f'stroke-width="0.25" opacity=".38"/>' for i in range(N+1)]
        g += [f'<line x1="0" y1="{i*k}" x2="{W}" y2="{i*k}" stroke="#ff00a0" '
              f'stroke-width="0.25" opacity=".38"/>' for i in range(M+1)]
    if "caja" in mostrar:
        g.append(f'<rect x="{x0*k:.2f}" y="{y0*k:.2f}" width="{(x1-x0)*k:.2f}" '
                 f'height="{(y1-y0)*k:.2f}" fill="none" stroke="#4af" '
                 f'stroke-width="0.6" stroke-dasharray="2 2"/>')
    if "ejes" in mostrar:
        g.append(f'<line x1="{W/2}" y1="0" x2="{W/2}" y2="{H}" stroke="#4af" '
                 f'stroke-width="0.5" opacity=".8"/>')
        g.append(f'<line x1="0" y1="{H/2}" x2="{W}" y2="{H/2}" stroke="#4af" '
                 f'stroke-width="0.5" opacity=".8"/>')
    if "masa" in mostrar:
        cx, cy = cm[0]*k, cm[1]*k
        g.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="none" '
                 f'stroke="#3f6" stroke-width="0.9"/>')
        g.append(f'<line x1="{cx-5:.2f}" y1="{cy:.2f}" x2="{cx+5:.2f}" y2="{cy:.2f}" '
                 f'stroke="#3f6" stroke-width="0.6"/>')
        g.append(f'<line x1="{cx:.2f}" y1="{cy-5:.2f}" x2="{cx:.2f}" y2="{cy+5:.2f}" '
                 f'stroke="#3f6" stroke-width="0.6"/>')
    from espiral import polilinea
    return (f'<svg viewBox="0 0 {W:.1f} {H:.1f}" width="{round(size*W/H)}" '
            f'height="{size}"><rect width="{W}" height="{H}" fill="#ffb923"/>'
            f'{polilinea(P, N, gr, "#171513")}{"".join(g)}</svg>')


def pagina():
    filas = []
    for n, kw in CASOS:
        r = informe(n, **kw)
        dx, dy = r["d_cm"]; mi, ms, md, mb = r["margenes"]; hx, hy = r["hueco"]
        filas.append(
          f'<div class="u"><div class="v">{anotada(kw, 300)}</div>'
          f'<div class="m"><b>{n}</b>'
          f'<div>centro de masa &Delta; <code>{dx:+.2f}, {dy:+.2f}</code> mód</div>'
          f'<div>márgenes <code>{mi:.2f} / {ms:.2f} / {md:.2f} / {mb:.2f}</code></div>'
          f'<div>hueco interior <code>{hx:.1f} × {hy:.1f}</code> mód '
          f'(paso {r["paso"]})</div></div></div>')
    doc = ('<!doctype html><meta charset="utf-8"><title>análisis</title><style>'
      'body{margin:0;padding:32px 36px;background:#13131a;color:#e6e6ef;'
      'font:14px/1.6 system-ui}'
      'h1{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}'
      '.intro{color:#9a9ab0;max-width:900px;margin:0 0 26px}'
      '.u{display:flex;gap:26px;align-items:center;border-top:1px solid #2a2a38;'
      'padding:20px 0}.v{line-height:0}'
      '.m{font-size:12.5px;color:#9a9ab0}.m b{color:#e6e6ef;font-size:13.5px;'
      'display:block;margin-bottom:7px}'
      'code{background:#22222e;padding:1px 5px;border-radius:3px;color:#ffd27a}'
      '.leg{font-size:12px;color:#83839b;margin-bottom:10px}'
      '.leg i{font-style:normal;padding:1px 6px;border-radius:3px}'
      '</style><h1>C.F.D.L. — análisis del dibujo</h1>'
      '<p class="intro">Medido, no opinado. <span style="color:#ff00a0">rosa</span> '
      'la retícula modular · <span style="color:#4af">azul</span> los ejes y la caja '
      'real de la tinta · <span style="color:#3f6">verde</span> el centro de masa. '
      'Si el verde no cae sobre el cruce azul, la marca se ve descolgada aunque la '
      'caja cuadre.</p>' + "".join(filas))
    open("analisis.html", "w", encoding="utf-8").write(doc)
    print("análisis → content/marca/analisis.html")
