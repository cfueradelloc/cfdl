#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la firma: símbolo y siglas, construidos juntos.

EL PROBLEMA. El símbolo es una banda de líneas finas; las siglas son
versalitas macizas. Si se juntan sin más, el símbolo se queda sin voz.

Lo primero que se intentó fue igualar el GROSOR: que la línea de la espiral
pese lo que el asta de la letra. Medido en el propio tipo, el asta de Futura
Book es 0,084 em y la altura de mayúscula 0,754 em — el asta es el 11,1 % de
la mayúscula. Hacer que la línea de la espiral pese eso obliga a 2–3 anillos,
no a siete: la banda fina, que es la que significa algo, es necesariamente
mucho más ligera que la letra. Por ahí no se puede.

LA SOLUCIÓN. No se igualan los grosores: se iguala el GRIS. Se mide qué
fracción de su caja ocupa de tinta cada uno y se abre el interletrado de las
siglas hasta que los dos grises coinciden. Y resulta que abrir las versalitas
ya es el estilo de la casa para las etiquetas, así que la regla no es una
imposición: es lo que ya se hacía, ahora con un número detrás.

AJUSTE DE LA FIRMA — elegido:
  densidad media · rel 3,20 · pie centrado · separación 0,40 · interletrado 0,200 em

La separación se mide en anchos de símbolo y 0,34 no es un número redondo por
casualidad: es donde el hueco entre símbolo y pie vale ≈ el ancho de una
mayúscula (1,14 anchos de «C») y seis veces el hueco entre letras. Esa
proporción es la que hace que el símbolo presida la firma en vez de
incorporarse a la cadena como un signo más. Con 0,14 el hueco era sólo 2,5
veces la interletra y el símbolo se leía como parte de la palabra.

El pie va centrado sobre el eje horizontal del símbolo. Se probó apoyarlo en
la banda y en el borde exterior; centrado es lo que se eligió.

El pie va deliberadamente PEQUEÑO respecto al símbolo. Por debajo de rel ~2,5
los dos compiten como iguales y el ojo tiene que decidir cuál es el logotipo;
por encima, la jerarquía es inequívoca — el símbolo es la marca y las siglas
son su pie. Está más cerca de un colofón que de un lockup corporativo, que es
lo que corresponde a un colectivo cuyo símbolo carga el significado.

  símbolo                gris      interletrado que lo iguala
  7 anillos 1:4         12,6 %     0,32 em
  5 anillos 1:3         16,6 %     0,135 em
  3 anillos 1:2         24,6 %     0 em  (el símbolo pesa algo más: a tamaño
                                    pequeño conviene)
