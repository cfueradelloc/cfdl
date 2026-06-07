# GF Smith Colorplan — Reference Palette

Digital hex approximations of the Colorplan paper range. GF Smith does not publish official hex values; these are widely used community equivalents.

## Full Palette

| Color Name | Hex |
|---|---|
| Adriatic | #50789e |
| Amethyst | #3c3048 |
| Azure Blue | #b7c4d5 |
| Bagdad Brown | #4b3c34 |
| Bitter Chocolate | #3e3535 |
| Bright Red | #be4346 |
| Bright White | #e4e4e4 |
| Candy Pink | #e2bdc4 |
| China White | #e4d3c3 |
| Citrine | #e9ad51 |
| Claret | #4d2f37 |
| Cobalt | #4d5971 |
| Cool Blue | #d0d0d8 |
| Cool Grey | #d4d1d8 |
| Dark Grey | #5d5d5b |
| Ebony | #2e2e30 |
| Emerald | #6e988a |
| Factory Yellow | #edd468 |
| Forest | #405944 |
| Fuchsia Pink | #c1659a |
| Harvest | #b29981 |
| Hot Pink | #e84a73 |
| Imperial Blue | #2e3a4b |
| Lavender | #c0aed4 |
| Lockwood Green | #538055 |
| Mandarin | #e37a4e |
| Marrs Green | #288d84 |
| Mid Green | #909880 |
| Mist | #ddd4cb |
| Natural | #dad5d5 |
| New Blue | #889dbc |
| Pale Grey | #cbcbcb |
| Park Green | #b4d7b8 |
| Pistachio | #d4dec6 |
| Powder Green | #d3dbcd |
| Pristine White | #e1e1e1 |
| Purple | #775e9e |
| Racing Green | #495a59 |
| Real Grey | #aeaeae |
| Rust | #dc7448 |
| Sapphire | #445d87 |
| Scarlet | #85383e |
| Slate | #374247 |
| Smoke | #8f8f91 |
| Stone | #d4bdac |
| Tabriz Blue | #4c9bca |
| Turquoise | #8fd3d5 |
| Vellum White | #ded9d6 |
| Vermillion | #a1373b |
| White Frost | #dedfe3 |

## CFDL Active Subset — as shipped on the live site

The live site (and every generative piece in `docs/output/`) uses a **saturated**
take on the Colorplan tones: brighter, higher-contrast hex than the paper swatches
above. These exact values are the source of truth — match them, don't soften them.

```css
:root {
    --bg:      #f8ccce; /* Candy Pink   — page background (light pages)   */
    --surface: #bbabd5; /* Lavender     — sidebars / cards                */
    --text:    #332f8a; /* Sapphire     — body text, dark bands           */
    --muted:   #857c75; /* Smoke        — secondary text on light ground  */
    --border:  #c8b8d8; /* lavender-pink — borders, dividers              */
    --accent:  #fde700; /* Factory Yellow — interactive accents           */
}
```

The **manifiesto** page inverts this (Sapphire ground, Candy Pink text). On the
Sapphire dark bands (header/footer, manifiesto body) secondary text is lightened to
`#b0a8e0` for WCAG contrast. The shared implementation lives in
`docs/assets/css/base.css` (tokens + `body.theme-dark`) and `docs/assets/css/viewer.css`.

> Earlier docs listed a muted paper subset (Mist / Ebony / Citrine) and an amber
> editorial palette (`#fafaf8` / `#ffb923`). Neither is shipped — the saturated set
> above is the real identity.
