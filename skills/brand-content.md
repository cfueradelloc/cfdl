---
name: brand-content
description: Generate or rewrite content in C.F.D.L.'s voice and visual identity, and apply visual branding to images. Use this when writing event descriptions, social posts, press copy, artwork blurbs, or converting images to the collective's visual style.
---

## C.F.D.L. Brand Guidelines

<!-- Update this section as the collective's identity evolves -->

**Name:** C.F.D.L. — Colectivo Fuera de Lugar (ES) / Col·lectiu Fora de Lloc (CA)

**Brand color:** #ffb923 (golden amber, RGB 255 185 35)

**Typography:**
- Primary: Futura Std Book — `skills/references/typography/FuturaStd-Book.otf`
- Secondary: Minion Pro Regular — `skills/references/typography/MinionPro-Regular.otf`

When generating any code that renders text (HTML, CSS, p5.js, etc.), always load these fonts via `@font-face` from the paths above (adjust relative path based on output location). Never substitute with system fonts, Google Fonts, or other typefaces. Example:

```css
@font-face {
    font-family: 'FuturaStd';
    src: url('../skills/references/typography/FuturaStd-Book.otf') format('opentype');
}
@font-face {
    font-family: 'MinionPro';
    src: url('../skills/references/typography/MinionPro-Regular.otf') format('opentype');
}
```

Use `FuturaStd` for body text and UI; `MinionPro` for titles and display text.

**Visual style:** Black and white photography with well-adjusted contrast

**Website:** https://cfdl.site

**Social:** Instagram @cfueradelloc

**Languages:** Spanish and Catalan (default to these; use English only if explicitly requested)

**Voice:** Concise and bold, playful but serious

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

## Extended Color Palette

A modern, harmonious palette centered on Citrina (#ffb923), spanning warm to cold. Named in Spanish. Use beyond the single brand color when visual work calls for richer tone.

| Nombre | Hex | RGB | Temperatura |
|--------|-----|-----|-------------|
| Cera | `#fff4d6` | 255 244 214 | cálida |
| Sol | `#ffd25a` | 255 210 90 | cálida |
| **Citrina** *(marca)* | **`#ffb923`** | 255 185 35 | **ancla** |
| Azafrán | `#c07d00` | 192 125 0 | cálida |
| Resina | `#6b4200` | 107 66 0 | cálida |
| Niebla | `#e8edf0` | 232 237 240 | fría |
| Salvia | `#7d9e92` | 125 158 146 | fría |
| Pizarra | `#4a6880` | 74 104 128 | fría |
| Medianoche | `#1a2e3d` | 26 46 61 | fría |

**Uso:** Cera y Niebla para fondos suaves; Sol y Citrina para acentos activos; Azafrán y Resina para textura oscura cálida; Salvia y Pizarra como fríos contemporáneos; Medianoche como negro alternativo con temperatura.

**Combinaciones recomendadas:**
- *Editorial*: Niebla + Citrina + Medianoche — frío, limpio, acento de color
- *Cálida*: Cera + Azafrán + Resina — amarillo pergamino, profundidad de ámbar
- *Contraste*: Citrina + Pizarra — complementario dividido, muy contemporáneo
- *Terrosa*: Salvia + Resina + Sol — naturaleza, pigmento, sin estridencias

---

## Visual Output Standards

Inspired by the design language of Frieze, e-flux, Mousse, MoMA, Tate, and MACBA. Apply these to every HTML, CSS, or visual output.

### Design tokens

```css
--bg:      #fafaf8;   /* warm near-white — page background */
--surface: #ffffff;   /* white — sidebar / card backgrounds */
--text:    #0f0f0e;   /* near-black — all body text */
--muted:   #6b6b65;   /* medium gray — labels, secondary text */
--border:  #e5e4df;   /* subtle warm gray — borders, dividers */
--accent:  #ffb923;   /* C.F.D.L. amber — interactive elements only */
```

### Typography

```css
@font-face {
    font-family: 'FuturaStd';
    src: url('[path]/skills/references/typography/FuturaStd-Book.otf') format('opentype');
}
@font-face {
    font-family: 'MinionPro';
    src: url('[path]/skills/references/typography/MinionPro-Regular.otf') format('opentype');
}
```

- **FuturaStd** — UI, labels, buttons, body text. Uppercase + tracked for labels (10px, 0.1em).
- **MinionPro** — titles, display text, editorial headings.
- Never substitute with Google Fonts, system fonts, or other typefaces.

### Color rules

- `--accent` (#ffb923) appears **only** on interactive elements: slider thumbs, active buttons, focus rings.
- Never use amber as a background for UI chrome. It may be used as a canvas background when deliberately mirroring the printed manifesto.
- No Anthropic palette (orange `#d97757`, blue `#6a9bcc`, green `#788c5d`).

### Layout & spacing

- Sidebar: white surface, `1px solid var(--border)`, `border-radius: 4px`, no blur, no heavy shadow.
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

Using the brand guidelines above, take the content provided by the user and:

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
