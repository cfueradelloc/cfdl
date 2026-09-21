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
  densidad medio · rel 3,20 · pie centrado · separación 0,40 · interletrado 0,200 em
  (el interletrado es constante en las tres densidades)

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

  tamaño     símbolo            gris
  grande     6 anillos 1:3      18,0 %    104 px
  medio      5 anillos 1:3      16,6 %    60 px
  pequeno    3 anillos 1:2      24,6 %    30 px
"""
import math
from espiral import espiral, polilinea
from metricas import Futura

_F = Futura()
FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"

CAP_EM   = _F.cap_em              # 0.7540
LSB_C    = _F.prosa_izq("C")      # prosa izquierdo de la «C»
ASTA_EM  = 0.0840                 # medida sobre el tipo renderizado
SIGLAS   = "C.F.D.L."
AV_EM    = _F.ancho(SIGLAS)       # 3.4800 — ancho de avance
TINTA_EM = 3.2200                 # ancho de TINTA sin interletrado (medido)
HUECOS   = 7                      # espacios entre los 8 signos

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = ("#ffb923","#171513","#332f8a",
                                       "#ffffff","#fff4d6")
ROSA = "#f8ccce"   # Candy Pink — el --band-fg de docs/assets/css/base.css

# INTERLETRADO CONSTANTE. Se derivó uno por densidad para igualar el gris,
# pero eso era para cuando símbolo y siglas medían lo mismo. Con el pie a un
# tercio manda la legibilidad, y cambiarlo con el tamaño hacía que la firma
# pareciera otra según dónde se usara — además al revés de lo que toca, porque
# la letra pequeña pide más aire, no menos. 0,200 en todas.
#
# EL CORTE, NO. La última vuelta cortada es un gesto de tamaño grande: a 16 px
# deja un pico suelto que se lee como suciedad. La densidad «gruesa», que es la
# del favicon, cierra sus anillos.
#
# anillos, hueco (en módulos de grosor), vacío central, interletrado, corte
# TRES TAMAÑOS, un signo. La retícula cambia con el tamaño porque no caben a
# la vez muchos anillos, un vacío grande y un trazo nítido: a 104 px, siete
# anillos con aire 1:4 dejan el trazo en 0,57 px y la marca se ve gris; con
# aire 1:3, en 0,84, todavía por debajo del píxel. Seis anillos llevan la
# retícula a 107 módulos y el trazo a 0,97 px — sale del subpíxel, y el grande
# sigue siendo el más denso de los tres sin pelearse con el medio.
#          anillos, aire (en grosores), vacío central, interletrado, corte
DENSIDAD = {
    "grande":  dict(anillos=6, hu=3, vacio=0.55, track=0.200, corte=0.55),
    "medio":   dict(anillos=5, hu=3, vacio=0.60, track=0.200, corte=0.55),
    "pequeno": dict(anillos=3, hu=2, vacio=0.55, track=0.200, corte=None),
}
# a qué tamaño se usa cada una
TAMANO = {"grande": 104, "medio": 60, "pequeno": 30}


# Para que un cuadrado quepa ENTERO en el círculo inscrito, su semidiagonal
# tiene que caber en el radio: lado·√2/2 ≤ 50. Con respiro 0,11 el lado era 78
# y la semidiagonal 55,2 — las esquinas se salían. El mínimo es 0,1465, y ahí
# las esquinas rozan el borde. 0,20 deja el lado en 60 y la semidiagonal en
# 42,4: un 85 % del radio, con margen de verdad por dentro.
RESPIRO_CIRCULO = 0.20
# El símbolo SOLO lleva siempre aire dentro de su caja: la espiral no debe
# tocar nunca el límite de la figura. Es el área de respeto del signo, y va
# dentro del propio dibujo para que no dependa de que alguien se acuerde de
# dejarla. En la firma no se aplica: allí el espacio lo gobiernan las reglas
# del conjunto (separación 0,40) y sumarle el respiro lo abriría de más.
RESPIRO_SOLO = 0.12


def simbolo(densidad="grande", tinta=NEGRO, campo=None, respiro=0.0):
    """El símbolo sobre una caja de 100×100. `respiro` mete el dibujo hacia
    dentro (fracción del lado): hace falta para el recorte circular."""
    d = DENSIDAD[densidad]
    a, hu, v = d["anillos"], d["hu"], d["vacio"]
    banda = a * (1 + hu)
    N = int(round(2 * banda / (1 - v)))
    cr = d["corte"]
    corte = None if cr is None else banda + (N - 2 * banda) * cr
    P, *_ , g = espiral(N=N, vueltas=a, gr=1, hu=hu, corte=corte)
    m = N * respiro
    CN = N + 2 * m
    fondo = f'<rect width="100" height="100" fill="{campo}"/>' if campo else ""
    return fondo + polilinea(P, CN, g, tinta, desplaza=(m, m))


def gris_simbolo(densidad="grande"):
    d = DENSIDAD[densidad]
    a, hu, v = d["anillos"], d["hu"], d["vacio"]
    banda = a * (1 + hu); N = int(round(2 * banda / (1 - v)))
    cr = d["corte"]
    P, *_ , g = espiral(N=N, vueltas=a, gr=1, hu=hu,
                        corte=None if cr is None else banda + (N-2*banda)*cr)
    L = sum(math.hypot(P[i+1][0]-P[i][0], P[i+1][1]-P[i][1])
            for i in range(len(P)-1))
    return L * g / (N * N)


def ancho_siglas(track):
    """Ancho de TINTA de «C.F.D.L.», en em, con el interletrado dado."""
    return TINTA_EM + HUECOS * track


def firma(densidad="medio", tinta=NEGRO, campo=None, fondo_firma=None,
          rel=3.20, sep=0.40, respeto=0.0, alto=64, apilada=False,
          track=None, con_siglas=True, respiro=None, alinea="centro"):
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
    # el símbolo solo nunca va a ras: si no se pide otra cosa, lleva su aire
    if respiro is None:
        respiro = RESPIRO_SOLO if not con_siglas else 0.0
    S = 100.0                                   # lado del símbolo
    cap = S / rel                               # altura de mayúscula
    fs = cap / CAP_EM
    # ancho de TINTA, más un pelo para que el antialias del último punto no
    # se coma un píxel al redondear
    w_txt = ancho_siglas(tr) * fs + 0.01 * fs
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

    # El texto se retranquea su prosa izquierdo para que la TINTA empiece
    # exactamente en x. Si no: la separación real salía 0,033 em mayor de lo
    # pedido, y el punto final se salía de la caja y aparecía cortado.
    txt = (f'<text x="{-LSB_C*fs:.3f}" font-family="{FUENTE}" '
           f'font-size="{fs:.3f}" fill="{tinta}" '
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
