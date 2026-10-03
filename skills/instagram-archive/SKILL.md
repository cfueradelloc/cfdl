---
name: instagram-archive
description: Download everything @cfueradelloc has published on Instagram — posts, carousels, reels, captions, metadata and highlights — into the synced Drive folder CFDL/Instagram/, incrementally, with a chronological index.md. Use this when asked to download, back up, archive or refresh the collective's Instagram, to "bajar los posts", "archivar @cfueradelloc", or when the events calendar needs checking against what was announced on Instagram.
---

Keeps a local copy of the collective's public Instagram in the Drive, next to `Eventos/`
and `Branding/`. The media never goes into git.

## Run it

```bash
skills/instagram-archive/scripts/archive.sh chrome   # with your browser session (reliable)
skills/instagram-archive/scripts/archive.sh          # anonymous (Instagram usually refuses)
```

- **Destination:** `…/Writing/CFDL/Instagram/` (Drive root from `CLAUDE.md`; override
  with `CFDL_DRIVE`). Posts and the profile picture land in `cfueradelloc/`, highlights in
  subfolders, and `index.md` is rebuilt on every run.
- **Incremental:** `--fast-update` stops at the first post already on disk, so re-runs
  only fetch what is new. Delete a post's files to force it to download again.
- **Install once:** instaloader lives in its own venv, because the Homebrew build lacks
  `browser_cookie3` and cannot read cookies:
  `python3 -m venv ~/.local/venvs/instaloader && ~/.local/venvs/instaloader/bin/pip install instaloader browser_cookie3`

## Login

Nobody running this logs in as the collective. With a browser argument, instaloader reuses
the cookies of **your own** Instagram session in that browser (`chrome`, `safari`,
`firefox`…). That unlocks full pagination, reels and highlights. The first time,
macOS asks for Keychain access to "Chrome Safe Storage": choose Allow.

Without a browser, the run is anonymous and aborts on the first block (401/429) instead of
waiting for hours. As of October 2026, Instagram refuses anonymous profile queries outright.

## Limits, said plainly

- Only what is **still public**: expired stories and deleted posts are gone.
- Automated downloading goes against Instagram's terms. At this volume, the practical risk
  is a temporary "try again later" on your personal account. If you get a **429**, don't
  retry in a loop: instaloader waits on its own, and the next run resumes. Don't run two
  instances, and keep the Instagram app closed while it runs.
- **The complete, official archive** (stories included) can only come from whoever holds
  the @cfueradelloc login: Accounts Center → Your information and permissions → Export
  your information. If they send the zip, unpack it in `Instagram/export/`.

## After a run

Report how many posts are new, then compare `index.md` against
`content/events/calendario-eventos.md`. A dated event that appears on Instagram and is
missing from the calendar goes **into the calendar first** (see `CLAUDE.md`). Never edit
`docs/eventos.html` straight from the archive.
