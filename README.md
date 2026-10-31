# C.F.D.L.

**Colectivo Fuera de Lugar** · *Col·lectiu Fora de Lloc* — an arts collective: reading clubs,
recitals, film screenings and talks, alongside a thread of generative art.
This repository holds its website and the tools used to make its artwork.

**https://cfdl.site** · [@cfueradelloc](https://www.instagram.com/cfueradelloc/)

## The site

Hand-written HTML, no build step, served from `docs/` by GitHub Pages.

- **Manifiesto** — the manifesto, in six languages.
- **Eventos** — what is coming and what already happened.
- **Proyectos** — generative pieces made with p5.js.
- **Galería** — photographs from the events.

To preview it locally: `python3 -m http.server -d docs` and open <http://localhost:8000>.

## Layout

| Folder | What it holds |
|---|---|
| `docs/` | The website — the only folder that gets published. |
| `content/` | The site's source of truth: the events calendar and a map of sources in Drive. |
| `studio/` | Generators of artwork rather than pages: `tshirts/`, `instagram/`, `brand/` (a logo proposal), `palette/` (the single colour palette). Each has its own README. |
| `skills/` | Claude Code skills, below. |
| `scripts/` | `link-drive.sh` — see below. |

**Renders, photos and sketches are not in git.** They live in the collective's Google Drive
(`CFDL/Contenido/GitHub`) and appear in the repo as symlinks. After cloning, run
`scripts/link-drive.sh` to recreate them (it needs Google Drive for desktop and access to that folder).

## Skills

- **brand-content** — write or rewrite copy in the collective's voice; convert images to its style.
- **algorithmic-art** — build generative p5.js pieces with seeded randomness.
- **instagram-post** — turn a calendar entry into an Instagram announcement and its caption.
- **instagram-archive** — download everything @cfueradelloc has published into the Drive.

To use one elsewhere, copy or symlink its folder into a project's `.claude/skills/` (or `~/.claude/skills/`).

## Contributing

Conventions, the house writing style, deployment and the Drive setup are in [`CLAUDE.md`](CLAUDE.md).
