#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la firma: el signo junto a las siglas.

Es la prueba que decide: al lado de la letra se ve si el peso óptico casa, si
la altura está bien puesta y si se acompañan o compiten.

Las medidas salen del OTF (ver metricas.py), no de una estimación. Se estimó a
ojo dos veces y las dos salió mal — altura de mayúscula 0,70 em cuando es
0,754 (las mayúsculas se salían de la caja) y ancho de «C.F.D.L.» 4,06 y luego
4,46 em cuando es 3,48 (el campo sobraba un 28 %).
"""
from metricas import Futura

_F = Futura()
FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"
AMBAR, NEGRO, BLANCO = "#ffb923", "#171513", "#ffffff"

CAP_EM = _F.cap_em                      # 0.7540
SIGLAS = "C.F.D.L."
ANCHO_EM = _F.ancho(SIGLAS)             # 3.4800


def firma(cuerpo, ratio=1.0, alto=58, ink=NEGRO, campo=None,
          rel=1.35, sep=0.30, texto=SIGLAS, aire=0.0):
    """cuerpo: el dibujo del signo (sin envolver), sobre 100 × 100·ratio.

    rel   altura del signo ÷ altura de mayúscula. Un signo de línea fina pesa
          mucho menos que una versaleta maciza, así que por defecto va mayor
          que la caja: 1.35. Con 1.0 la letra se lo come.
    sep   aire entre signo y siglas, en alturas de signo.
    aire  margen alrededor de toda la firma, en alturas de signo.
    """
    mh = 100.0
    mw = mh / ratio
    k = 1.0 / ratio
    cap = mh / rel
    fs = cap / CAP_EM
    m = mh * aire
    x = m + mw + mh * sep
    ancho = x + fs * ANCHO_EM + m
    alto_caja = mh + 2 * m
    fondo = (f'<rect width="{ancho:.2f}" height="{alto_caja:.2f}" fill="{campo}"/>'
             if campo else "")
    # la línea de base centra la ALTURA DE MAYÚSCULA en la caja del signo
    y = m + (mh + cap) / 2
    return (f'<svg viewBox="0 0 {ancho:.2f} {alto_caja:.2f}" '
            f'width="{round(alto*ancho/alto_caja)}" height="{alto}" '
            f'xmlns="http://www.w3.org/2000/svg">{fondo}'
            f'<g transform="translate({m:.2f},{m:.2f}) scale({k:.5f})">{cuerpo}</g>'
            f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FUENTE}" '
            f'font-size="{fs:.2f}" fill="{ink}">{texto}</text></svg>')
