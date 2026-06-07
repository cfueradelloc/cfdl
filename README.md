# cfdl

The static website (plain HTML, deployed via GitHub Pages) and Claude Code skills for
[C.F.D.L.](https://github.com/cfueradelloc) — Colectivo Fuera de Lugar, an arts collective.

## Structure

```
docs/      the deployable website (GitHub Pages serves from /docs)
  *.html     site pages (index, manifiesto, proyectos, eventos, galeria)
  assets/    fonts, logo, images, docs — everything the site serves
  gallery/   published photo series used by galeria.html
  output/    generative-art pieces (p5.js), one self-contained HTML each
content/   source of truth for updating the site (events calendar, SOURCES.md)
skills/    Claude Code skills (one folder + SKILL.md each)
```

The website lives entirely under `docs/`. To update it, edit the source in `content/` and reflect
it into the relevant page in `docs/`. See `CLAUDE.md` for conventions, deployment, and the link to
the Drive source material.

## Skills

Skills live in `skills/`. To use them, point Claude Code at this repo's skills directory or
copy a skill folder into your project's `.claude/skills/`.

| Skill | Command | Description |
|-------|---------|-------------|
| Brand Content | `/brand-content` | Generate or rewrite content and convert images to C.F.D.L.'s visual style |
| Algorithmic Art | `/algorithmic-art` | Create generative art using p5.js with seeded randomness and interactive parameter exploration |