"""
import math
from espiral import espiral, polilinea
from metricas import Futura

_F = Futura()
FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"

CAP_EM   = _F.cap_em              # 0.7540
ASTA_EM  = 0.0840                 # medida sobre el tipo renderizado
SIGLAS   = "C.F.D.L."
AV_EM    = _F.ancho(SIGLAS)       # 3.4800 — ancho de avance
TINTA_EM = 3.2200                 # ancho de TINTA sin interletrado (medido)
HUECOS   = 7                      # espacios entre los 8 signos

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = ("#ffb923","#171513","#332f8a",
                                       "#ffffff","#fff4d6")

# anillos, hueco (en módulos de grosor), vacío central, interletrado que iguala
DENSIDAD = {
    "fina":   dict(anillos=7, hu=4, vacio=0.62, track=0.320),
    "media":  dict(anillos=5, hu=3, vacio=0.60, track=0.200),
    "gruesa": dict(anillos=3, hu=2, vacio=0.55, track=0.000),
}
CORTE_REL = 0.55


def simbolo(densidad="fina", tinta=NEGRO, campo=None, respiro=0.0):
    """El símbolo sobre una caja de 100×100. `respiro` mete el dibujo hacia
    dentro (fracción del lado): hace falta para el recorte circular."""
    d = DENSIDAD[densidad]
    a, hu, v = d["anillos"], d["hu"], d["vacio"]
    banda = a * (1 + hu)
    N = int(round(2 * banda / (1 - v)))
    corte = banda + (N - 2 * banda) * CORTE_REL
    P, *_ , g = espiral(N=N, vueltas=a, gr=1, hu=hu, corte=corte)
    m = N * respiro
    CN = N + 2 * m
    fondo = f'<rect width="100" height="100" fill="{campo}"/>' if campo else ""
    return fondo + polilinea(P, CN, g, tinta, desplaza=(m, m))


def gris_simbolo(densidad="fina"):
    d = DENSIDAD[densidad]
    a, hu, v = d["anillos"], d["hu"], d["vacio"]
    banda = a * (1 + hu); N = int(round(2 * banda / (1 - v)))
    P, *_ , g = espiral(N=N, vueltas=a, gr=1, hu=hu,
                        corte=banda + (N - 2*banda) * CORTE_REL)
    L = sum(math.hypot(P[i+1][0]-P[i][0], P[i+1][1]-P[i][1])
            for i in range(len(P)-1))
    return L * g / (N * N)


def ancho_siglas(track):
    """Ancho de TINTA de «C.F.D.L.», en em, con el interletrado dado."""
    return TINTA_EM + HUECOS * track


def firma(densidad="media", tinta=NEGRO, campo=None, fondo_firma=None,
          rel=3.20, sep=0.40, respeto=0.0, alto=64, apilada=False,
          track=None, con_siglas=True, respiro=0.0, alinea="centro"):
    """La firma completa.

    rel      alto del símbolo ÷ altura de mayúscula. Por encima de ~2,5 las
             siglas dejan de competir con el símbolo y pasan a ser su pie —
             que es la jerarquía correcta cuando el símbolo es el que
             significa algo.
    sep      aire entre símbolo y siglas, medido en ANCHOS DE SÍMBOLO. En
             alturas de mayúscula no vale: al encoger el pie el aire encogía
             con él, y a rel alto el pie casi tocaba el dibujo.
    alinea   dónde se apoya la línea de base del pie:
               base    el borde exterior del símbolo
               banda   el borde INTERIOR de la banda — lo ata a la estructura
                       de la espiral en vez de a una línea cualquiera
               centro  la mayúscula centrada en la caja del símbolo
               tercio  centrada en el tercio inferior
    respeto  área de respeto alrededor, en alturas de símbolo
    track    interletrado; si no se da, el que iguala el gris de esa densidad
    """
    d = DENSIDAD[densidad]
    tr = d["track"] if track is None else track
    S = 100.0                                   # lado del símbolo
    cap = S / rel                               # altura de mayúscula
    fs = cap / CAP_EM
    w_txt = ancho_siglas(tr) * fs
    m = S * respeto
    sim = simbolo(densidad, tinta, campo, respiro)

    # dónde acaba la banda de la espiral, en fracción del lado: hace falta
    # para poder apoyar el pie en la estructura del dibujo y no a ojo
    dd = DENSIDAD[densidad]
    _banda = dd["anillos"] * (1 + dd["hu"])
    _N = int(round(2 * _banda / (1 - dd["vacio"])))
    frac_banda = _banda / _N

    if not con_siglas:
        W = H = S + 2*m
        f = f'<rect width="{W:.2f}" height="{H:.2f}" fill="{fondo_firma}"/>' if fondo_firma else ""
        return (f'<svg viewBox="0 0 {W:.2f} {H:.2f}" width="{round(alto)}" '
                f'height="{round(alto)}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" aria-label="C.F.D.L.">{f}'
                f'<g transform="translate({m:.2f},{m:.2f})">{sim}</g></svg>')

    txt = (f'<text font-family="{FUENTE}" font-size="{fs:.3f}" fill="{tinta}" '
           f'letter-spacing="{tr*fs:.3f}">{SIGLAS}</text>')

    if apilada:
        hueco = S * sep
        W = max(S, w_txt) + 2*m
        H = S + hueco + cap + 2*m
        xs = m + (W - 2*m - S)/2
        xt = m + (W - 2*m - w_txt)/2
        f = f'<rect width="{W:.2f}" height="{H:.2f}" fill="{fondo_firma}"/>' if fondo_firma else ""
        cuerpo = (f'<g transform="translate({xs:.2f},{m:.2f})">{sim}</g>'
                  f'<g transform="translate({xt:.2f},{m+S+hueco+cap:.2f})">{txt}</g>')
    else:
        hueco = S * sep
        W = S + hueco + w_txt + 2*m
        H = S + 2*m
        # dónde se apoya el pie. Con la letra pequeña, «centro» la deja
        # flotando en medio de un símbolo alto; «base» la asienta sobre la
        # misma línea que cierra la espiral, que es lo que la ata al dibujo.
        if alinea == "base":     yb = m + S
        elif alinea == "banda":  yb = m + S * (1 - frac_banda)
        elif alinea == "tercio": yb = m + S*(2/3) + cap/2
        elif alinea == "alto":   yb = m + cap
        else:                    yb = m + (S + cap)/2
        f = f'<rect width="{W:.2f}" height="{H:.2f}" fill="{fondo_firma}"/>' if fondo_firma else ""
        cuerpo = (f'<g transform="translate({m:.2f},{m:.2f})">{sim}</g>'
                  f'<g transform="translate({m+S+hueco:.2f},{yb:.2f})">{txt}</g>')

    return (f'<svg viewBox="0 0 {W:.2f} {H:.2f}" width="{round(alto*W/H)}" '
            f'height="{round(alto)}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="C.F.D.L.">{f}{cuerpo}</svg>')


if __name__ == "__main__":
    print(f"altura de mayúscula {CAP_EM:.4f} em · asta {ASTA_EM:.4f} em "
          f"({100*ASTA_EM/CAP_EM:.1f} % de la mayúscula)")
    for k in DENSIDAD:
        print(f"{k:7} gris {100*gris_simbolo(k):5.2f} %  "
              f"interletrado {DENSIDAD[k]['track']:.3f} em  "
              f"ancho siglas {ancho_siglas(DENSIDAD[k]['track']):.3f} em")
