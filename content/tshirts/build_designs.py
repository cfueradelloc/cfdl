#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — t-shirt designs v2 (compact, professional, pink in play).
Data-driven: palettes + template builders + DESIGNS. All copy verbatim from
the manifesto; contact tag on every design; prints small & centered (never near
seams); website palette (sapphire+yellow) dominant, candy pink as third note.
No logo."""
import os, glob, json, re

SRC = os.path.join(os.path.dirname(__file__), "src")
# per-design horizontal corrections (slug -> px%) written by autocenter.py
_cf = os.path.join(os.path.dirname(__file__), "centering.json")
CORR = json.load(open(_cf)) if os.path.exists(_cf) else {}

# ---- palettes ----------------------------------------------------------
PAL = {
  "zafiro":   dict(ink="#332f8a", accent="#fde700", field="#fde700", bar="#332f8a", tag="#332f8a", g="white"),
  "citrina":  dict(ink="#171513", accent="#e0a23e", field="#e9ad51", bar="#171513", tag="#171513", g="white"),
  "caramelo": dict(ink="#332f8a", accent="#ef9aa2", field="#f8ccce", bar="#f3b6bb", tag="#332f8a", g="white"),
  "rosa":     dict(ink="#e09aa1", accent="#fde700", field="#f8ccce", bar="#e09aa1", tag="#b9858b", g="white"),
  "amatista": dict(ink="#332f8a", accent="#8c82c3", field="#d9d2ec", bar="#8c82c3", tag="#332f8a", g="white"),
}

TAG = '<div class="tag">@cfueradelloc<span class="sep">·</span>cfdl.site</div>'
# clear palette/text duplicates to drop (no obvious repeats)
REMOVE = {"gfx-moho-z","gfx-moho-caram","gfx-rings-caram","gfx-brujula-z2",
          "gfx-sintesis-c","gfx-emdash-z2","gfx-maleza-amat","marca-blanca-caram",
          "cal-garganta2","fuera-amatista","gfx-rings-zafiro","gfx-sintesis-zafiro"}

STYLE = """
.kicker{margin-bottom:11px}
.hero{font-family:var(--serif);font-style:italic;line-height:0.98;color:var(--ink)}
.oneliner{font-family:var(--serif);font-style:italic;line-height:1.1;color:var(--ink)}
.src{font-family:var(--serif);font-style:italic;color:var(--ink);opacity:.78;line-height:1.4}
.col{font-family:var(--serif);line-height:1.5;color:var(--ink);text-align:center}
.col .m{font-style:italic;box-shadow:inset 0 -0.13em 0 var(--accent)}
.anti .struck{position:relative;display:inline-block;font-family:var(--serif);font-style:italic;color:var(--ink);opacity:.5;margin-bottom:5px}
.anti .struck::after{content:"";position:absolute;left:-5px;right:-5px;top:52%;height:2.5px;background:var(--accent);transform:rotate(-2deg)}
.anti .repl{font-family:var(--serif);font-style:italic;color:var(--ink);line-height:0.98}
.verbs{font-family:var(--sans);text-transform:uppercase;letter-spacing:0.2em;color:var(--ink)}
.verbs div{padding:1px 0}
.verbs .hi{position:relative;display:inline-block}
.verbs .hi::after{content:"";display:block;height:2.5px;background:var(--accent);width:100%;margin-top:2px}
.sigla-grid{display:inline-grid;grid-template-columns:1fr 1fr;gap:0 .16em;font-family:var(--serif);color:var(--ink);line-height:1.04;text-align:center}
.siglacaps{font-family:var(--sans);color:var(--ink)}
.siglaserif{font-family:var(--serif);color:var(--ink);line-height:1}
.namecaps{font-family:var(--sans);text-transform:uppercase;letter-spacing:0.24em;color:var(--ink);line-height:1.5}
.photo{width:100%;display:block;object-fit:cover}
.cap{font-family:var(--serif);font-style:italic;color:var(--ink);opacity:.82;margin-top:9px}
.gfx{display:block;margin:0 auto 11px;max-width:100%;height:auto}
/* displace — out of place */
.disp{font-family:var(--serif);font-style:italic;color:var(--ink);line-height:1.0;text-align:left;display:inline-block}
.disp .l2{display:inline-block}
/* concrete */
.conc{font-family:var(--serif);color:var(--ink);line-height:1}
.conc span{display:inline-block}
.tangle{position:relative;display:inline-block}
.tangle svg{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);overflow:visible}
/* redaction */
.redact{font-family:var(--serif);color:var(--ink);line-height:1.7;text-align:center}
.redact .bar{background:var(--bar);color:transparent;border-radius:1px;padding:0 3px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.indice{text-align:left;display:inline-block}
.indice div{display:flex;align-items:baseline;justify-content:center;gap:8px;padding:1.5px 0}
.indice .n{font-family:var(--sans);color:var(--accent);font-weight:bold;min-width:18px}
.indice .t{font-family:var(--serif);font-style:italic;color:var(--ink)}
.colofon .ed{font-family:var(--sans);text-transform:uppercase;letter-spacing:0.2em;color:var(--ink);opacity:.7}
.truism{font-family:var(--sans);text-transform:uppercase;letter-spacing:0.12em;line-height:1.4;color:var(--ink)}
.glyph{font-family:var(--serif);line-height:1}
.bignum{font-family:var(--serif);line-height:0.88;color:var(--ink)}
.sw-old{position:relative;opacity:.5}
.sw-old::after{content:"";position:absolute;left:-1px;right:-1px;top:54%;height:3px;background:var(--accent);transform:rotate(-3deg)}
.sw-new{box-shadow:inset 0 -0.14em 0 var(--accent)}
.acrostic{font-family:var(--serif);font-style:italic;line-height:1.18;color:var(--ink);text-align:left;display:inline-block}
.acrostic b{font-style:normal;color:var(--ink);box-shadow:inset 0 -0.13em 0 var(--accent)}
.consteln{position:relative;width:168px;height:150px;margin:0 auto}
.consteln span{position:absolute;font-family:var(--serif);font-style:italic;color:var(--ink);white-space:nowrap;line-height:1}
.wool{font-family:var(--sans);text-transform:uppercase;font-weight:bold;letter-spacing:0.02em;line-height:0.9;color:var(--ink)}
.invert{background:var(--ink);color:#f1ece0;display:inline-block;padding:9px 13px;font-family:var(--serif);font-style:italic;line-height:1.16}
.invert .acc{color:var(--accent)}
.syll span{font-family:var(--serif);font-style:italic;line-height:1}
.offgrid{font-family:var(--serif);font-style:italic;color:var(--ink);white-space:nowrap}
.smear div{font-family:var(--serif);font-style:italic;color:var(--ink)}
.freedom span{font-family:var(--serif);font-style:italic;color:var(--ink);display:inline-block;margin:0 .12em;vertical-align:middle}
.pinlabel{font-family:var(--sans);text-transform:uppercase;letter-spacing:0.2em;color:var(--ink)}
.mt6{margin-top:6px}.mt10{margin-top:10px}.mt14{margin-top:14px}
"""

# ---- inline SVG motifs (palette-aware) ---------------------------------
def svg_brujula(s=116):
    ink="stroke:var(--ink);fill:none;stroke-width:2.2"
    return f'''<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 150 150">
<circle cx="75" cy="75" r="58" style="{ink}"/><circle cx="75" cy="75" r="48" style="stroke:var(--ink);fill:none;stroke-width:1;opacity:.4"/>
<polygon points="75,30 84,78 75,70 66,78" style="fill:var(--ink)"/><polygon points="75,120 66,72 75,80 84,72" style="fill:var(--ink);opacity:.35"/>
<circle cx="121" cy="34" r="6.5" style="fill:var(--accent)"/></svg>'''
def svg_rings(s=116):
    c=''.join(f'<circle cx="75" cy="75" r="{r}" style="stroke:var(--ink);fill:none;stroke-width:{2.0-ri*0.16:.2f}"/>' for ri,r in enumerate([66,52,40,29,19]))
    return f'<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 150 150">{c}<circle cx="75" cy="75" r="7" style="fill:var(--accent)"/></svg>'
def svg_crack(s=150):
    w=int(s*1.5)
    return f'''<svg class="gfx" width="{w}" height="{int(w*0.55)}" viewBox="0 0 200 110">
<polyline points="8,56 40,42 70,66 100,34 130,66 160,42 192,56" style="stroke:var(--ink);fill:none;stroke-width:3"/>
<polygon points="42,18 70,24 60,42 38,36" style="fill:var(--ink);opacity:.8"/>
<polygon points="158,18 130,24 140,42 162,36" style="fill:var(--ink);opacity:.8"/>
<polygon points="92,80 110,84 104,98 88,94" style="fill:var(--accent)"/></svg>'''
def svg_moho(s=120):
    pts=[(75,75,22),(95,62,15),(58,64,14),(86,92,13),(60,92,12),(104,82,10),(48,82,9),(96,46,8),(66,48,9),(112,64,7),(40,66,7),(82,108,8)]
    blobs=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--ink);opacity:{0.30+0.05*(i%4):.2f}"/>' for i,(x,y,r) in enumerate(pts))
    sp=''.join(f'<circle cx="{x}" cy="{y}" r="3" style="fill:var(--accent)"/>' for x,y in [(95,62),(60,92),(104,82)])
    return f'<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 150 150">{blobs}{sp}</svg>'
def svg_maleza(s=140):
    paths=["M10,120 C30,60 40,90 55,40 C62,18 70,60 78,30","M50,124 C66,70 74,98 88,52 C96,26 104,66 112,36","M92,122 C108,74 116,100 130,54 C138,30 146,70 158,44"]
    pp=''.join(f'<path d="{d}" style="stroke:var(--ink);fill:none;stroke-width:2;stroke-linecap:round"/>' for d in paths)
    sp=''.join(f'<circle cx="{x}" cy="{y}" r="2.6" style="fill:var(--accent)"/>' for x,y in [(78,30),(112,36),(158,44)])
    return f'<svg class="gfx" width="{s}" height="{int(s*0.76)}" viewBox="0 0 170 130">{pp}{sp}</svg>'
def svg_sintesis(s=116):
    return f'''<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 150 150">
<rect x="46" y="46" width="58" height="58" style="stroke:var(--ink);fill:none;stroke-width:2.4"/>
<rect x="20" y="22" width="26" height="26" transform="rotate(-12 33 35)" style="fill:var(--ink);opacity:.8"/>
<rect x="108" y="30" width="22" height="22" transform="rotate(14 119 41)" style="fill:var(--ink);opacity:.5"/>
<rect x="112" y="104" width="24" height="24" transform="rotate(-10 124 116)" style="fill:var(--accent)"/>
<rect x="18" y="110" width="20" height="20" transform="rotate(18 28 120)" style="fill:var(--ink);opacity:.4"/></svg>'''
def svg_espiral(s=120):
    import math
    pts=[]
    for i in range(0,720,6):
        a=math.radians(i); r=2+i*0.072
        pts.append(f"{75+r*math.cos(a):.1f},{75+r*math.sin(a):.1f}")
    return f'<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 150 150"><polyline points="{" ".join(pts)}" style="stroke:var(--ink);fill:none;stroke-width:1.8"/><circle cx="75" cy="75" r="5" style="fill:var(--accent)"/></svg>'
def svg_emdash(s=150):
    return f'<svg class="gfx" width="{s}" height="{int(s*0.18)}" viewBox="0 0 220 40"><line x1="10" y1="20" x2="210" y2="20" style="stroke:var(--ink);stroke-width:4"/><circle cx="110" cy="20" r="6" style="fill:var(--accent)"/></svg>'
def svg_acordeon(s=160):
    xs=[12,34,56,78,100,122,144,166,188]
    top=[16 if i%2==0 else 40 for i in range(len(xs))]
    bot=[100 if i%2==0 else 124 for i in range(len(xs))]
    panels=''
    for i in range(len(xs)-1):
        pts=f"{xs[i]},{top[i]} {xs[i+1]},{top[i+1]} {xs[i+1]},{bot[i+1]} {xs[i]},{bot[i]}"
        fill="var(--ink)" if i%2==0 else "none"; op="0.12" if i%2==0 else "1"
        panels+=f'<polygon points="{pts}" style="fill:{fill};fill-opacity:{op};stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round"/>'
    return f'<svg class="gfx" width="{s}" height="{int(s*0.68)}" viewBox="0 0 200 136">{panels}<circle cx="78" cy="40" r="4.5" style="fill:var(--accent)"/></svg>'
def svg_sawtooth(s=175):
    n=8; step=200/n; pts=[(i*step, 12 if i%2==0 else 40) for i in range(n+1)]
    path=f"M0,{pts[0][1]:.0f} "+' '.join(f"L{x:.0f},{y:.0f}" for x,y in pts[1:])+" L200,78 L0,78 Z"
    return f'<svg class="gfx" width="{s}" height="{int(s*0.4)}" viewBox="0 0 200 80"><path d="{path}" style="fill:var(--field);stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round"/></svg>'
def svg_dogear(s=120):
    return f'''<svg class="gfx" width="{int(s*0.8)}" height="{s}" viewBox="0 0 130 160">
<path d="M14,12 L96,12 L120,36 L120,148 L14,148 Z" style="fill:none;stroke:var(--ink);stroke-width:2"/>
<path d="M96,12 L120,36 L96,36 Z" style="fill:var(--ink);opacity:.85"/>
<line x1="30" y1="50" x2="104" y2="50" style="stroke:var(--ink);stroke-width:1;opacity:.4"/>
<line x1="30" y1="66" x2="104" y2="66" style="stroke:var(--ink);stroke-width:1;opacity:.4"/>
<line x1="30" y1="82" x2="90" y2="82" style="stroke:var(--ink);stroke-width:1;opacity:.4"/>
<circle cx="107" cy="130" r="5" style="fill:var(--accent)"/></svg>'''
def svg_mask(s=120):
    return f'''<svg class="gfx" width="{int(s*0.82)}" height="{s}" viewBox="0 0 124 150">
<ellipse cx="62" cy="74" rx="42" ry="56" style="fill:none;stroke:var(--ink);stroke-width:2.4"/>
<path d="M30,60 Q44,52 56,60" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>
<path d="M68,60 Q80,52 94,60" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>
<path d="M48,98 Q62,108 76,98" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>
<circle cx="62" cy="20" r="4.5" style="fill:var(--accent)"/></svg>'''
def svg_horizonline(s=150):
    return f'<svg class="gfx" width="{s}" height="{int(s*0.16)}" viewBox="0 0 200 32"><line x1="2" y1="22" x2="198" y2="22" style="stroke:var(--ink);stroke-width:2"/><circle cx="100" cy="22" r="5" style="fill:var(--accent)"/></svg>'
MOTIF={"brujula":svg_brujula,"rings":svg_rings,"crack":svg_crack,"moho":svg_moho,"maleza":svg_maleza,"sintesis":svg_sintesis,"espiral":svg_espiral,"emdash":svg_emdash,"acordeon":svg_acordeon,"sawtooth":svg_sawtooth,"dogear":svg_dogear,"mask":svg_mask,"horizonline":svg_horizonline}

def svg_stamp(center_lines, ring, fill=False, s=140):
    ground = '<circle cx="100" cy="100" r="95" style="fill:var(--field)"/>' if fill else ''
    rings='<circle cx="100" cy="100" r="95" style="stroke:var(--ink);fill:none;stroke-width:2.2"/><circle cx="100" cy="100" r="74" style="stroke:var(--ink);fill:none;stroke-width:1"/>'
    path='<path id="ring" d="M100,100 m0,-84 a84,84 0 1,1 0,168 a84,84 0 1,1 0,-168" style="fill:none;stroke:none"/>'
    rtext=f'<text style="fill:var(--ink);font-family:var(--sans);letter-spacing:3px" font-size="11"><textPath href="#ring" startOffset="2%">{ring}</textPath></text>'
    n=len(center_lines); y0=100-(n-1)*13
    ctext=''.join(f'<text x="100" y="{y0+i*26+7}" text-anchor="middle" style="fill:var(--ink);font-family:var(--serif);font-style:italic" font-size="22">{l}</text>' for i,l in enumerate(center_lines))
    return f'<svg class="gfx" width="{s}" height="{s}" viewBox="0 0 200 200"><defs>{path}</defs>{ground}{rings}{rtext}{ctext}</svg>'

# ---- template builders -------------------------------------------------
def _txtlen(s): return len(re.sub(r'<[^>]+>','',s).replace('&nbsp;',' '))
def _fit(size, segs, em=0.52, target=158):
    """Clamp font-size so the widest line fits within ~target px (the compact box),
    so text never overflows the shirt and stays centred."""
    n=max((_txtlen(s) for s in segs), default=1) or 1
    return min(size, max(9, int(target/(n*em))))
def K(k): return f'<div class="kicker">{k}</div>' if k else ''
def hero(lines, size, kicker=None, src=None, rule=True):
    size=_fit(size, lines, 0.52, 158)
    h=K(kicker)+f'<div class="hero" style="font-size:{size}px">'+'<br>'.join(lines)+'</div>'
    if rule: h+='<hr class="rule">'
    if src: h+=f'<div class="src" style="font-size:11px">{src}</div>'
    return h+TAG
def oneliner(text, size, kicker=None, src=None):
    size=_fit(size, text.split('<br>'), 0.52, 158)
    h=K(kicker)+f'<div class="oneliner" style="font-size:{size}px">{text}</div>'
    if src: h+=f'<div class="src mt10" style="font-size:10.5px">{src}</div>'
    return h+TAG
def column(par, size, kicker=None):
    return K(kicker)+f'<p class="col" style="font-size:{size}px">{par}</p>'+TAG
def antithesis(struck, repl_lines, size, sign=None):
    size=min(_fit(size, repl_lines, 0.52, 158), _fit(int(size), [struck], 0.52*0.44, 150))
    h=f'<div class="anti"><div class="struck" style="font-size:{int(size*0.44)}px">{struck}</div>'
    h+=f'<div class="repl" style="font-size:{size}px">'+'<br>'.join(repl_lines)+'</div></div>'
    if sign: h+=f'<div class="namecaps mt14" style="font-size:8.5px">{sign}</div>'
    return h+TAG
def verbs(items, size, hi=None):
    rows=''.join(f'<div>{("<span class=hi>"+v+"</span>") if i==hi else v}</div>' for i,v in enumerate(items))
    return f'<div class="verbs" style="font-size:{size}px">{rows}</div>'+TAG
def sigla_grid(size, periods=True, sub=None):
    d='.' if periods else ''
    cells=''.join(f'<div>{l}{d}</div>' for l in ['C','F','D','L'])
    h=f'<div class="sigla-grid" style="font-size:{size}px">{cells}</div>'
    if sub: h+=f'<div class="namecaps mt14" style="font-size:8.5px">{sub}</div>'
    return h+TAG
def sigla_line(size, sub=None):
    body='<span class="dot" style="margin:0 .26em"></span>'.join(['C','F','D','L'])
    h=f'<div class="siglacaps" style="font-size:{size}px;letter-spacing:0.26em">{body}</div>'
    if sub: h+=f'<div class="namecaps mt10" style="font-size:8.5px">{sub}</div>'
    return h+TAG
def sigla_serif(text, size, sub=None):
    h=f'<div class="siglaserif" style="font-size:{size}px">{text}</div>'
    if sub: h+=f'<div class="namecaps mt10" style="font-size:8.5px">{sub}</div>'
    return h+TAG
def photo(src, cap, ar="4 / 3"):
    h=f'<img class="photo" src="../assets/photos/{src}" style="aspect-ratio:{ar}">'
    if cap: h+=f'<div class="cap" style="font-size:11px">{cap}</div>'
    return h+TAG
def graphic(motif, caption, cap_size=18, kicker=None, msize=None):
    h=K(kicker)+(MOTIF[motif]() if msize is None else MOTIF[motif](msize))
    if caption:
        cap_size=_fit(cap_size, caption.split('<br>'), 0.52, 150)
        h+=f'<div class="oneliner" style="font-size:{cap_size}px">{caption}</div>'
    return h+TAG
def stamp(center_lines, ring, fill=False, s=140):
    return svg_stamp(center_lines, ring, fill, s)+TAG
def displace(l1, l2, size, dx=34, dy=-2):
    h=f'<div class="disp" style="font-size:{size}px"><div>{l1}</div><div class="l2" style="transform:translate({dx}px,{dy}px)">{l2}</div></div>'
    return h+TAG
def concrete(kind, word, size, caption=None):
    if kind=="stretch":
        body=f'<div class="conc" style="font-size:{size}px;letter-spacing:0.26em;white-space:nowrap">{word}</div>'
    elif kind=="exile":
        n=len(word)
        sp=''.join(f'<span style="transform:translate({(30 if i==n-1 else 0)}px,{(-15 if i==n-1 else 0)}px);opacity:{(0.6 if i==n-1 else 1)}">{c}</span>' for i,c in enumerate(word))
        body=f'<div class="conc" style="font-size:{size}px">{sp}</div>'
    elif kind=="split":
        mid=len(word)//2
        body=f'<div class="conc" style="font-size:{size}px;white-space:nowrap">{word[:mid]}<span style="display:inline-block;width:0.55em"></span>{word[mid:]}</div>'
    elif kind=="sink":
        n=len(word)
        sp=''.join(f'<span style="transform:translateY({int((i/max(1,n-1))**1.6*size*0.5)}px);opacity:{max(0.35,1-(i/max(1,n-1))*0.6):.2f}">{c}</span>' for i,c in enumerate(word))
        body=f'<div class="conc" style="font-size:{size}px">{sp}</div>'
    elif kind=="tangle":
        vines='<svg width="200" height="120" viewBox="0 0 200 120"><path d="M8,100 C40,40 60,80 92,28" style="stroke:var(--accent);fill:none;stroke-width:2"/><path d="M120,108 C150,52 168,86 196,30" style="stroke:var(--accent);fill:none;stroke-width:2"/></svg>'
        body=f'<div class="tangle"><span class="conc" style="font-size:{size}px">{word}</span>{vines}</div>'
    else:
        if kind=="fall":
            offs=[(i, i*i*0.6) for i in range(len(word))]; tf=lambda i,dx,dy:f"translateY({dy:.0f}px)"
        else:  # shatter
            seed=[(-6,-4,-12),(5,3,9),(-3,6,-7),(7,-5,14),(-8,4,-9),(4,7,8),(-5,-6,-11),(8,2,10),(-2,5,-6),(6,-4,12),(-7,3,-8),(3,6,7),(-4,-5,-10)]
            tf=lambda i,a,b:f"translate({seed[i%len(seed)][0]}px,{seed[i%len(seed)][1]}px) rotate({seed[i%len(seed)][2]}deg)"
            offs=[(i,0) for i in range(len(word))]
        spans=''.join((f'<span style="transform:{tf(i,*( (i, i*i*0.6) if kind=="fall" else (0,0)))}">{c if c!=" " else "&nbsp;"}</span>') for i,c in enumerate(word))
        body=f'<div class="conc" style="font-size:{size}px">{spans}</div>'
    h=body
    if caption: h+=f'<div class="oneliner mt14" style="font-size:12px">{caption}</div>'
    return h+TAG
def redaction(tokens, size, kicker=None):
    # tokens: list of (text, redacted_bool)
    body=' '.join((f'<span class="bar">{t}</span>' if r else f'<span>{t}</span>') for t,r in tokens)
    return K(kicker)+f'<div class="redact" style="font-size:{size}px">{body}</div>'+TAG
def heart(inner):
    return inner+TAG
def index(items, size=8.5, kicker=None):
    rows=''.join(f'<div><span class="n">{n}</span><span class="t">{t}</span></div>' for n,t in items)
    return K(kicker)+f'<div class="indice" style="font-size:{size}px">{rows}</div>'+TAG
def colofon(size=20):
    h='<div class="colofon">'
    h+=f'<div class="ital" style="font-size:{size}px;line-height:1.06;color:var(--ink)">Manifiesto cambiante<br>y nunca cumplido</div>'
    h+='<hr class="rule">'
    h+='<div class="namecaps" style="font-size:7.5px">Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc</div>'
    h+='<div class="ed mt6" style="font-size:7px">primera edición — octubre 2023</div></div>'
    return h+TAG
def truism(lines, size, kicker=None):
    size=_fit(size, lines, 0.66, 158)
    return K(kicker)+f'<div class="truism" style="font-size:{size}px">'+'<br>'.join(lines)+'</div>'+TAG
def glyph(ch, size, caption=None, accent=False):
    col="var(--accent)" if accent else "var(--ink)"
    h=f'<div class="glyph" style="font-size:{size}px;color:{col}">{ch}</div>'
    if caption: h+=f'<div class="oneliner mt10" style="font-size:13px">{caption}</div>'
    return h+TAG
def bignum(num, frag, size=110):
    size=_fit(size, [num], 0.56, 175)
    fs=_fit(13, [frag], 0.5, 158)
    return f'<div class="bignum" style="font-size:{size}px">{num}</div><div class="oneliner mt8" style="font-size:{fs}px">{frag}</div>'+TAG
def horizon(word, size, below=None):
    size=_fit(size, [word], 0.52, 150)
    h=f'<div class="ital" style="font-size:{size}px;color:var(--ink)">{word}</div>'+svg_horizonline(150)
    if below: h+=f'<div class="src" style="font-size:11px">{below}</div>'
    return h+TAG
def wordswap(pre, old, new, post, size, caption=None):
    h=f'<div class="hero" style="font-size:{size}px">{pre}<span class="sw-old">{old}</span><span class="sw-new">{new}</span>{post}</div>'
    if caption: h+=f'<hr class="rule"><div class="src" style="font-size:11px">{caption}</div>'
    return h+TAG
def acrostic(pairs, size, kicker=None):
    # pairs: list of (initial, rest) -> initial highlighted
    rows=''.join(f'<div><b>{a}</b>{r}</div>' for a,r in pairs)
    return K(kicker)+f'<div class="acrostic" style="font-size:{size}px">{rows}</div>'+TAG
def fade(lines, top=28, kicker=None):
    n=max(1,len(lines)); out=''
    for i,l in enumerate(lines):
        sz=max(9,int(top*(1-0.62*i/n))); op=max(0.28,1-i*(0.7/n))
        out+=f'<div class="ital" style="font-size:{sz}px;opacity:{op:.2f};line-height:1.2;color:var(--ink)">{l}</div>'
    return K(kicker)+f'<div>{out}</div>'+TAG
def repeat_texture(word, n=16, size=13, kicker=None, fadelast=False):
    items=[word]*n
    body=' '.join(items)
    extra=''
    return K(kicker)+f'<div class="col" style="font-size:{size}px;line-height:1.3;text-align:justify;hyphens:none">{body}</div>'+TAG
def diagram(a, b, size=22, kicker=None):
    size=_fit(size,[a+" → "+b],0.5,156)
    arrow='<span style="margin:0 .35em;color:var(--accent)">→</span>'
    return K(kicker)+f'<div class="ital" style="font-size:{size}px;color:var(--ink);line-height:1.1">{a}{arrow}{b}</div>'+TAG
def bracket(word, size=46, kicker=None):
    size=_fit(size,["("+word+")"],0.5,150)
    return K(kicker)+f'<div class="hero" style="font-size:{size}px">({word})</div>'+TAG
def overlap(w1, w2, size=38):
    size=_fit(size,[w1,w2],0.52,150)
    return f'<div style="position:relative;height:{int(size*1.5)}px"><span class="ital" style="position:absolute;left:50%;top:0;transform:translateX(-50%);font-size:{size}px;color:var(--ink)">{w1}</span><span class="ital" style="position:absolute;left:50%;top:{int(size*0.42)}px;transform:translateX(-50%);font-size:{size}px;color:var(--ink);opacity:.4">{w2}</span></div>'+TAG
def mirror(word, size=40, kicker=None):
    sz=_fit(size,[word],0.52,150)
    return K(kicker)+f'<div class="ital" style="font-size:{sz}px;color:var(--ink);line-height:0.9">{word}</div><div class="ital" style="font-size:{sz}px;color:var(--ink);opacity:.32;transform:scaleY(-1);line-height:0.9">{word}</div>'+TAG
# --- research-driven mechanics ---
_CPOS=[(4,10),(54,4),(26,34),(70,30),(2,56),(40,60),(58,78),(14,84),(34,16),(64,54)]
def constellation(words, size=15, kicker=None):
    sp=''
    for i,w in enumerate(words):
        x,y=_CPOS[i%len(_CPOS)]; s=size+(2 if i%3==0 else (-3 if i%3==1 else 0))
        sp+=f'<span style="left:{x}%;top:{y}%;font-size:{s}px">{w}</span>'
    return K(kicker)+f'<div class="consteln">{sp}</div>'+TAG
def wool(lines, size=42, kicker=None):
    size=_fit(size, lines, 0.66, 150)
    return K(kicker)+f'<div class="wool" style="font-size:{size}px">'+'<br>'.join(lines)+'</div>'+TAG
def invert(lines, size=22, kicker=None):
    size=_fit(size, lines, 0.56, 140)
    return K(kicker)+f'<div class="invert" style="font-size:{size}px">'+'<br>'.join(lines)+'</div>'+TAG
def syllables(parts, size=44, kicker=None):
    size=_fit(size, [''.join(parts)], 0.52, 150)
    sp=''.join(f'<span style="font-size:{size}px;color:var(--ink);opacity:{1 if i%2==0 else 0.4}">{p}</span>' for i,p in enumerate(parts))
    return K(kicker)+f'<div class="syll">{sp}</div>'+TAG
def offgrid(pre, knocked, size=40, dy=-16, kicker=None):
    size=_fit(size,[pre+knocked],0.52,150)
    return K(kicker)+f'<div class="offgrid" style="font-size:{size}px">{pre}<span style="display:inline-block;transform:translateY({dy}px)">{knocked}</span></div>'+TAG
def pin(label, coord="0°00′00″", size=18, kicker=None):
    svg='<svg class="gfx" width="44" height="58" viewBox="0 0 46 60"><path d="M23,2 C11,2 2,11 2,23 C2,38 23,58 23,58 C23,58 44,38 44,23 C44,11 35,2 23,2 Z" style="fill:none;stroke:var(--ink);stroke-width:2.4"/><circle cx="23" cy="22" r="6" style="fill:var(--accent)"/></svg>'
    size=_fit(size,[label],0.52,150)
    return K(kicker)+svg+f'<div class="ital" style="font-size:{size}px;color:var(--ink);margin-top:5px">{label}</div><div class="pinlabel" style="font-size:8.5px;margin-top:4px">{coord}</div>'+TAG
def derive(fragment, size=17, kicker=None):
    svg='<svg class="gfx" width="158" height="64" viewBox="0 0 200 80"><polyline points="6,58 32,18 60,54 90,14 120,58 150,22 188,48" style="fill:none;stroke:var(--ink);stroke-width:2;stroke-dasharray:2.5 6;stroke-linecap:round"/><circle cx="6" cy="58" r="3.5" style="fill:var(--ink)"/><circle cx="188" cy="48" r="5" style="fill:var(--accent)"/></svg>'
    size=_fit(size, fragment.split('<br>'), 0.52, 150)
    return K(kicker)+svg+f'<div class="oneliner" style="font-size:{size}px">{fragment}</div>'+TAG
def smear(line, n=5, size=20, kicker=None):
    size=_fit(size,[line],0.52,150); out=''
    for i in range(n):
        out+=f'<div style="font-family:var(--serif);font-style:italic;color:var(--ink);font-size:{size}px;line-height:1.12;opacity:{max(0.1,1-i*0.92/n):.2f};filter:blur({i*0.7:.1f}px)">{line}</div>'
    return K(kicker)+f'<div class="smear">{out}</div>'+TAG
def freedom(items, kicker=None):
    sp=''.join(f'<span style="font-size:{s}px;transform:translate({dx}px,{dy}px) rotate({r}deg)">{w}</span>' for (w,s,dx,dy,r) in items)
    return K(kicker)+f'<div class="freedom" style="text-align:center;line-height:1.05">{sp}</div>'+TAG

# ---- DESIGNS -----------------------------------------------------------
D=[]
def add(slug, pal, inner, pw=None, cls="", px=None, py=None):
    D.append(dict(slug=slug, pal=pal, inner=inner, pw=pw, cls=cls, px=px, py=py))

# A · TEXTO PURO — the wittiest only (~14) ------------------------------
add("marca-blanca",        "zafiro",  hero(["marca","blanca"], 44))
add("fuera-de-lugar",      "zafiro",  hero(["fuera de","lugar"], 40, kicker="C · F · D · L"))
add("suicidio-creativo",   "citrina", hero(["suicidio","creativo"], 38, src="acto rutinario"))
add("garganta-sin-fondo",  "zafiro",  hero(["garganta","sin fondo"], 38))
add("lo-atopico",          "zafiro",  hero(["lo","atópico"], 56, kicker="ni utópico ni distópico"))
add("resucitar-en-vida",   "caramelo",hero(["resucitar","en vida"], 40))
add("la-inmadurez",        "zafiro",  oneliner("la inmadurez<br>como propósito", 22))
add("naufrago",            "citrina", hero(["náufrago"], 50, src="lo que el mar entrega"))
add("nostalgia-atroz",     "rosa",    hero(["nostalgia","atroz"], 44))
add("esperanza-voraz",     "zafiro",  hero(["esperanza","voraz"], 42, src="sobrante, desmedida"))
add("la-creacion-trastorno","zafiro", oneliner("la creación<br>como trastorno", 26))
add("atopia",              "citrina", hero(["atopia"], 58))
add("la-obra-mejora",      "zafiro",  oneliner("la obra mejora<br>si está fuera de lugar", 19, kicker="10"))
add("marca-blanca-rosa",   "rosa",    hero(["marca","blanca"], 46))

# B · ANTÍTESIS (~12) ----------------------------------------------------
add("anti-marca",      "zafiro",  antithesis("marca personal", ["marca","blanca"], 40, sign="Colectivo Fuera de Lugar"))
add("anti-sintesis",   "zafiro",  antithesis("la síntesis", ["la","disgregación"], 34))
add("anti-cura",       "citrina", antithesis("la cura", ["la","prótesis"], 44))
add("anti-moderacion", "zafiro",  antithesis("la moderación", ["el","dispendio"], 42))
add("anti-empatia",    "caramelo",antithesis("la empatía", ["la","opacidad"], 42))
add("anti-utopico",    "zafiro",  antithesis("lo utópico", ["lo","atópico"], 44))
add("anti-comprension","citrina", antithesis("la comprensión", ["la","aceptación"], 36))
add("anti-coherencia", "zafiro",  antithesis("la coherencia", ["la","enajenación"], 34))
add("anti-ser",        "citrina", antithesis("averiguar qué somos", ["dejar de ser","quien somos"], 28))
add("anti-individuo",  "zafiro",  antithesis("el individuo", ["la","colectividad"], 38, sign="ambas opciones"))
add("anti-tradicion",  "caramelo",antithesis("la tradición", ["la","heterodoxia"], 36))
add("anti-raiz",       "citrina", antithesis("ninguna raíz", ["crear","igual"], 40))

# C · TEXTO + GRÁFICO (SVG) (~14) ---------------------------------------
add("gfx-brujula",   "zafiro",  graphic("brujula","brújula sin imán", 17))
add("gfx-rings",     "citrina", graphic("rings","garganta sin fondo", 16))
add("gfx-crack",     "zafiro",  graphic("crack","ante la síntesis,<br>la disgregación", 16))
add("gfx-moho",      "amatista",graphic("moho","la llegada del moho", 16))
add("gfx-maleza",    "zafiro",  graphic("maleza","maleza", 24))
add("gfx-sintesis",  "zafiro",  graphic("sintesis","la disgregación", 17))
add("gfx-espiral",   "citrina", graphic("espiral","asomarse al vértigo", 15))
add("gfx-emdash",    "zafiro",  graphic("emdash","fuera — de — lugar", 19))
add("gfx-brujula-cit","citrina", graphic("brujula","navegar sin imán", 16))
add("gfx-rings-z",   "zafiro",  graphic("rings","el abismo", 24))
add("gfx-moho-caram","caramelo",graphic("moho","la llegada del moho", 16))
add("gfx-emdash-cit","citrina", graphic("emdash","extemporáneo", 18))
add("gfx-maleza-amat","amatista",graphic("maleza","la misma maleza", 17))
add("gfx-espiral-z", "zafiro",  graphic("espiral","garganta sin fondo", 16))

# D · C.F.D.L. TIPOGRÁFICO (~9) -----------------------------------------
add("cfdl-grid",       "zafiro",  sigla_grid(52, periods=True))
add("cfdl-grid-nodot", "citrina", sigla_grid(56, periods=False))
add("cfdl-grid-name",  "zafiro",  sigla_grid(44, periods=True, sub="Colectivo Fuera de Lugar"))
add("cfdl-line",       "zafiro",  sigla_line(22))
add("cfdl-line-name",  "amatista",sigla_line(20, sub="Col·lectiu Fora de Lloc"))
add("cfdl-serif-big",  "citrina", sigla_serif("CFDL", 64))
add("cfdl-serif-dots", "zafiro",  sigla_serif("C.F.D.L.", 40))
add("cfdl-vertical",   "amatista",sigla_serif("C<br>F<br>D<br>L", 40))
add("cfdl-caramelo",   "caramelo",sigla_grid(54, periods=True))

# E · TIPOGRAFÍA CONCRETA (~6) ------------------------------------------
add("conc-garganta", "zafiro",  concrete("fall","garganta", 40, caption="garganta sin fondo"))
add("conc-disgreg",  "zafiro",  concrete("shatter","disgregación", 30, caption="ante la síntesis"))
add("conc-extenua",  "citrina", concrete("stretch","extenuación", 18, caption="de la palabra, de los recursos"))
add("conc-maleza",   "zafiro",  concrete("tangle","maleza", 42))
add("conc-exilio",   "citrina", concrete("fall","exilio", 46))
add("conc-disgreg-c","caramelo",concrete("shatter","fractura", 34))

# F · SELLOS / CUÑOS (~5) -----------------------------------------------
add("sello-fdl",     "zafiro",  stamp(["fuera de","lugar"], "· COLECTIVO FUERA DE LUGAR · CFDL "))
add("sello-marca",   "caramelo",stamp(["marca","blanca"], "· MARCA BLANCA · COPIA · TRAVESTISMO ", fill=True))
add("sello-atopia",  "citrina", stamp(["atopia"], "· LO ATÓPICO · ANTES QUE LO UTÓPICO "))
add("sello-aduanas", "zafiro",  stamp(["aduanas"], "· ATRAVESAR FRONTERAS · LUGARES COMUNES "))
add("sello-moho",    "caramelo",stamp(["el moho"], "· CONSTRUIMOS PARA LAS RUINAS · "))

# G · DESPLAZADOS (~4) ---------------------------------------------------
add("disp-fdl",      "zafiro",  displace("fuera de", "lugar", 40, dx=40, dy=-4))
add("disp-exilio",   "citrina", displace("exilio y", "destierro", 30, dx=30))
add("disp-atopico",  "zafiro",  displace("siempre en otro", "lugar", 26, dx=44, dy=2))
add("disp-naufrago", "amatista",displace("náu", "frago", 50, dx=24, dy=6))

# H · REDACCIÓN (~3) -----------------------------------------------------
add("red-marca",  "caramelo", redaction([("Frente",1),("a",1),("la",0),("marca",0),("personal",1),("la",0),("marca",0),("blanca",0)], 16, kicker="09"))
add("red-opac",   "zafiro",   redaction([("promulgamos",1),("la",0),("opacidad",0),("y",1),("la",1),("aceptación",0)], 16, kicker="06"))
add("red-ruinas", "citrina",  redaction([("Construimos",0),("pensando",1),("en",1),("las",0),("ruinas",0)], 17, kicker="10"))

# I · BLOQUES DEL MANIFIESTO (~6) ---------------------------------------
add("man-01", "zafiro",  column("Navegar quitándole a la brújula su imán y, así, deambular hasta perder de vista lo inmutable.", 12.5, kicker="01"), pw=170)
add("man-02", "citrina", column('al mirar atrás, un camino lleno de <span class="m">maleza</span>; al mirar adelante, la misma <span class="m">maleza</span>.', 12.5, kicker="02"), pw=170)
add("man-03", "zafiro",  column("Frente a la moderación y el ahorro, el dispendio; la libertad perdida a posta.", 12.5, kicker="03"), pw=170)
add("man-04", "amatista",column("Invocamos el suicidio creativo como acto rutinario. La inmadurez como propósito.", 12.5, kicker="04"), pw=170)
add("man-09", "zafiro",  column('Celebramos el plagio, la copia, la búsqueda promiscua de todo el material creativo.', 12.5, kicker="09"), pw=170)
add("man-10", "citrina", column("La obra se marchita el día que encuentra su público. La obra mejora si está fuera de lugar.", 12.5, kicker="10"), pw=170)

# J · VERBOS (~2) --------------------------------------------------------
add("verbos",  "zafiro",  verbs(["Escogemos","Reivindicamos","Proponemos","Invocamos","Aspiramos","Celebramos"], 13, hi=3))
add("verbos-c","citrina", verbs(["Creemos","Defendemos","Construimos","Usamos"], 15, hi=1))

# K · MANIFIESTO — ideas gráficas (≥5 nuevas) + 2 fotos ----------------
add("man-acordeon", "zafiro",  graphic("acordeon","manifiesto cambiante<br>y nunca cumplido", 13))
add("man-sawtooth", "zafiro",  graphic("sawtooth","fuera de lugar", 19))
add("man-dogear",   "amatista",graphic("dogear","nunca cumplido", 15))
add("man-indice",   "citrina", index([("01","crear donde no alcance ninguna raíz"),("02","la misma maleza"),
    ("03","una garganta sin fondo"),("04","el suicidio creativo"),("05","el producto deforme"),
    ("06","la opacidad"),("07","descendencia bastarda"),("08","el venero creativo"),
    ("09","la marca blanca"),("10","la llegada del moho")], 8, kicker="manifiesto · 01–10"), pw=185)
add("man-colofon",  "zafiro",  colofon(20))
add("man-edicion",  "citrina", stamp(["1.ª","edición"], "· MANIFIESTO CAMBIANTE Y NUNCA CUMPLIDO · "))
add("man-pagina",   "zafiro",  column("Escogemos un mundo de ciudades recordadas, siempre en construcción, en terrenos donde no deberían estar. Crear donde no alcance ninguna raíz.", 10, kicker="01"), pw=158)
add("foto-fan-c",   "citrina", photo("manif_3.jpg","cambiante y nunca cumplido","3 / 2"), pw=180)
add("foto-fan-z",   "zafiro",  photo("manif_3_zafiro.jpg","el manifiesto, fuera de lugar","3 / 2"), pw=180)

# L · NEAR THE HEART — pocket minis (~8) --------------------------------
add("heart-cfdl",   "zafiro",  heart('<div class="siglacaps" style="font-size:13px;letter-spacing:.26em">'+'<span class="dot" style="margin:0 .24em"></span>'.join(["C","F","D","L"])+'</div>'), cls="heart")
add("heart-dot",    "zafiro",  heart('<div class="ital" style="font-size:14px">fuera de lugar</div><div style="margin-top:5px"><span class="dot" style="width:7px;height:7px"></span></div>'), cls="heart")
add("heart-compass","citrina", heart(svg_brujula(58)), cls="heart")
add("heart-marca",  "caramelo",heart('<div class="ital" style="font-size:15px">marca<br>blanca</div>'), cls="heart")
add("heart-emdash", "zafiro",  heart(svg_emdash(80)), cls="heart")
add("heart-sello",  "zafiro",  heart(svg_stamp(["fdl"],"· FUERA DE LUGAR · ", s=92)), cls="heart")
add("heart-atopico","citrina", heart('<div class="ital" style="font-size:16px">atópico</div>'), cls="heart")
add("heart-moho",   "amatista",heart(svg_moho(64)), cls="heart")

# M · MÁS (hacia ~100, sin más texto puro) ------------------------------
add("sello-suicidio","citrina", stamp(["suicidio","creativo"], "· SUICIDIO CREATIVO · INMADUREZ · "))
add("sello-cfdl",    "zafiro",  stamp(["C·F·D·L"], "· COLECTIVO FUERA DE LUGAR · "))
add("sello-fdl-rosa","caramelo",stamp(["fuera de","lugar"], "· FUERA DE LUGAR · ATÓPICO · ", fill=True))
add("gfx-crack-c",   "caramelo",graphic("crack","la fractura profiláctica", 14))
add("gfx-rings-caram","caramelo",graphic("rings","el abismo", 22))
add("conc-ruinas",   "citrina", concrete("shatter","ruinas", 38, caption="pensar en las ruinas"))
add("anti-cordura",  "zafiro",  antithesis("la rehabilitación", ["la","fractura"], 32))
add("disp-marca",    "zafiro",  displace("marca", "blanca", 44, dx=30, dy=4))
add("red-atopico",   "zafiro",  redaction([("Usamos",1),("lo",0),("atópico",0),("antes",1),("que",1),("lo",0),("utópico",1)], 15, kicker="10"))
add("red-extenua",   "caramelo",redaction([("Buscamos",1),("la",0),("extenuación",0),("de",1),("la",1),("palabra",0)], 16, kicker="03"))

# ============ NUEVAS IDEAS (Brossa · Holzer · Ruscha · Swiss · concreta) ============
# N1 · TRUISMS — declaraciones en mayúsculas (Holzer)
add("tru-obra",      "zafiro",  truism(["la obra mejora","si está","fuera de lugar"], 17))
add("tru-raiz",      "citrina", truism(["crear donde no","alcance","ninguna raíz"], 17))
add("tru-averiguar", "zafiro",  truism(["no creamos para","averiguar","lo que somos"], 16))
add("tru-angustia",  "caramelo",truism(["avanzar a favor","de la angustia"], 17))
add("tru-inmadurez", "zafiro",  truism(["la inmadurez","como propósito"], 18))
add("tru-plagio",    "citrina", truism(["celebramos","el plagio"], 22))
add("tru-exilio",    "zafiro",  truism(["reivindicamos","el exilio"], 19))
add("tru-ruinas",    "amatista",truism(["construimos","para las ruinas"], 18))
add("tru-trastorno", "zafiro",  truism(["la creación","como trastorno"], 18))
add("tru-marca",     "citrina", truism(["frente a la","marca personal,","la marca blanca"], 14))
add("tru-fdl",       "zafiro",  truism(["fuera","de lugar"], 26))
add("tru-opacidad",  "amatista",truism(["promulgamos","la opacidad"], 18))
# N2 · CALIGRAMAS — la forma dice el sentido (Brossa / poesía concreta)
add("cal-exilio",    "zafiro",  concrete("exile","exilio", 40, caption="reivindicamos el exilio"))
add("cal-destierro", "citrina", concrete("split","destierro", 28))
add("cal-naufrago",  "amatista",concrete("sink","náufrago", 40))
add("cal-vertigo",   "zafiro",  concrete("fall","vértigo", 44))
add("cal-raiz",      "citrina", concrete("tangle","raíz", 46, caption="ninguna raíz"))
add("cal-dispendio", "zafiro",  concrete("stretch","dispendio", 22, caption="frente al ahorro"))
add("cal-ruinas2",   "caramelo",concrete("shatter","ruinas", 38))
add("cal-fractura2", "zafiro",  concrete("split","fractura", 28))
add("cal-moho2",     "amatista",concrete("sink","moho", 48))
add("cal-angustia",  "citrina", concrete("fall","angustia", 34))
# N3 · JUEGO DE PALABRAS / ACRÓSTICO (Brossa: letra como objeto)
add("sw-atopico",  "zafiro",  wordswap("","u","a","tópico", 40, caption="antes que lo utópico"))
add("rev-atopico", "citrina", oneliner('a<span class="sw-new">tópico</span>', 44, kicker="lo común, dentro"))
add("acr-cfdl",    "zafiro",  acrostic([("C","olectivo"),("F","uera"),("D","e"),("L","ugar")], 24, kicker="C · F · D · L"))
add("acr-cfdl-cat","amatista",acrostic([("C","ol·lectiu"),("F","ora"),("D","e"),("L","loc")], 22, kicker="català"))
add("rev-fuera",   "caramelo", oneliner('a<span class="sw-new">fuera</span>', 44))
# N4 · GLIFOS (signo como obra)
add("gly-c",      "zafiro",  glyph("C", 180, caption="colectivo fuera de lugar"))
add("gly-emdash", "citrina", glyph("—", 140, caption="fuera — de — lugar"))
add("gly-colon",  "zafiro",  glyph(":", 150, caption="la extenuación:"))
add("gly-middot", "amatista",glyph("·", 130, caption="Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc"))
add("gly-dot",    "zafiro",  glyph("•", 80, caption="brújula sin su imán", accent=True))
# N5 · NÚMEROS / EDITORIAL (Swiss)
add("num-03", "zafiro",  bignum("03","una garganta sin fondo"))
add("num-10", "citrina", bignum("10","la llegada del moho"))
add("num-01", "zafiro",  bignum("01","crear donde no alcance ninguna raíz"))
add("num-04", "amatista",bignum("04","la inmadurez como propósito"))
add("num-144","zafiro",  bignum("14,4","km — entre dos orillas"))
add("num-mmxxiii","citrina", bignum("MMXXIII","manifiesto — primera edición"))
# N6 · HORIZONTE (Ruscha / Finlay)
add("hor-inmutable","zafiro",  horizon("lo inmutable", 26, below="deambular hasta perder de vista"))
add("hor-fdl",      "citrina", horizon("fuera de lugar", 24))
add("hor-destierro","amatista",horizon("el destierro", 26))
add("hor-asilo",    "zafiro",  horizon("solicitud de asilo", 22))
# N7 · CATALÀ (bilingüe)
add("cat-fora",     "zafiro",  hero(["fora de","lloc"], 40, kicker="C · F · D · L"))
add("cat-collectiu","amatista",truism(["col·lectiu","fora de lloc"], 18))
add("cat-manifest", "citrina", oneliner("Manifest canviant<br>i mai complert", 19, kicker="català"))
add("cat-naufrag",  "zafiro",  hero(["nàufrag"], 50))
add("cat-maleza",   "caramelo",hero(["mala","herba"], 44))
# N8 · MÁSCARA / travestismo (Brossa)
add("gfx-mask",   "zafiro",  graphic("mask","detrás de una máscara", 15))
add("gfx-mask-c", "citrina", graphic("mask","el travestismo", 16))
# N9 · MÁS FRASES (hero / oneliner verbatim)
add("libertad-posta","zafiro", oneliner("la libertad<br>perdida a posta", 22))
add("condena-vol",  "citrina", oneliner("la condena<br>voluntaria", 24))
add("identidad-inq","amatista",oneliner("una identidad<br>inquieta", 26, src="de paso hacia la incertidumbre"))
add("cultura-subsuelo","zafiro", oneliner("la cultura<br>del subsuelo", 26))
add("venero",       "citrina", oneliner("el venero<br>creativo", 26))
add("lugares-comunes","zafiro", oneliner("lugares<br>comunes", 30, src="aduanas para atravesar fronteras"))
add("ciudades-rec", "amatista",oneliner("ciudades<br>recordadas", 24, src="en construcción donde no deberían estar"))
add("solicitud-asilo2","zafiro", hero(["solicitud","de asilo"], 34))
add("extemporanea", "citrina", hero(["extemporánea"], 38, kicker="políglota y ubicua"))
add("perplejidad",  "zafiro",  oneliner("el extrañamiento<br>y la perplejidad", 22))
add("muros",        "amatista",oneliner("relatos sobre<br>muros derribados", 22))
add("descomposicion","citrina", oneliner("la descomposición<br>de las expectativas", 20))
add("memoria",      "zafiro",  oneliner("no hay modernidad<br>sin memoria", 22))
add("heterodoxia2", "zafiro",  oneliner("no hay tradición<br>sin heterodoxia", 22))
add("atonitos",     "caramelo",hero(["atónitos"], 46, kicker="crear desde la enajenación"))
add("viaje",        "citrina", oneliner("el viaje como acto<br>frustrante e improductivo", 18))
# N10 · SELLOS nuevos
add("sello-extenua","zafiro",  stamp(["extenuación"], "· DE LA PALABRA · DE LOS RECURSOS · "))
add("sello-disgreg","citrina", stamp(["la","disgregación"], "· ANTE LA SÍNTESIS · LA DISGREGACIÓN · "))
add("sello-exilio", "caramelo",stamp(["exilio"], "· EXILIO · DESTIERRO · ASILO · ", fill=True))
add("sello-naufrago","zafiro", stamp(["náufrago"], "· LO QUE EL MAR ENTREGA AL NÁUFRAGO · "))
add("sello-trastorno","citrina",stamp(["trastorno"], "· LA CREACIÓN COMO TRASTORNO · "))
# N11 · GFX variantes (palette / palabra)
add("gfx-brujula-z2","caramelo", graphic("brujula","brújula sin imán", 16))
add("gfx-moho-z",   "zafiro",  graphic("moho","la llegada del moho", 16))
add("gfx-sintesis-c","citrina", graphic("sintesis","la disgregación", 16))
add("gfx-dogear-z", "zafiro",  graphic("dogear","siempre inacabado", 15))
add("gfx-acordeon-c","citrina", graphic("acordeon","manifiesto plegado", 13))
add("gfx-sawtooth-z","caramelo",graphic("sawtooth","la sombra dentada", 17))
add("gfx-mask-amat","amatista", graphic("mask","cientos de máscaras", 15))
add("gfx-emdash-z2","amatista", graphic("emdash","extemporáneo", 18))
# N12 · CERCA DEL CORAZÓN — nuevas mini
add("heart-cfdl2","citrina", heart('<div class="siglacaps" style="font-size:12px;letter-spacing:.26em">'+'<span class="dot" style="margin:0 .24em"></span>'.join(["C","F","D","L"])+'</div>'), cls="heart")
add("heart-fdl",  "zafiro",  heart('<div class="ital" style="font-size:14px">fuera<br>de lugar</div>'), cls="heart")
add("heart-naufrago","amatista", heart('<div class="ital" style="font-size:15px">náufrago</div>'), cls="heart")
add("heart-mask", "zafiro",  heart(svg_mask(52)), cls="heart")
add("heart-fora", "citrina", heart('<div class="ital" style="font-size:14px">fora<br>de lloc</div>'), cls="heart")
add("heart-colon","zafiro",  heart('<div class="glyph" style="font-size:34px">:</div>'), cls="heart")
# N13 · REDACCIÓN nuevas
add("red-individuo","caramelo", redaction([("entre",1),("el",0),("individuo",0),("y",1),("la",0),("colectividad",0),("ambas",1)], 15, kicker="07"))
add("red-asilo",  "zafiro",   redaction([("la",1),("creación",0),("como",1),("solicitud",0),("de",1),("asilo",0)], 15, kicker="01"))
add("red-plagio", "citrina",  redaction([("celebramos",0),("el",1),("plagio,",0),("la",1),("copia",0)], 16, kicker="09"))
# N14 · ANTÍTESIS nuevas (verbatim)
add("anti-utopia2","zafiro",  antithesis("lo distópico", ["lo","atópico"], 38))
add("anti-cura2", "caramelo", antithesis("la rehabilitación", ["la","prótesis"], 32))
add("anti-ahorro","citrina",  antithesis("el ahorro", ["el","dispendio"], 40))
add("anti-mestizo","amatista",antithesis("lo mestizo", ["la","fusión"], 38))

# N15 · más (hacia 200+)
add("num-02","amatista", bignum("02","la misma maleza"))
add("num-05","zafiro",   bignum("05","el producto deforme"))
add("num-06","citrina",  bignum("06","la opacidad"))
add("num-07","zafiro",   bignum("07","descendencia bastarda"))
add("num-08","amatista", bignum("08","el venero creativo"))
add("num-09","caramelo", bignum("09","la marca blanca"))
add("tru-asilo","citrina", truism(["la creación como","solicitud de asilo"], 16))
add("tru-disg", "zafiro",  truism(["ante la síntesis","la disgregación"], 16))
add("cal-garganta2","citrina", concrete("fall","garganta", 36))
add("hero-protesis","zafiro", hero(["la","prótesis"], 50, kicker="antes que la cura"))
add("hero-fusion","amatista", hero(["una","fusión"], 44, kicker="más allá de lo mestizo"))
add("sello-atopia2","zafiro", stamp(["atopia"], "· NI UTÓPICO NI DISTÓPICO · ATÓPICO · "))

# ============ TANDA 3 — más poesía visual (hacia 300) ============
# P1 · FADE — eco que se desvanece (trazo desvanecido, extenuación)
add("fade-trazo",   "zafiro",  fade(["el trazo","desvanecido","imposible","de recorrer"], 30, kicker="02"))
add("fade-maleza",  "citrina", fade(["maleza","maleza","maleza","maleza"], 34))
add("fade-extenua", "amatista",fade(["de la palabra","de los recursos","de la energía"], 24, kicker="extenuación"))
add("fade-eco",     "zafiro",  fade(["lo inmutable","inmutable","mutable","…"], 30))
add("fade-nostalgia","rosa",   fade(["nostalgia","nostalgia","nostalgia"], 36))
add("fade-moho",    "amatista",fade(["el moho","el moho","el moho","el moho"], 30))
add("fade-ruinas",  "citrina", fade(["ruinas","y abandono","y silencio"], 28))
add("fade-asilo",   "zafiro",  fade(["solicitud","de asilo"], 30))
# P2 · REPETICIÓN — textura (lo que se propaga / lugares comunes)
add("rep-moho",     "amatista",repeat_texture("moho", 26, 14, kicker="la llegada del"))
add("rep-maleza",   "zafiro",  repeat_texture("maleza", 20, 14, kicker="al mirar adelante"))
add("rep-fdl",      "citrina", repeat_texture("fuera de lugar", 12, 13))
add("rep-comunes",  "zafiro",  repeat_texture("lugar común", 16, 13, kicker="aduanas"))
add("rep-copia",    "caramelo",repeat_texture("copia", 24, 14, kicker="marca blanca"))
add("rep-exilio",   "amatista",repeat_texture("exilio", 22, 14))
add("rep-ruinas",   "citrina", repeat_texture("ruinas", 22, 14, kicker="construimos para las"))
# P3 · DIAGRAMA — relación con flecha (no antítesis)
add("dia-exilio",   "zafiro",  diagram("exilio","creación", 24, kicker="solicitud de asilo"))
add("dia-raiz",     "citrina", diagram("raíz","maleza", 26))
add("dia-palabra",  "amatista",diagram("la palabra","la extenuación", 20))
add("dia-publico",  "zafiro",  diagram("lo público","lo íntimo", 24))
add("dia-viaje",    "citrina", diagram("el viaje","el asilo", 24))
add("dia-fractura", "caramelo",diagram("la fractura","la prótesis", 22))
add("dia-panico",   "zafiro",  diagram("el pánico","la creación", 22))
# P4 · PARÉNTESIS (Weiner)
add("par-fdl",      "zafiro",  bracket("fuera de lugar", 40))
add("par-atopico",  "citrina", bracket("atópico", 52))
add("par-marca",    "caramelo",bracket("marca blanca", 42))
add("par-naufrago", "amatista",bracket("náufrago", 50))
add("par-sinimaán", "zafiro",  bracket("sin imán", 50))
add("par-deforme",  "citrina", bracket("deforme", 52))
# P5 · SUPERPOSICIÓN (fusión / ambas opciones)
add("ovl-individuo","zafiro",  overlap("individuo","colectividad", 34))
add("ovl-mestizo",  "amatista",overlap("mestizo","fusión", 40))
add("ovl-tradicion","citrina", overlap("tradición","modernidad", 34))
add("ovl-intimo",   "zafiro",  overlap("íntimo","público", 42))
add("ovl-utopico",  "caramelo",overlap("utópico","distópico", 36))
# P6 · ESPEJO (reflejo)
add("mir-resucitar","zafiro",  mirror("resucitar", 40, kicker="en vida"))
add("mir-exilio",   "citrina", mirror("exilio", 46))
add("mir-naufrago", "amatista",mirror("náufrago", 40))
add("mir-atopico",  "zafiro",  mirror("atópico", 46))
add("mir-destierro","caramelo",mirror("destierro", 38))
# P7 · HERO verbatim (palabras nuevas)
add("h-incertidumbre","zafiro", hero(["la","incertidumbre"], 40, kicker="de paso hacia"))
add("h-subsuelo",   "citrina", hero(["la cultura","del subsuelo"], 34))
add("h-deforme",    "zafiro",  hero(["producto","deforme"], 40, src="siempre inacabado"))
add("h-claridad",   "amatista",hero(["forma de","claridad"], 36, kicker="ofuscación abnegada"))
add("h-defectos",   "zafiro",  hero(["nuestros","defectos"], 38, src="abrazamos y desterramos la coherencia"))
add("h-voraz",      "caramelo",hero(["esperanza","voraz"], 42, src="sobrante, desmedida"))
add("h-compania",   "citrina", hero(["en","compañía"], 48, kicker="el camino se hace"))
add("h-intimo",     "zafiro",  hero(["lo íntimo","lo público"], 34))
add("h-fronteras",  "amatista",hero(["atravesar","fronteras", ], 34, kicker="aduanas"))
add("h-organica",   "citrina", hero(["materia","orgánica"], 36, kicker="venero creativo"))
add("h-abandono",   "zafiro",  hero(["el","abandono"], 50, src="su inevitable llegada"))
add("h-marchita",   "amatista",hero(["la obra","se marchita"], 32, src="el día que encuentra su público"))
add("h-pretesis",   "caramelo",hero(["la","prótesis"], 50))
add("h-panico",     "zafiro",  hero(["verdadero","pánico"], 38))
add("h-mascara",    "citrina", hero(["una","máscara"], 46, kicker="cientos de ellas"))
add("h-ligereza",   "zafiro",  hero(["material","ligero"], 40, kicker="suicidio creativo"))
add("h-otro-lugar", "amatista",hero(["en algún","otro lugar"], 32))
add("h-asilo3",     "zafiro",  hero(["solicitud","de asilo"], 36))
add("h-promiscua",  "citrina", hero(["búsqueda","promiscua"], 34, kicker="plagio · copia"))
add("h-inacabado",  "zafiro",  hero(["siempre","inacabado"], 38))
# P8 · TRUISMS nuevos
add("tru2-museo",   "zafiro",  truism(["creamos para un museo","que nunca","visitaremos"], 14))
add("tru2-deber",   "citrina", truism(["en terrenos donde","no deberían estar"], 14))
add("tru2-amistad", "amatista",truism(["no hay creación","sin amistad"], 15))
add("tru2-solos",   "zafiro",  truism(["nacemos solos","morimos solos"], 16))
add("tru2-defecto", "caramelo",truism(["desterramos","la coherencia"], 16))
add("tru2-subsuelo","citrina", truism(["cultura","del subsuelo"], 18))
add("tru2-dejar",   "zafiro",  truism(["dejar de ser","quien somos"], 16))
add("tru2-asilo",   "amatista",truism(["el viaje:","acto improductivo"], 15))
add("tru2-promiscua","zafiro", truism(["búsqueda","promiscua"], 18))
add("tru2-memoria", "citrina", truism(["no hay modernidad","sin memoria"], 15))
# P9 · GLIFOS nuevos
add("gly-f",        "zafiro",  glyph("F", 170, caption="fuera de lugar"))
add("gly-question", "citrina", glyph("·", 150, caption="el punto · el imán"))
add("gly-amp",      "amatista",glyph("&", 150, caption="individuo & colectividad"))
add("gly-slash",    "zafiro",  glyph("/", 160, caption="dentro / fuera"))
add("gly-asterisk", "caramelo",glyph("∗", 140, caption="siempre fuera de lugar"))
# P10 · NÚMEROS / editorial nuevos
add("n2-00",        "zafiro",  bignum("00","ningún lugar"))
add("n2-grados",    "citrina", bignum("0°00′","fuera de todo lugar"))
add("n2-paginas",   "amatista",bignum("1—10","manifiesto cambiante"))
add("n2-inf",       "zafiro",  bignum("∞ ∞","dudar entre dos infinitos"))
add("n2-2023",      "citrina", bignum("2023","primera edición"))
# P11 · SELLOS nuevos
add("se-asilo",     "zafiro",  stamp(["asilo"], "· LA CREACIÓN COMO SOLICITUD DE ASILO · "))
add("se-deforme",   "citrina", stamp(["deforme"], "· PRODUCTO DEFORME · SIEMPRE INACABADO · ", fill=False))
add("se-mascara",   "caramelo",stamp(["máscara"], "· TRAVESTISMO · CIENTOS DE MÁSCARAS · ", fill=True))
add("se-museo",     "zafiro",  stamp(["museo"], "· UN MUSEO QUE NUNCA VISITAREMOS · "))
add("se-subsuelo",  "amatista",stamp(["subsuelo"], "· LA CULTURA DEL SUBSUELO · "))
add("se-pánico",    "citrina", stamp(["pánico"], "· INSTANTES DE VERDADERO PÁNICO · "))
# P12 · CONCRETA nueva (palabras nuevas)
add("c2-incertidumbre","zafiro", concrete("sink","incertidumbre", 22))
add("c2-claridad",  "citrina", concrete("stretch","claridad", 24))
add("c2-abandono",  "amatista",concrete("sink","abandono", 34))
add("c2-fronteras", "zafiro",  concrete("split","fronteras", 28))
add("c2-panico",    "caramelo",concrete("shatter","pánico", 40))
add("c2-deforme",   "citrina", concrete("exile","deforme", 38))
add("c2-incierto",  "zafiro",  concrete("fall","caer", 50))
add("c2-mascara",   "amatista",concrete("split","máscara", 34))
# P13 · CATALÀ nuevos
add("ca2-exili",    "zafiro",  hero(["exili i","desterrament"], 28))
add("ca2-atopic",   "citrina", hero(["allò","atòpic"], 44))
add("ca2-naufragi", "amatista",hero(["nàufrag"], 50))
add("ca2-molsa",    "caramelo",hero(["l'arribada","de la molsa"], 30))
add("ca2-truism",   "zafiro",  truism(["fora","de lloc"], 24))
# P14 · HEART nuevas
add("he-c",         "zafiro",  heart('<div class="glyph" style="font-size:40px">C</div>'), cls="heart")
add("he-emdash2",   "citrina", heart('<div class="glyph" style="font-size:30px">—</div>'), cls="heart")
add("he-atopia",    "amatista",heart('<div class="ital" style="font-size:15px">atopia</div>'), cls="heart")
add("he-dot2",      "zafiro",  heart('<span class="dot" style="width:12px;height:12px"></span>'), cls="heart")
add("he-exilio",    "citrina", heart('<div class="ital" style="font-size:14px">exilio</div>'), cls="heart")
# P15 · más antítesis verbatim (distintas)
add("an2-claridad", "zafiro",  antithesis("la claridad", ["la","ofuscación"], 36))
add("an2-cura",     "citrina", antithesis("la rehabilitación", ["la","prótesis"], 32))
add("an2-raiz",     "amatista",antithesis("la raíz", ["la","maleza"], 40))
add("an2-publico",  "zafiro",  antithesis("lo público", ["lo","íntimo"], 38))
add("an2-cordura2", "caramelo",antithesis("la coherencia", ["la","enajenación"], 34))

# ============ TANDA 4 — poesía visual: «fuera de lugar» + excerptos (hacia 400) ============
# A · FUERA DE LUGAR — mecánicas nuevas (~26)
add("fdl-const",    "zafiro",  constellation(["fuera","de","lugar"], 22))
add("fdl-const2",   "citrina", constellation(["fuera","de","lugar","otro","lugar"], 16))
add("fdl-wool",     "zafiro",  wool(["FUERA","DE","LUGAR"], 44))
add("fdl-wool2",    "citrina", wool(["FUE","RA","DE","LU","GAR"], 40))
add("fdl-woolcat",  "amatista",wool(["FORA","DE","LLOC"], 44))
add("fdl-invert",   "zafiro",  invert(["fuera de","lugar"], 24))
add("fdl-invertcat","citrina", invert(["fora","de lloc"], 24))
add("fdl-syll",     "zafiro",  syllables(["fue","ra·","de·","lu","gar"], 40))
add("fdl-offgrid",  "zafiro",  offgrid("fuera de ","lugar", 36, dy=-16))
add("fdl-offgrid2", "citrina", offgrid("fuera ","de lugar", 30, dy=18))
add("fdl-pin",      "zafiro",  pin("fuera de lugar","0°00′00″"))
add("fdl-pin2",     "citrina", pin("ningún lugar","sin coordenadas"))
add("fdl-nolugar",  "amatista",pin("lugar — no lugar","desplazamiento"))
add("fdl-derive",   "zafiro",  derive("deambular hasta perder<br>de vista lo inmutable"))
add("fdl-derive2",  "citrina", derive("siempre en otro lugar"))
add("fdl-freedom",  "zafiro",  freedom([("fuera",36,0,2,-4),("de",18,6,-12,4),("lugar",40,-4,10,-2)]))
add("fdl-freedom2", "caramelo",freedom([("fora",34,0,0,3),("de",18,4,-10,-5),("lloc",38,-2,8,2)]))
add("fdl-mirror",   "zafiro",  mirror("fuera de lugar", 28))
add("fdl-fade",     "amatista",fade(["fuera de lugar","de lugar","lugar","…"], 30))
add("fdl-rep",      "citrina", repeat_texture("fuera de lugar", 14, 13))
add("fdl-edge",     "zafiro",  constellation(["lugar"], 34))
add("fdl-bracket2", "citrina", bracket("en otro lugar", 34))
add("fdl-otrolugar","zafiro",  hero(["siempre en","otro lugar"], 32, kicker="resucitar en vida"))
add("fdl-truism",   "amatista",truism(["la obra mejora","fuera de lugar"], 16))
add("fdl-invert3",  "caramelo",invert(["siempre","fuera de","lugar"], 22))
add("fdl-syll2",    "citrina", syllables(["a","tó","pi","co"], 50))

# B · EXCERPTOS DEL MANIFIESTO — verbatim, una mecánica cada uno (~58)
add("ex-ciudades",  "zafiro",  offgrid("ciudades ","recordadas", 26, dy=-14))
add("ex-terrenos",  "citrina", wool(["EN TERRENOS","DONDE NO","DEBERÍAN ESTAR"], 22))
add("ex-brujula",   "zafiro",  derive("navegar quitándole<br>a la brújula su imán"))
add("ex-deambular", "amatista",smear("deambular hasta perder", 5, 18))
add("ex-raiz",      "zafiro",  wool(["CREAR DONDE","NO ALCANCE","NINGUNA RAÍZ"], 22))
add("ex-asilo",     "citrina", invert(["la creación:","solicitud","de asilo"], 22))
add("ex-viaje",     "zafiro",  truism(["el viaje:","acto frustrante","e improductivo"], 14))
add("ex-extemporanea","amatista",column("una creación extemporánea, políglota y ubicua, que emana de la cultura del subsuelo.", 13, kicker="02"), pw=168)
add("ex-inquieta",  "zafiro",  oneliner("identidad inquieta,<br>de paso hacia la incertidumbre", 16))
add("ex-trazo",     "citrina", smear("el trazo desvanecido", 5, 18))
add("ex-maleza",    "zafiro",  constellation(["al mirar","atrás","maleza","adelante","la misma"], 15))
add("ex-dejarser",  "citrina", smear("dejar de ser quien somos", 5, 16))
add("ex-noaveriguar","zafiro", wool(["NO PARA SABER","QUÉ SOMOS","SINO PARA","DEJAR DE SERLO"], 16))
add("ex-extenuacion","amatista",fade(["la extenuación","de la palabra","de los recursos","de la energía"], 24))
add("ex-dispendio", "citrina", invert(["frente al ahorro,","el dispendio"], 22))
add("ex-aposta",    "zafiro",  oneliner("la libertad<br>perdida a posta", 24))
add("ex-garganta",  "zafiro",  derive("asomarse a una<br>garganta sin fondo"))
add("ex-trastorno", "caramelo",wool(["LA CREACIÓN","COMO","TRASTORNO"], 30))
add("ex-angustia",  "citrina", offgrid("a favor de ","la angustia", 24, dy=16))
add("ex-panico",    "amatista",smear("verdadero pánico", 5, 22))
add("ex-suicidio",  "zafiro",  invert(["suicidio creativo:","acto rutinario"], 20))
add("ex-inmadurez", "citrina", wool(["LA INMADUREZ","COMO","PROPÓSITO"], 28))
add("ex-protesis",  "zafiro",  diagram("la cura","la prótesis", 24))
add("ex-fractura",  "amatista",syllables(["frac","tu","ra"], 50))
add("ex-resucitar", "zafiro",  mirror("resucitar", 40, kicker="en vida"))
add("ex-deforme",   "citrina", offgrid("producto ","deforme", 30, dy=-14, kicker="siempre inacabado"))
add("ex-ofuscacion","zafiro",  smear("la ofuscación abnegada", 6, 17))
add("ex-defectos",  "amatista",column("Abrazamos nuestros defectos y desterramos la coherencia para crear desde la enajenación, atónitos.", 13, kicker="05"), pw=168)
add("ex-voraz",     "caramelo",wool(["ESPERANZA","VORAZ"], 40))
add("ex-nostalgia", "rosa",    invert(["nostalgia","atroz"], 30))
add("ex-solos",     "zafiro",  wool(["NACEMOS SOLOS","MORIMOS SOLOS"], 22))
add("ex-amistad",   "citrina", oneliner("no hay creación<br>sin amistad", 24))
add("ex-opacidad",  "zafiro",  invert(["promulgamos","la opacidad"], 24))
add("ex-zonas",     "amatista",smear("las zonas oscuras del otro", 5, 15))
add("ex-perplejidad","citrina", constellation(["el","extrañamiento","y la","perplejidad"], 15))
add("ex-ambas",     "zafiro",  freedom([("individuo",26,0,-6,-3),("y",16,0,0,0),("colectividad",26,0,6,2)]))
add("ex-intimo",    "citrina", oneliner("lo íntimo con<br>pedazos de lo público", 16))
add("ex-muros",     "zafiro",  wool(["RELATOS SOBRE","MUROS","DERRIBADOS"], 22))
add("ex-descendencia","amatista",column("Formar una descendencia bastarda, desheredada y con traumas.", 14, kicker="07"), pw=168)
add("ex-tradicion", "zafiro",  oneliner("no hay tradición<br>sin heterodoxia", 18))
add("ex-infinitos", "citrina", constellation(["dos","∞","infinitos","∞","habitar"], 16))
add("ex-inamovibles","zafiro", wool(["OPINIONES","ESTÉTICAS","INAMOVIBLES"], 22))
add("ex-fusion",    "amatista",overlap("mestizo","fusión", 38))
add("ex-reciclado", "citrina", oneliner("el reciclado:<br>fuente de material", 18))
add("ex-venero",    "zafiro",  oneliner("el contenedor de materia<br>como venero creativo", 14))
add("ex-naufrago",  "amatista",derive("lo que el mar entrega<br>al náufrago"))
add("ex-plagio",    "zafiro",  repeat_texture("copia", 22, 14, kicker="celebramos el plagio"))
add("ex-aduanas",   "citrina", oneliner("aduanas desde las que<br>atravesar fronteras", 15, kicker="lugares comunes"))
add("ex-marca",     "zafiro",  invert(["marca personal →","marca blanca"], 18))
add("ex-talleres",  "caramelo",oneliner("la copia manufacturada<br>en talleres ilegales", 15))
add("ex-mascara",   "citrina", graphic("mask","cientos de máscaras", 15))
add("ex-atopico",   "zafiro",  wool(["NI UTÓPICO","NI DISTÓPICO","ATÓPICO"], 24))
add("ex-disgregacion","amatista",freedom([("la",18,0,0,0),("dis",30,-4,-8,-6),("gre",30,2,4,4),("gación",30,4,10,-3)]))
add("ex-museo",     "zafiro",  invert(["un museo","que nunca","visitaremos"], 20))
add("ex-marchita",  "citrina", smear("la obra se marchita", 5, 17))
add("ex-ruinas",    "amatista",column("Construimos pensando en las ruinas, la llegada del moho, y su inevitable abandono.", 13, kicker="10"), pw=168)
add("ex-mejora",    "zafiro",  wool(["LA OBRA MEJORA","SI ESTÁ","FUERA DE LUGAR"], 20))
add("ex-asilo2",    "citrina", smear("una solicitud de asilo", 5, 16))

# C · EXTRAS modernos / editoriales (~16)
add("xt-coord",     "zafiro",  pin("aquí, en ningún sitio","41°N · sin lugar"))
add("xt-sitenosite","citrina", invert(["lugar","· no-lugar"], 26))
add("xt-deriva",    "amatista",derive("la deriva — el extravío"))
add("xt-const-cfdl","zafiro",  constellation(["C","F","D","L","fuera","de","lugar"], 17))
add("xt-wool-cfdl", "citrina", wool(["C.F.D.L."], 56))
add("xt-syll-exilio","zafiro",  syllables(["e","xi","lio"], 52))
add("xt-invert-exilio","amatista",invert(["exilio","y destierro"], 26))
add("xt-fade-inmutable","citrina",fade(["lo inmutable","inmutable","mutable","…"], 30))
add("xt-rep-comunes","zafiro", repeat_texture("lugar común", 16, 13))
add("xt-offgrid-extempo","caramelo",offgrid("extem","poráneo", 30, dy=-14))
add("xt-mir-destierro","zafiro", mirror("destierro", 38))
add("xt-bracket-deforme","citrina",bracket("deforme", 50))
add("xt-truism-museo","amatista",truism(["un museo que","nunca visitaremos"], 15))
add("xt-cat-molsa", "zafiro",  wool(["L'ARRIBADA","DE LA MOLSA"], 24))
add("xt-cat-atopic","citrina", bracket("allò atòpic", 36))
add("xt-derive-asilo","zafiro", derive("el viaje como asilo"))

# ---- emit --------------------------------------------------------------
PAGE='''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>C.F.D.L. — {slug}</title>
<link rel="stylesheet" href="_shared.css"><style>{style}</style></head>
<body><div class="stage {g}" style="--ink:{ink};--accent:{accent};--field:{field};--bar:{bar};--tagcol:{tag}">
<div class="print {cls}" style="{pstyle}">{inner}</div></div></body></html>'''

def main():
    for f in glob.glob(os.path.join(SRC,"*.html")):
        os.remove(f)
    avail_black = os.path.exists(os.path.join(os.path.dirname(__file__),"assets","tee-black.jpg"))
    n=0
    for i,d in enumerate(D,1):
        if d["slug"] in REMOVE: continue
        p=PAL[d["pal"]]
        if p["g"]=="black" and not avail_black: continue
        ps=[]
        px = d["px"] if d["px"] is not None else CORR.get(d["slug"])
        if d["pw"] is not None: ps.append(f'--pw:{d["pw"]}px')
        if px is not None: ps.append(f'--px:{px}')
        if d["py"] is not None: ps.append(f'--py:{d["py"]}')
        html=PAGE.format(slug=d["slug"], style=STYLE, g=p["g"], ink=p["ink"], accent=p["accent"],
                         field=p["field"], bar=p["bar"], tag=p["tag"], cls=d["cls"],
                         pstyle=';'.join(ps), inner=d["inner"])
        open(os.path.join(SRC,f'{i:03d}-{d["slug"]}.html'),"w",encoding="utf-8").write(html)
        n+=1
    print(f"wrote {n} design html files")

if __name__=="__main__":
    main()
