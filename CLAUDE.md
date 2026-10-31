# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

The website and working tools of **C.F.D.L.** — *Colectivo Fuera de Lugar · Col·lectiu Fora de
Lloc* (<https://github.com/cfueradelloc>), an arts collective: reading clubs, recitals, screenings,
and a thread of generative art. Plain HTML, no build step, served by GitHub Pages.

## Layout

Four folders, one job each. Only `docs/` is published.

| Folder | Job |
|---|---|
| `docs/` | **The website.** Pages (`index`, `manifiesto`, `eventos`, `proyectos`, `galeria`) at the root; `assets/` (css, js, fonts, logo, images, the manifesto PDF); `gallery/` (event photos + `sm/` thumbnails); `output/` (p5.js pieces, one self-contained HTML each). All links relative. |
| `content/` | **Source of truth for the site** (not served): `events/calendario-eventos.md` and `SOURCES.md` (each site section → its raw material in Drive). Edit here first, then reflect into `docs/`. |
| `studio/` | **Generators of artwork, not pages.** Each has a `README.md`; scripts at its root, inputs in `assets/`, generated files in `src/` and `out/`. `tshirts/` (shirt mockups: `build_designs.py` → `src/` → `render.sh` → `out/`), `instagram/` (1080×1350 posts + captions, see the `instagram-post` skill), `brand/` (logo proposal, not adopted yet), `palette/` (the single palette; `paleta.py` generates the tokens others import). |
| `skills/` | Claude Code skills: `brand-content`, `algorithmic-art`, `instagram-post`, `instagram-archive`. |

`scripts/link-drive.sh` links the Drive-hosted folders (see below). `README.md` is the public overview.

## Deployment & git

- GitHub Pages, deploy from branch `main`, source **`/docs`** (repo `cfueradelloc/cfdl`).
  `docs/.nojekyll` disables Jekyll. A custom-domain `CNAME` would also go in `docs/` (none today).
- **Commit and push directly to `main`** — solo project, authorized by the user. Pushing publishes the site.
- After moving or renaming anything, grep for the old path across the repo and fix every reference.

## Google Drive

The collective's working material (manifesto translations, branding, posters, admin, photos) lives
in Google Drive, not in the repo. **Synchronization with Drive matters to the user.**

- **Full CFDL folder** — ID `1uC9dE92peUs_G2lHoZCsJz3cjdPj9cHo`
  (<https://drive.google.com/drive/folders/1uC9dE92peUs_G2lHoZCsJz3cjdPj9cHo>), synced locally (personal
  account miquelduranfrigola@gmail.com) at:
  ```
  /Users/mduranfrigola/Library/CloudStorage/GoogleDrive-miquelduranfrigola@gmail.com/My Drive/Documents/Writing/CFDL
  ```
- **Default to the local path** — it *is* Drive; whatever is written there syncs. Use the **Google Drive
  connector whenever it is necessary** (lookups by ID, files not yet downloaded, sharing). The connector
  is authenticated as miquel@ersilia.io, where CFDL appears as a *shortcut*; resolve the original folder
  ID if it returns the pointer instead of the contents. Say so when you use it.
- Match a Drive ID to a local folder without the connector:
  `xattr -p 'com.google.drivefs.item-id#S' <folder>`.

### Gitignored repo material → `CFDL/Contenido/GitHub`

ID `1EVYkA-xXSs8MvOCG6Lb829JxtX6RQZX5`
(<https://drive.google.com/drive/folders/1EVYkA-xXSs8MvOCG6Lb829JxtX6RQZX5>). Whatever the repo
produces or needs but does not version lives here, at the same relative path; in the repo each such
path is a **symlink into Drive**, listed in `.gitignore`. Generators write through the link and Drive
syncs on its own. Currently: `studio/tshirts/out`, `studio/tshirts/assets/photos`,
`studio/tshirts/assets/Manifesto_Fuera_De_Lugar.pdf`, `studio/instagram/out`,
`studio/instagram/assets/{retratos,portadas}`, `studio/brand/{bocetos,png}`.

- Fresh clone or new machine: run **`scripts/link-drive.sh`**.
- Moving something new to Drive: add it to `PATHS` in the script and to `.gitignore`,
  `git rm -r --cached` it, run the script (it copies, verifies, and only then replaces with a link).
- Photos of real people and raw source material go here, never in git — the repo is public.

### Drive folder structure (`…/Writing/CFDL`)

- `Administracion/` — registration, tax (Agencia Tributaria), meeting notes (`Reuniones`).
- `Branding/` — logo, favicon (PNG/PDF/JPEG), brand assets.
- `Contenido/` — `Manifiesto/` (ES, CA, EN, DE, FR, PT, AST, plus `Fotos/`), `Proyectos/`,
  `Miscelanea/`, and `GitHub/` (above).
- `Eventos/` — per cycle (*Almíbar Off*, *En Voz Alta*, *La Perecquiana*…): posters in `Carteles/`,
  portraits and covers per author, the events spreadsheet.
- `Instagram/` — archive of @cfueradelloc written by the `instagram-archive` skill. Not edited by hand.
- `Seleccion/` — selected event photos.

## Conventions

- Site copy is in **Spanish**; follow *Writing style* below.
- Keep the plain-HTML, no-build-step approach. Generative pieces use **p5.js with seeded randomness**
  (`algorithmic-art` skill) and live as self-contained HTML in `docs/output/`.
- Colours come from `studio/palette/`; never hand-write a new hex.
- **Events:** `content/events/calendario-eventos.md` is the single source of truth; `docs/eventos.html`
  only renders it. Update the markdown first (chronological, full dates, cycle noted per entry), then
  derive the page — one entry per event with its day, the cycle as a tag, full month names. Never
  invent or edit events directly in the HTML.

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
