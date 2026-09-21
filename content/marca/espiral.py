#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la geometría de la espiral. Núcleo compartido.

Lo usan marca.py (produce la marca), explorador.py (barre parámetros) y
analisis.py (mide). Una sola definición: si la espiral cambia, cambia en un
sitio.

RETÍCULA MODULAR. Grosor y hueco se expresan en módulos enteros; la caja tiene
N×M módulos. Así cada trazo, cada hueco y cada remate cae en línea entera, y la
alineación es demostrable en vez de opinable.
"""
U = 100.0   # el lienzo en unidades de usuario del SVG


def espiral(N=16, vueltas=3.5, gr=1, hu=1, M=None, corte=None, boca=0,
            espejo=False, hu_prog=1.0):
    """Espiral rectangular hacia dentro sobre retícula de N×M módulos.

    gr, hu   grosor de trazo y hueco entre vueltas, en módulos
    corte    módulo en que se detiene la última recta (None = entera).
             Es el gesto abierto: la hoja impresa hace lo mismo.
    boca     módulos que se le quitan al arranque — abre la vuelta exterior
    espejo   invierte el sentido de giro
    hu_prog  el hueco se multiplica por esto en cada vuelta: >1 abre el aire
             hacia dentro, <1 lo cierra. Un texto que gira hace algo así.

    Devuelve (puntos, N, M, gr). Los puntos van en módulos, no en px.
    """
    M = M or N
    c = gr / 2.0
    hu_k = float(hu)
    paso = gr + hu_k
    l, t, r, b = c, c, N - c, M - c
    # el remate de arranque sale a ras de caja, no sobre la línea media de la
    # columna de al lado: medio grosor corto se lee como un error
    P = [(boca if boca else 0.0, t)]
    n = int(vueltas * 4)
    for k in range(n):
        if r - l < paso or b - t < paso:
            break
        ult, lado = (k == n - 1), k % 4
        if lado == 0:   P.append((r, t))
        elif lado == 1: P.append((r, corte if (ult and corte is not None) else b))
        elif lado == 2: P.append((l, b)); t += paso
        else:
            P.append((l, t)); l += paso; r -= paso; b -= paso
            hu_k *= hu_prog; paso = gr + hu_k
    if espejo:
        P = [(N - x, y) for x, y in P]
    return P, N, M, gr


def polilinea(P, N, gr, ink, ancho_extra=0.0, desplaza=(0.0, 0.0)):
    """La espiral como <polyline>, escalada de módulos a unidades de usuario."""
    k = U / N
    dx, dy = desplaza
    d = " ".join(f"{(x+dx)*k:.3f},{(y+dy)*k:.3f}" for x, y in P)
    return (f'<polyline points="{d}" fill="none" stroke="{ink}" '
            f'stroke-width="{(gr+ancho_extra)*k:.3f}" stroke-linejoin="miter" '
            f'stroke-linecap="butt"/>')
