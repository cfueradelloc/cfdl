# C.F.D.L.

**Colectivo Fuera de Lugar** (in Catalan, *Col·lectiu Fora de Lloc*) is an arts collective:
reading clubs, recitals, film screenings and conferences, alongside a thread of generative art.
This repository is its website and a couple of Claude Code skills used to build and maintain it.

Website: **https://cfdl.site**

## The site

A hand-written static site (plain HTML, no build step), served from `docs/` with GitHub Pages:

- **Manifiesto** — the collective's manifesto, in six languages.
- **Eventos** — what's coming up and what already happened.
- **Proyectos** — generative pieces made with p5.js.
- **Galería** — photographs from the events.

## Repository layout

- `docs/` — the site itself, the only folder that gets published.
- `content/` — the raw material behind the site: the events calendar and a map of sources in Drive.
- `studio/` — generators that produce artwork rather than pages: `tshirts/` (shirt mockups),
  `instagram/` (announcement images for [@cfueradelloc](https://www.instagram.com/cfueradelloc/)),
  `brand/` (a logo proposal) and `palette/` (the collective's single colour palette).
- `skills/` — Claude Code skills, below.
- `scripts/link-drive.sh` — renders, photos and sketches are not in git: they live in the
  collective's Google Drive (`CFDL/Contenido/GitHub`) and appear in the repo as symlinks.
  Run this script after cloning to recreate them.

## Skills

The `skills/` folder holds four Claude Code skills:

- **brand-content** — write or rewrite copy in the collective's voice, and convert images to its style.
- **algorithmic-art** — build generative p5.js pieces with seeded randomness.
- **instagram-post** — turn a calendar entry into an Instagram announcement and its caption.
- **instagram-archive** — download everything @cfueradelloc has published into the Drive.

To use one, point Claude Code at this `skills/` directory or copy a skill folder into your own
project's `.claude/skills/`.

## Contributing

Conventions, deployment, and where the source material lives are documented in `CLAUDE.md`.
