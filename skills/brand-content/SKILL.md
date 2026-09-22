---
name: brand-content
description: Generate or rewrite content in C.F.D.L.'s voice and visual identity, and apply visual branding to images. Use this when writing event descriptions, social posts, press copy, artwork blurbs, or converting images to the collective's visual style.
---

## C.F.D.L. Brand Guidelines

<!-- Update this section as the collective's identity evolves -->

**Name:** C.F.D.L. — Colectivo Fuera de Lugar (ES) / Col·lectiu Fora de Lloc (CA)

**Brand colors (as shipped):** one palette, thirteen tones — six neutrals, five colours, two for use on dark. Ámbar `#ffb923` and Zafiro `#332f8a` carry the identity; the ground is Papel `#fdf5eb`. **`content/paleta/` is the single source of truth** — `python3 paleta.py` lists it, `--verificar` checks the contrasts, `--css` emits the tokens. Never hand-write a hex; read it from there. See *Visual Output Standards* below.

**Typography:**
- Primary: Futura Std Book — `assets/fonts/FuturaStd-Book.otf`
- Secondary: Minion Pro Regular — `assets/fonts/MinionPro-Regular.otf`

The fonts live under the site's `assets/fonts/` folder (the site root is `docs/`). When generating any code that renders text (HTML, CSS, p5.js, etc.), always load these fonts via `@font-face` from those paths (adjust the relative prefix based on output location — e.g. `assets/fonts/…` from a page at the site root, `../assets/fonts/…` from `output/`). Never substitute with system fonts, Google Fonts, or other typefaces. Example (from a page at the site root):

```css
@font-face {
    font-family: 'FuturaStd';
    src: url('assets/fonts/FuturaStd-Book.otf') format('opentype');
}
@font-face {
    font-family: 'MinionPro';
    src: url('assets/fonts/MinionPro-Regular.otf') format('opentype');
}
```

Use `FuturaStd` for body text and UI; `MinionPro` for titles and display text.

**Visual style:** Black and white photography with well-adjusted contrast

**Website:** https://cfdl.site

**Social:** Instagram @cfueradelloc

**Languages:** Spanish and Catalan (default to these; use English only if explicitly requested)

**Voice:** Concise and bold, playful but serious. First person plural (*nosotros*),
declarative, literary, never promotional. **The full writing-style rules are canonical
in `CLAUDE.md` ("Writing style — C.F.D.L. voice") — read and apply them before writing or
rewriting any Spanish copy.** The key themes and avoid-list below feed that voice.

**Key themes:**
- Exile, displacement, being out of place as the ideal condition
- Cities always under construction, on terrain where they shouldn't be
- Creation as asylum-seeking; travel as frustrating and unproductive
- Unfinished and deformed work as a goal, not a failure
- Creative suicide as a routine act; immaturity as purpose
- Excess over moderation; exhaustion of words, resources, energy
- Opacity over empathy; tolerance through strangeness, not understanding
- Plagiarism and copying as legitimate creative method
- Building while thinking of ruins and inevitable abandonment
- Work improves when it is out of place

**Avoid:** Personal brand (embrace "marca blanca"), coherence, moderation, productivity, polished or finished feel, corporate or institutional tone, anything that signals resolution or completion

---

## The Palette

**Source of truth: `content/paleta/`.** Do not copy these values into new code — import
them (`from paleta import HEX`) or generate the tokens (`python3 paleta.py --css`). They
used to live in eleven places at once, which is how the collective ended up with two
palettes that did not speak to each other.

| token | hex | papel |
|---|---|---|
| `papel` | `#fdf5eb` | fondo de página |
| `hueso` | `#f1e7db` | superficie levantada sobre el papel |
| `filete` | `#e0d6ca` | borde, separador, filete |
| `ceniza` | `#a89f96` | inactivo, rejilla, filete fuerte |
| `humo` | `#6a625a` | texto secundario sobre claro |
| `tinta` | `#171513` | texto principal |
| `ámbar` | `#ffb923` | ancla: campo, marca, acento |
| `rosa` | `#f8ccce` | el puente: bandas y tintes |
| `zafiro` | `#332f8a` | la nota ajena: texto y bandas oscuras |
| `moho` | `#1b5033` | banda de ciclo |
| `náufrago` | `#004d5f` | banda de ciclo |
| `cera` | `#fff4d6` | tinta clara sobre fondo oscuro |
| `lavanda` | `#bbabd5` | secundario sobre zafiro |

**Six neutrals is deliberate.** An earlier cut had seven chromatics and three neutrals,
which is backwards: the greys do the quiet work — grounds, surfaces, borders, states — and
without them you reach for colour for everything, so a card ends up pink and a border
lavender. They sit at the amber hue with chroma 6–7, so they read as greys — but greys
belonging to the same paper, not the cold factory grey that goes blue over a warm ground.

**Five colours, not three**, because there are three cycles and the ámbar belongs to the
collective, not to one of them. `ámbar` and `zafiro` are the collective; `rosa`, `moho`
and `náufrago` are the cycle bands.

### Two rules that come from measurement, not taste

- **Ámbar cannot be the focus ring on a light ground.** It gives 1.59:1 on papel and
  disappears. Focus goes in zafiro. A light tone lends its darkened version
  (`TONOS['ámbar']['acento']` = `#714a00`, 7.25:1) wherever the accent
  carries text.
- **`ceniza` does not reach the 3:1 non-text minimum** (2.41:1), and that is correct: its
  job is inactive states and decorative rules, which the guideline exempts. A border that
  *must* be seen uses `humo`.

