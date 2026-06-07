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

The raw material behind the site (events calendar, source notes) lives in `content/`; the fonts,
logo and images it serves live in `docs/assets/`.

## Skills

The `skills/` folder holds two Claude Code skills:

- **brand-content** — write or rewrite copy in the collective's voice, and convert images to its style.
- **algorithmic-art** — build generative p5.js pieces with seeded randomness.

To use one, point Claude Code at this `skills/` directory or copy a skill folder into your own
project's `.claude/skills/`.

## Contributing

Conventions, deployment, and where the source material lives are documented in `CLAUDE.md`.
