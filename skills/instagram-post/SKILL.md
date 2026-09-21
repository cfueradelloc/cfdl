---
name: instagram-post
description: Create an Instagram post for C.F.D.L. — an event, a cycle, a reminder, a manifesto quote, a post-event recap, a generative piece — as an image (or carousel) plus its Spanish caption, in 4:5, 1:1 or 9:16. Use this when asked to announce an event on Instagram, make a poster or cartel for @cfueradelloc, prepare a social post or story for the collective, or turn a calendar entry into an image.
---

Turns an event into **an image and a text** — a post is always both — using
`content/instagram/`. The script is deterministic; the judgement is yours.

## 1. Get the facts from the calendar, not from memory

`content/events/calendario-eventos.md` is the single source of truth for date, weekday,
time, venue and cycle. Read the entry first.

**If the event is not there, add it there first.** Announcing something the calendar does
not know about is how the two drift apart. `--verificar` warns but never auto-fills.

## 2. Decide the shape before writing any JSON

**Template** — eleven, listed with their block caps in `content/instagram/README.md`:
`evento`, `ciclo`, `recordatorio`, `cita`, `portada`, `retrato`, `programa`, `datos`,
`resumen`, `pieza`, `numero`. One runnable example of each lives in
`content/instagram/ejemplos/` — read those before inventing anything.

**How many slides.** One for a reminder or a quote. Three for an event: `portada` or
`evento`, then the text on `"superficie": "oscuro"`, then the practical details. Four for
a cycle. The block cap is enforced, because a feed image is seen at ~430 pt and the full
printed-poster inventory is illegible there.

**Format.** `feed` 1080×1350 by default. `historia` 1080×1920 for stories — note its
margins are large because Instagram's own UI covers the top and bottom. `cuadrado` when it
also goes elsewhere. `"formatos": ["feed","historia"]` renders the same brief in several.

**Theme.** `pink` is the shipped identity and the default. `citrine` when a piece
deliberately steps outside it.

**Photo.** `docs/gallery/*.jpg` is already published and safe — reference it as
`docs/gallery/<file>.jpg` (paths are resolved from the repo root). Author portraits are in
Google Drive, which currently does not serve bytes locally: copy them by hand into
`content/instagram/assets/retratos/` and check the collective may publish them. A
type-only slide always beats a bad crop. Those gallery photos are 16:9, so leave
`foto.forma` on its `banda` default rather than cropping a portrait out of a landscape.

**Logos.** `marca_cfdl` draws the collective's own mark in SVG. Other people's logos go in
`assets/logos/` and default to flat ink — see `assets/logos/README.md`. Don't switch them
to `color` unless someone actually requires it.

## 3. Write the brief

One JSON file in `content/instagram/posts/`, named `AAAA-MM-DD-slug.json`.
`posts/_ejemplo.json` lists every key. `plantilla` is the only required key in a slide;
everything else draws only if present, so omit rather than empty-string.

Write `caption.texto` and every slide's `alt`. Leave the caption out and the build emits a
`[PENDIENTE]` scaffold that the linter rejects — deliberately, because half a post is not
a post.

## 4. Copy

Read the **"Writing style — C.F.D.L. voice"** section of `CLAUDE.md` and apply it — it is
canonical for grammar, register, the spaced em dash, naming and captions.
`skills/brand-content` covers palette and typography. Don't restate those rules; follow them.

The linter mechanises part of it (no exclamation marks, no emoji, no calls to action —
including "desliza" and "link en bio" — no hyphen where an em dash belongs, no Title Case)
but it cannot tell you whether the sentence is any good. Two to four declarative sentences,
then the practical block. Hashtags are off by default and should stay off.

## 5. Build, render, look

```bash
cd content/instagram
python3 build_posts.py --lint --verificar --indice
bash render.sh
open out/index.html
```

Fix every warning before showing anything. Then actually look: `out/index.html` puts the
input JSON, the rendered PNG and the caption side by side, with the image at **430 px, the
real width in a phone feed**. *If the date is not readable there, the poster has failed*,
however good it looks at 1080.

A magenta band on a render means the page failed its own check — something left the canvas,
two zones collided, or two texts overlapped. Never ship one.

Show the user the PNG **and** the caption text. Both, every time.

## 6. Tuning is CSS, never Python

Layout lives in `content/instagram/src/_shared.css`. `open src/<id>-01.html` in a normal
Chrome tab — it is 1:1 — and edit that stylesheet in DevTools. `build_posts.py` emits
structure and data-driven custom properties; putting design decisions in it would mean a
regenerate-and-rerender cycle for every nudge.
