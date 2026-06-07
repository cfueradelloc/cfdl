# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

`cfdl` is the static website **and** Claude Code skills collection for **C.F.D.L.**
(Cooperativa / colectivo artístico — see <https://github.com/cfueradelloc>), an arts
collective. The site is plain HTML deployed via GitHub Pages (`.nojekyll` present).

### Repo layout
The repo root separates **the served website** (`docs/`) from **project material** (`content/`, `skills/`).

- `docs/` — **the deployable website** (everything served). Contains:
  - `index.html`, `manifiesto.html`, `proyectos.html`, `eventos.html`, `galeria.html` — site pages (Spanish).
  - `assets/` — fonts (FuturaStd, MinionPro), `logo/` (favicon), `images/` (manifesto imagery),
    `docs/` (downloadable manifesto PDF). Pages reference these via `assets/…`; `output/` pieces via `../assets/…`.
  - `gallery/` — published image assets (e.g. the *En voz alta* photo series), used by `galeria.html`.
  - `output/` — generative-art pieces (p5.js), one HTML each (`garganta.html`, `maleza.html`,
    `moho.html`, `disgregacion.html`, `brujula.html`, `paleta.html`, `manifiesto-animado.html`).
  - `.nojekyll` — disables Jekyll on the published site.
- `content/` — **source of truth for updating the site** (NOT served): `events/calendario-eventos.md`
  (canonical events list) and `SOURCES.md` (maps each site section → its raw material in Drive).
  Edit here, then reflect changes into the pages under `docs/`.
- `skills/` — Claude Code skills (NOT served), each a folder with a `SKILL.md`: `brand-content/`
  (+ `references/` for colorplan and manifesto sources) and `algorithmic-art/`.
- `README.md` — overview of the skills.

### Deployment
Classic **GitHub Pages**, deploy-from-branch — repo `github.com/cfueradelloc/cfdl`. The Pages
**source must be set to `/docs`** (Settings → Pages). The whole site lives under `docs/`, all
links are relative, and `.nojekyll` sits inside `docs/`. If a custom domain (cfdl.site) is used,
its `CNAME` file also belongs in `docs/`. The site no longer depends on the `skills/` path for any
asset. If you move folders, update the references and re-run the grep in the verification below.

## Source material lives in Google Drive — use the LOCAL synced copy

The collective's working material (manifesto translations, branding assets, event
posters, admin docs, photos) is **not** in this repo. It lives in Google Drive.

**Always access it through the locally synced folder, NOT via the MCP/connector.**

Canonical local path:

```
/Users/mduranfrigola/Library/CloudStorage/GoogleDrive-miquelduranfrigola@gmail.com/My Drive/Documents/Writing/CFDL
```

This is synced from the **miquelduranfrigola@gmail.com** (personal) Google Drive.
Reading/writing the local synced files is faster and is the user's preferred workflow,
so **default to the local path above**.

### Backup: Google Drive connector (MCP)
A shortcut to the same CFDL folder also exists in the **miquel@ersilia.io** Drive, which
is what the Google Drive *connector* (MCP) is authenticated against (the active session
email). Use the connector **only as a fallback** — e.g. if the local sync is stale,
missing, or the file hasn't downloaded yet — and prefer it for read-only lookups.
Note: it points at a *shortcut*, so the connector may surface the shortcut pointer rather
than the folder contents; resolving the original folder ID can help. Always tell the user
when you fall back to the connector instead of the local copy.

### Drive folder structure (`…/Writing/CFDL`)
- `Administracion/` — registration, tax (Agencia Tributaria), meeting notes (Reuniones).
- `Branding/` — logo, favicon (PNG/PDF/JPEG), brand assets.
- `Contenido/` — content, incl. `Manifiesto/` in many languages (Español, Català,
  English, Deutsch, Français, Português, Asturiano) and `Manifiesto/Fotos/`.
- `Eventos/` — events such as *Almíbar Off*, *En Voz Alta*, *La Perecquiana*; posters
  (`Carteles/`) and an events calendar spreadsheet.

The repo is, in effect, the *published* surface; the Drive folder is the *source* of
truth for raw content and assets.

## Conventions
- Site content is in **Spanish**; match existing tone and language on pages.
- Generative-art pieces use **p5.js with seeded randomness** (see the `algorithmic-art`
  skill) and live as self-contained HTML files in `output/`.
