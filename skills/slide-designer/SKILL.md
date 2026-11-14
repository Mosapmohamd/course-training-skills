---
name: slide-designer
description: Two-stage skill. Stage 1 produces an instructional slide specification (per-slide title, purpose, content, visual recommendation, speaker notes, interaction) matching the session's actual content. Stage 2 builds a real, self-contained HTML slide deck (one .html file per session) from that spec — never a flattened image deck. A .pptx is built only when the user explicitly asks for one.
---

# slide-designer

## Purpose
Specify what each slide teaches (Stage 1), then build a self-contained
HTML slide deck from that spec (Stage 2).

## Trigger
`course-designer` invokes per session after `session-designer` (and usually
after activities/exercise, since slides may reference them) completes.
`/create-slides` invoked directly.

## Non-trigger conditions
- Do not design session content here — pull it from `session-designer`'s
  Topics/Explanation, don't invent new content at slide time.
- Do not produce a `.pptx` or a native slide-deck artifact unless the user
  explicitly asks for that format; the default Stage 2 output is HTML.

## Inputs
This session's Topics, Key Concepts, Examples (`session-designer`);
Activities/Exercise names for Instructions/Exercise-type slides;
`config/instructor-profile.md` (Trainer Intro, Contact, Closing slides);
`config/presentation-style.md` (Stage 2 only).
For each config file, read its `.local` variant instead when one exists
(e.g. `config/instructor-profile.local.md`, see `config/README.md`).

## Outputs
Stage 1: `slides/session-NN-slides.md`, one entry per
`templates/slide-template.md`. Stage 2:
`slides/session-NN-slides.html` — one self-contained HTML file built to
`slide-patterns.md#html-deck-format`, with live text, tables, code blocks
and diagrams; images may remain images. Only on explicit request: a
`.pptx` or native deck (`slide-patterns.md#stage-2-targets`).

## Dependencies
`session-designer` (required); `activity-designer`, `practical-work`
(referenced, not required — slides can be drafted before them and revised).

## References
`references/slides/slide-patterns.md` (Stage 1, and the HTML deck format
for Stage 2),
`config/presentation-style.md` (Stage 2, visual design only — never
instructional content).

## Templates
`templates/slide-template.md`

## Downstream consumers
`course-reviewer` (Slide alignment check); the instructor (delivery).

## Procedure

### Stage 1 — specification
1. Walk this session's Topics/Key Concepts/Examples in teaching order.
2. For each teaching beat, choose a slide type from `slide-patterns.md`'s
   catalog (Concept, Visual explanation, Example, Diagram, Definition,
   Process, Comparison, Question, Instructions, Exercise, Recap).
3. Fill Slide Number, Title, Purpose, Main Content (≤6 bullets/≤8 words
   default), Visual Recommendation (described, not designed), Speaker Notes
   (what's said, not a restatement of the slide), Interaction.
4. Do not copy the course outline or the instructor guide verbatim onto
   slides — each slide earns its place in the teaching sequence.
5. Include at least one Recap slide at session end, and an
   Instructions/Exercise slide immediately before any Practice block.
6. Wrap the deck in the frame from `slide-patterns.md#deck-frame`: Title →
   Trainer Intro → Agenda → Objectives → … → Recap → Q&A → Contact
   (penultimate) → Closing "Thank You" (last). Fill the Trainer Intro and
   Contact from `config/instructor-profile.md`; a missing value, or one still
   written as `{{...}}`, becomes a bracketed placeholder (`[Your full name]`)
   listed in the hand-off, never an invented one.
7. Give every activity in `activities/session-NN-activities.md` (embedded
   micro-activities included) its own Instructions slide where it runs, per
   `slide-patterns.md#activity-slides`.
8. If the manifest says `delivery.direction: rtl`, write the spec in Arabic
   and apply `slide-patterns.md#right-to-left-arabic-decks` plus
   `references/localization/arabic-rtl.md` §5 (Slides) in Stage 2:
   `<html lang="ar" dir="rtl">`, mirrored layout, Arabic-capable fonts.

### Stage 2 — HTML deck generation
1. Feed Stage 1's spec as the only source of instructional content. Apply
   visual design (typography, color, spacing, layout, diagram/code/chart
   style) from `config/presentation-style.md`.
2. Write `slides/session-NN-slides.html` to
   `slide-patterns.md#html-deck-format`: one file, one
   `<section class="slide">` per spec slide in spec order, inline CSS and
   JavaScript, keyboard/click navigation, speaker notes, print stylesheet.
3. Build every slide from real elements — live text, `<table>`,
   `<pre><code>`, inline SVG or HTML/CSS diagrams — never a full-slide
   screenshot/image standing in for the whole slide. Photographic/
   illustrative images may remain images.
4. Validate with `python3 scripts/validate_course.py courses/<course-id>/`
   (parses the deck, checks it is self-contained, and compares its slide
   count to the spec) before calling it done. Record the file path in the
   manifest's `slides:` entry.
5. If the user explicitly asked for a `.pptx` or a native deck, build it
   as well, per `slide-patterns.md#stage-2-targets`.

## Validation
- [ ] Every slide's content traces to this session's actual Topics/Explanation
- [ ] No slide is a verbatim copy of the outline or instructor guide
- [ ] Deck frame present: Trainer Intro second, Contact penultimate,
      Closing "Thank You" last
- [ ] Every activity in the session's activities file has its own slide
- [ ] Stage 2 produced `slides/session-NN-slides.html`: self-contained, one
      `<section class="slide">` per spec slide, passing
      `scripts/validate_course.py`
