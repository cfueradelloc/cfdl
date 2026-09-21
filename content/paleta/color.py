#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matemática de color, de biblioteca estándar.

Existe porque las decisiones de paleta se tomaron midiendo, no a ojo, y eso
tiene que poder repetirse. sRGB ↔ XYZ ↔ Lab ↔ LCh con iluminante D65, más el
contraste de la WCAG.

LCh es Lab en polares: L* es la claridad (0 negro, 100 blanco), C* el croma
—cuánto se aleja del gris—, y h el matiz en grados. Se trabaja aquí y no en
HSL porque HSL miente sobre la claridad: el amarillo puro y el azul puro
tienen la misma «lightness» 50 % y no se parecen en nada.
"""
import math

D65 = (0.95047, 1.0, 1.08883)


# ── sRGB ───────────────────────────────────────────────────────────────────
def _a_lineal(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _a_gamma(c):
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(v * 255)))


def rgb(hexa):
    """«#ffb923» → (255, 185, 35). Acepta con o sin almohadilla."""
    h = hexa.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ── Lab y LCh ──────────────────────────────────────────────────────────────
def lab(hexa):
    r, g, b = (_a_lineal(v) for v in rgb(hexa))
    X = 0.4124 * r + 0.3576 * g + 0.1805 * b
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    Z = 0.0193 * r + 0.1192 * g + 0.9505 * b

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(X / D65[0]), f(Y / D65[1]), f(Z / D65[2])
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lch(hexa):
    """→ (L*, C*, h). El matiz en grados, 0–360."""
    L, a, b = lab(hexa)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def desde_lch(L, C, h):
    """El camino de vuelta: (L*, C*, h) → «#rrggbb». Recorta a la gama sRGB,
    así que pedir un croma imposible devuelve el más cercano que existe."""
    a = C * math.cos(math.radians(h))
    b = C * math.sin(math.radians(h))
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200

    def g(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    X, Y, Z = g(fx) * D65[0], g(fy) * D65[1], g(fz) * D65[2]
    return "#%02x%02x%02x" % (
        _a_gamma(3.2406 * X - 1.5372 * Y - 0.4986 * Z),
        _a_gamma(-0.9689 * X + 1.8758 * Y + 0.0415 * Z),
        _a_gamma(0.0557 * X - 0.2040 * Y + 1.0570 * Z))


def distancia(a, b):
    """ΔE CIE94 aproximada: cuánto se distinguen dos colores. Por debajo de 2
    el ojo apenas los separa; por encima de 5 son colores distintos."""
    La, Ca, Ha = lch(a)
    Lb, Cb, Hb = lch(b)
    dh = math.radians(min(abs(Ha - Hb), 360 - abs(Ha - Hb)))
    dH = 2 * math.sqrt(Ca * Cb) * math.sin(dh / 2)
    return math.sqrt((La - Lb) ** 2 + (Ca - Cb) ** 2 + dH ** 2)


def salto_matiz(a, b):
    """Grados entre dos matices por el camino corto. 180 = complementarios."""
    ha, hb = lch(a)[2], lch(b)[2]
    d = abs(ha - hb)
    return min(d, 360 - d)


# ── contraste ──────────────────────────────────────────────────────────────
def luminancia(hexa):
    r, g, b = (_a_lineal(v) for v in rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    """Razón de contraste WCAG 2.1, de 1:1 a 21:1."""
    l1, l2 = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def nivel(c):
    """Qué permite una razón de contraste dada.

    AAA   ≥ 7,0   texto pequeño, sin reservas
    AA    ≥ 4,5   texto normal — el mínimo para leer
    grande ≥ 3,0  sólo titulares (≥24 px, o ≥19 px en negrita) e iconos
    no     < 3,0  no se puede poner uno sobre otro y esperar que se lea
    """
    return "AAA" if c >= 7 else "AA" if c >= 4.5 else "grande" if c >= 3 else "no"


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        L, C, h = lch(sys.argv[1])
        print(f"{sys.argv[1]}  L*{L:.1f}  C*{C:.1f}  h{h:.0f}°")
    elif len(sys.argv) == 3:
        a, b = sys.argv[1], sys.argv[2]
        c = contraste(a, b)
        print(f"{a} / {b}  contraste {c:.2f}:1 ({nivel(c)})  "
              f"matiz {salto_matiz(a, b):.0f}°  ΔE {distancia(a, b):.1f}")
    else:
        print("uso: color.py <hex> | color.py <hex> <hex>")