### Retired, with the measured reason

`#fde700` Factory Yellow — 1.36:1 against ámbar, two yellows 17° apart that cannot be told
apart by value. `#1a2e3d` Medianoche, `#4a6880` Pizarra, `#e8edf0` Niebla — the cold blue
branch (h 241–256°) competing with zafiro (h 301°). `#ffd25a` Sol, `#6b4200` Resina,
`#7d9e92` Salvia — leftover steps with no job. `#c07d00` Azafrán — a fourth warm chromatic
made redundant by the neutral ramp. `#857c75` Smoke — 3.78:1 as secondary text, below the
legible minimum, and shipped that way for a long time. `#c8b8d8` lavender-pink — a border
should be a grey, not a colour. `#e9ad51` — a third value for the same idea.

---

## Visual Output Standards

Inspired by the design language of Frieze, e-flux, Mousse, MoMA, Tate, and MACBA. Apply these to every HTML, CSS, or visual output.

### Design tokens

The live identity is the single palette in `content/paleta/`. These are the exact tokens
shipped on the site and in every `docs/output/` piece; the shared source is
`docs/assets/css/base.css` (site) and `viewer.css` (pieces), both of which take their
values from `content/paleta/`.

```css
--bg:        #fdf5eb;   /* papel   — page background                  */
--surface:   #f1e7db;   /* hueso   — sidebar / card backgrounds       */
--text:      #171513;   /* tinta   — body text                        */
--muted:     #6a625a;   /* humo    — secondary text on light ground   */
--border:    #e0d6ca;   /* filete  — borders, dividers                */
--rule:      #e0d6ca;   /* filete  — hairlines                        */
--accent:    #ffb923;   /* ámbar   — fills, large marks               */
--accent-fg: #714a00;   /* ámbar darkened — accent as TEXT or focus   */
--band-bg:   #332f8a;   /* zafiro  — header, footer, dark bands       */
--band-fg:   #fff4d6;   /* cera    — light ink on the band            */
```

**The accent is two tokens, and that is not redundancy.** Ámbar on papel is 1.59:1: it
works as a fill and a rule, never as letters or a focus ring. `--accent-fg` is the same
amber darkened to 7.25:1. On zafiro the distinction collapses — amber reads there (6.38:1)
— so both hold the same value in the dark block.

The **manifiesto** inverts this (zafiro ground, cera text — `body.theme-dark`).
On zafiro bands, secondary text is `#bbabd5` (lavanda, 5.17:1).

### Typography

```css
@font-face {
    font-family: 'FuturaStd';
    src: url('[path]/assets/fonts/FuturaStd-Book.otf') format('opentype');
}
@font-face {
    font-family: 'MinionPro';
    src: url('[path]/assets/fonts/MinionPro-Regular.otf') format('opentype');
}
```

- **FuturaStd** — UI, labels, buttons, body text. Uppercase + tracked for labels (10px, 0.1em).
- **MinionPro** — titles, display text, editorial headings.
- Never substitute with Google Fonts, system fonts, or other typefaces.

### Color rules

- `--accent` (#ffb923, ámbar) is the collective's anchor. Unlike the Factory Yellow
  it replaces, it **may** carry a large field — a whole post, a shirt, the logo's ground —
  because tinta on it gives 10.59:1. What it may not do is carry small text or a focus
  ring on a light ground: that is `--accent-fg`.
- Zafiro (`--band-bg`) and ámbar carry the identity; papel is the ground. Never place
  rosa and ámbar at equal area — they are 1.19:1 apart and one vanishes into the other.
- No Anthropic palette (orange `#d97757`, blue `#6a9bcc`, green `#788c5d`).

### Layout & spacing

- Sidebar: `var(--surface)` (hueso), `1px solid var(--border)`, `border-radius: 4px`, no blur, no heavy shadow.
- Container padding: 24px. Gap between sidebar and canvas: 24px.
- Control sections: 32px margin-bottom. Control groups: 20px. Labels: 8px below text.
- Canvas container: `border-radius: 4px`, `1px solid var(--border)`, no drop shadow.

### Animation pacing

- Measured and contemplative: 0.8s–2s for most artwork transitions.
- UI interactions (hover, focus): 0.15s ease.
- Avoid rapid flashing or aggressive motion.

---

## Tasks

### Text content

First, read the **"Writing style — C.F.D.L. voice"** section of `CLAUDE.md` — it is the
canonical source for grammar, register, punctuation (the spaced em dash —), naming
conventions, caption format, and the motif vocabulary. Then, using those rules plus the
brand guidelines above, take the content provided by the user and:

1. Rewrite or generate it in C.F.D.L.'s voice — consistent in tone, energy, and language
2. Keep it concise and purposeful; cut anything that dilutes the message
3. Present one version by default; offer an alternative only if the format warrants it (e.g. long-form vs. short-form copy)

Ask for the content brief or raw text if not provided.

### Image conversion

Convert images to C.F.D.L.'s visual style: black and white with well-adjusted contrast.

```bash
convert INPUT -colorspace Gray -normalize -contrast-stretch 2%x2% OUTPUT
```

- Save output as `FILENAME_bw.EXT` in the same directory, preserving the original
- For batch conversion: `for f in FOLDER/*.jpg; do convert "$f" -colorspace Gray -normalize -contrast-stretch 2%x2% "${f%.jpg}_bw.jpg"; done`
- If ImageMagick is not installed: `brew install imagemagick`
- If the result feels too harsh or too flat, adjust the `contrast-stretch` percentage
