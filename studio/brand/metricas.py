#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — métricas reales de FuturaStd, leídas del propio OTF.

Se habían estimado a ojo dos veces (altura de mayúscula ≈ 0,70 em; ancho de
«C.F.D.L.» ≈ 4,06 em) y las dos veces salió mal: las mayúsculas se salían de
la caja y el campo sobraba o recortaba. Las tablas del tipo tienen el dato
exacto; no hay razón para adivinarlo.

Lee `head` (unidades por em), `OS/2` (altura de mayúscula), `cmap` formato 4
(carácter → glifo) y `hmtx` (avances). Sólo biblioteca estándar.
"""
import os, struct

AQUI = os.path.dirname(os.path.abspath(__file__))
OTF = os.path.normpath(os.path.join(AQUI, "..", "..", "docs", "assets",
                                    "fonts", "FuturaStd-Book.otf"))


def _tablas(d):
    num = struct.unpack(">H", d[4:6])[0]
    t = {}
    for i in range(num):
        o = 12 + i * 16
        tag = d[o:o+4].decode("latin-1")
        off, ln = struct.unpack(">II", d[o+8:o+16])
        t[tag] = (off, ln)
    return t


def _cmap4(d, off):
    """Subtabla cmap formato 4: unicode → id de glifo."""
    n = struct.unpack(">H", d[off+2:off+4])[0]
    mejor = None
    for i in range(n):
        o = off + 4 + i * 8
        pid, eid, sub = struct.unpack(">HHI", d[o:o+8])
        if (pid, eid) in ((3, 1), (3, 10), (0, 3), (0, 4)):
            mejor = off + sub
    if mejor is None:
        return {}
    fmt = struct.unpack(">H", d[mejor:mejor+2])[0]
    if fmt != 4:
        return {}
    segX2 = struct.unpack(">H", d[mejor+6:mejor+8])[0]
    seg = segX2 // 2
    b = mejor + 14
    fin   = struct.unpack(f">{seg}H", d[b:b+segX2]); b += segX2 + 2
    ini   = struct.unpack(f">{seg}H", d[b:b+segX2]); b += segX2
    delta = struct.unpack(f">{seg}h", d[b:b+segX2]); b += segX2
    rbase = b
    rango = struct.unpack(f">{seg}H", d[b:b+segX2])
    m = {}
    for i in range(seg):
        for c in range(ini[i], min(fin[i], 0xFFFF) + 1):
            if rango[i] == 0:
                g = (c + delta[i]) & 0xFFFF
            else:
                p = rbase + i*2 + rango[i] + (c - ini[i]) * 2
                if p + 2 > len(d): continue
                g = struct.unpack(">H", d[p:p+2])[0]
                if g: g = (g + delta[i]) & 0xFFFF
            if g: m[c] = g
    return m


class Futura:
    def __init__(self, ruta=OTF):
        d = open(ruta, "rb").read()
        t = _tablas(d)
        ho, _ = t["head"]
        self.upem = struct.unpack(">H", d[ho+18:ho+20])[0]
        oo, _ = t["OS/2"]
        ver = struct.unpack(">H", d[oo:oo+2])[0]
        self.cap = (struct.unpack(">h", d[oo+88:oo+90])[0]
                    if ver >= 2 else int(0.70 * self.upem))
        self.asc, self.desc = struct.unpack(">hh", d[oo+68:oo+72])
        hh, _ = t["hhea"]
        nh = struct.unpack(">H", d[hh+34:hh+36])[0]
        mo, _ = t["hmtx"]
        self.adv = [struct.unpack(">H", d[mo+i*4:mo+i*4+2])[0] for i in range(nh)]
        self.lsb = [struct.unpack(">h", d[mo+i*4+2:mo+i*4+4])[0] for i in range(nh)]
        co, _ = t["cmap"]
        self.cmap = _cmap4(d, co)

    def ancho(self, texto):
        """Ancho del texto en em."""
        tot = 0
        for ch in texto:
            g = self.cmap.get(ord(ch), 0)
            tot += self.adv[g] if g < len(self.adv) else self.adv[-1]
        return tot / self.upem

    def prosa_izq(self, ch):
        """Prosa izquierdo del carácter, en em. Es lo que separa el origen del
        glifo de donde empieza su tinta — si no se descuenta, la firma se
        desplaza a la derecha y el último punto se sale de la caja."""
        g = self.cmap.get(ord(ch), 0)
        return (self.lsb[g] if g < len(self.lsb) else 0) / self.upem

    @property
    def cap_em(self):
        return self.cap / self.upem


if __name__ == "__main__":
    f = Futura()
    print(f"unidades por em      {f.upem}")
    print(f"altura de mayúscula  {f.cap}  =  {f.cap_em:.4f} em")
    print(f"ascendente/descend.  {f.asc} / {f.desc}")
    for t in ("C.F.D.L.", "C.F.D.L", "CFDL", "C", "."):
        print(f"ancho {t!r:12} {f.ancho(t):.4f} em")
    for ch in "CFDL.":
        print(f"prosa izquierdo {ch!r} {f.prosa_izq(ch):.4f} em")
