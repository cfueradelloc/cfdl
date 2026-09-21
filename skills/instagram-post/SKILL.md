---
name: instagram-post
description: Create an Instagram announcement image for C.F.D.L. — an event, a cycle of events, a reminder, or a manifesto quote — as a 1080×1350 post or a carousel, with its Spanish caption. Use this when asked to announce an event on Instagram, make a poster or cartel for @cfueradelloc, prepare a social post for the collective, or turn a calendar entry into an image.
---

Turns an event into images plus a caption, using `content/instagram/`. The script is
deterministic; the judgement is yours. Work in this order.

## 1. Get the facts from the calendar, not from memory

`content/events/calendario-eventos.md` is the single source of truth for date, weekday,
time, venue and cycle. Read the entry first.

**If the event is not there, add it there first** and only then make the post. Announcing
something the calendar does not know about is how the two drift apart.

## 2. Decide the shape before writing any JSON

- **How many slides?** A single 4:5 post for a reminder or a quote. Three for an event:
  name + date + photo, then the text on a dark surface, then the practical details. Four
  for a cycle. The block cap per template is enforced by the linter, and it exists because
  a feed image is seen at ~430 pt — the full printed-poster inventory is illegible there.
- **Which template?** `evento`, `ciclo`, `recordatorio`, `cita`.
- **Which theme?** `pink` is the shipped identity and the default. Reach for `citrine`
  when a piece deliberately steps outside it.
- **Which photo?** `docs/gallery/*.jpg` is already published and safe to use; reference it
  as `../../../docs/gallery/<file>.jpg`. Author portraits live in Google Drive, which
  currently does not serve bytes locally — copy them by hand into
  `content/instagram/assets/retratos/` and check the collective may publish them. A
  type-only slide is always better than a bad crop.

## 3. Write the brief

One JSON file in `content/instagram/posts/`, named `AAAA-MM-DD-slug.json`. Copy
`posts/_ejemplo.json` — it lists every key. `plantilla` is the only required key in a
slide; everything else draws only if present, so omit rather than empty-string.

Write `caption.texto` and every slide's `alt`. If you leave the caption out the build
emits a scaffold marked `[PENDIENTE]` and the linter will fail you for it.

## 4. Copy

Read the **"Writing style — C.F.D.L. voice"** section of `CLAUDE.md` and apply it — it is
canonical for grammar, register, the spaced em dash, naming and captions. `skills/brand-content`
covers the palette and typography. Do not restate those rules; follow them.

The linter mechanises part of this (no exclamation marks, no emoji, no calls to action, no
hyphen where an em dash belongs, no Title Case) but it cannot tell you whether the sentence
is any good. Two to four declarative sentences, then the practical block.

## 5. Build, render, look

```bash
cd content/instagram
python3 build_posts.py --lint --verificar --indice
bash render.sh
open out/index.html
```

Fix every warning before showing the result. Then actually look at the contact sheet:
column one is 430 px, the real size in a feed. **If the date is not readable there, the
poster has failed**, however good it looks at 1080.

Show the user the PNG, not just a "done".

## 6. Tuning is CSS, never Python

Layout lives in `content/instagram/src/_shared.css`. `open src/<id>-01.html` in a normal
Chrome tab — it is 1:1 — and edit that stylesheet in DevTools. `build_posts.py` emits
structure and data-driven custom properties; putting design decisions in it would mean a
regenerate-and-rerender cycle for every nudge.

The output is `out/<id>-NN.png` (upload in filename order), `out/<id>.caption.txt` and
`out/<id>.alt.txt` (Instagram's per-image alt field).