- Keep new pages consistent with the existing plain-HTML, no-build-step approach.

## Writing style — C.F.D.L. voice

These rules are distilled from the live corpus (`manifiesto.html`, event titles in
`eventos.html`, piece descriptions in `proyectos.html`, captions in `galeria.html`).
Apply them to **all** new copy — page text, event/piece titles, captions, social posts,
press. They extend, and take precedence over, the looser **Voice** note in
`skills/brand-content/SKILL.md`. When in doubt, mine the manifesto.

### Voice & grammar
- **First person plural, present indicative.** The collective speaks as *nosotros*, never
  as a named individual (embrace *marca blanca*, no personal brand). Manifesto-register
  sentences open with a declarative collective verb: *Escogemos, Reivindicamos, Defendemos,
  Buscamos, Invocamos, Aspiramos, Celebramos, Proponemos, Construimos, Creemos, Usamos.*
- **Declarative, never promotional.** No questions, no hedging (*quizás*, *tal vez*), no
  marketing imperatives or calls to action (*¡Únete!*, *Descubre*, *No te lo pierdas*),
  no exclamation marks, no emoji.
- Assertive and a little severe — *concise and bold, playful but serious*.

### Register & rhetoric
- **Elevated, literary, slightly archaic lexicon:** *extenuación, dispendio, ofuscación,
  enajenación, heterodoxia, atópico, venero, náufrago, extemporáneo, abnegado.* Prefer the
  denser word.
- **Antithesis / oxymoron is the signature device.** Build phrases on a tension between two
  opposed terms: *"la libertad perdida a posta", "resucitar en vida", "esperanza voraz",
  "nostalgia atroz", "avanzar a favor, y no en contra, de la angustia", "marca blanca"*
  against *"marca personal".*
- **Triads and asyndeton.** Enumerate in threes, often without a conjunction: *"de la
  palabra, de los recursos, de la energía corporal"; "el plagio, la copia, la búsqueda
  promiscua".*
- **Embrace the unfinished, deformed, out-of-place.** Avoid any word that signals polish,
  resolution, completion, productivity, moderation, or institutional/corporate tone.

### Punctuation & typography
- The **em dash (—), spaced**, is the house connective — in titles, meta lines, and
  technical descriptions. Never the hyphen-minus, never `" - "`.
- Use the **colon** to open an expansion or enumeration: *"Buscamos la extenuación: de la
  palabra…".*
- **Titles & display text:** sentence case (lowercase initial except the first word and
  proper nouns), set in italic serif. Do **not** Title-Case.
- **Labels, meta, nav, footers:** leave source text in normal case — the CSS
  (`text-transform: uppercase` + letter-spacing) does the uppercasing. Don't hard-uppercase
  in the HTML.

### Naming events, pieces, exhibitions
- **Titles are lifted verbatim or near-verbatim from the manifesto.** Existing examples:
  *"Crear donde no alcance ninguna raíz", "La fractura profiláctica", "Ante la síntesis,
  la disgregación", "Brújula sin imán", "Nostalgia atroz", "La llegada del moho", "Atopia".*
  Need a new title? Mine a manifesto fragment first.
- **Event meta line:** `Tipo — Lugar, Ciudad` (capitalized *Tipo*, spaced em dash).
  E.g. *"Exposición colectiva — Sala d'Art Jove, Barcelona".*
- **Generative-piece description:** `Técnica — detalle`.
  E.g. *"Campo vectorial — ruido curl con tres especies de partículas".*

### Gallery captions
- Very short (1–4 words), **lowercase**, fragmentary and observational, no final period:
  *"entre libros", "tomando la palabra", "la voz", "pausa", "escucha".* Proper names keep
  their capitals (*"Ángela Mallén"*).

### Bilingualism
- **Spanish is primary; Catalan is the co-equal second language** — the collective signs
  *"Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc"* (middle dot `·` between the two).
  The manifesto also exists in EN / FR / AST / PT. Default to Spanish for new copy; mirror
  it in Catalan on bilingual chrome (footers, brand lines). Use other languages only on
  request.

### Motif vocabulary (draw titles & copy from here)
*exilio · destierro · fuera de lugar · brújula sin imán · maleza · garganta sin fondo ·
moho · ruinas · disgregación · marca blanca · atópico · extenuación · suicidio creativo ·
fractura profiláctica · náufrago.*
