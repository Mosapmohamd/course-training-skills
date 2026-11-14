---
name: slide-designer
description: Two-stage skill. Stage 1 produces an instructional slide specification (per-slide title, purpose, content, visual recommendation, speaker notes, interaction) matching the session's actual content. Stage 2 builds a real deck from that spec in the format the instructor chose — a self-contained HTML deck, an editable .pptx, or both — never a flattened image deck, and asks which format when none was chosen.
---

# slide-designer

## Purpose
Specify what each slide teaches (Stage 1), then build the deck from that
spec in the instructor's chosen format: HTML, `.pptx`, or both (Stage 2).

## Trigger
`course-designer` invokes per session after `session-designer` (and usually
after activities/exercise, since slides may reference them) completes.
`/create-slides` invoked directly.

## Non-trigger conditions
- Do not design session content here — pull it from `session-designer`'s
  Topics/Explanation, don't invent new content at slide time.
- Do not pick the deck format yourself. Resolve it per
  `slide-patterns.md#stage-2-targets`, and ask when nothing has set it.

## Inputs
This session's Topics, Key Concepts, Examples (`session-designer`);
Activities/Exercise names for Instructions/Exercise-type slides;
`config/instructor-profile.md` (Trainer Intro, Contact, Closing slides);
`config/presentation-style.md` (Stage 2 only).
For each config file, read its `.local` variant instead when one exists
(e.g. `config/instructor-profile.local.md`, see `config/README.md`).

## Outputs
Stage 1: `slides/session-NN-slides.md`, one entry per
`templates/slide-template.md`. Stage 2, by chosen
format (`slide-patterns.md#stage-2-targets`):
`slides/session-NN-slides.html` (one self-contained file built to
`slide-patterns.md#html-deck-format`), `slides/session-NN-slides.pptx`
(a real editable deck), or both — live, editable text/tables/code blocks/
diagrams in either format; images may remain images.

## Dependencies
`session-designer` (required); `activity-designer`, `practical-work`
(referenced, not required — slides can be drafted before them and revised).

## References
`references/slides/slide-patterns.md` (Stage 1; format choice and the
HTML deck format for Stage 2),
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
   `references/localization/arabic-rtl.md` §5 (Slides) in Stage 2: every
   Arabic paragraph RTL and right-aligned, mirrored layout, Arabic-capable
   fonts, by the HTML or `.pptx` rules for the chosen format.

### Stage 2 — deck generation
1. Resolve the deck format (`html`, `pptx` or `both`) in the order given in
   `slide-patterns.md#stage-2-targets`: the request, then the manifest's
   `artifacts.slides_format`, then `config/defaults.yaml`. If none of them
   sets it, ask the instructor once — HTML, PowerPoint, or both — and
   record the answer in the manifest.
2. Feed Stage 1's spec as the only source of instructional content. Apply
   visual design (typography, color, spacing, layout, diagram/code/chart
   style) from `config/presentation-style.md`.
3. For `html` or `both`: write `slides/session-NN-slides.html` to
   `slide-patterns.md#html-deck-format` — one file, one
   `<section class="slide">` per spec slide in spec order, inline CSS and
   JavaScript, keyboard/click navigation, speaker notes, print stylesheet.
4. For `pptx` or `both`: build `slides/session-NN-slides.pptx` with real,
   editable text boxes, shapes, tables, charts and code blocks. If no
   presentation/design capability is available, say so plainly and deliver
   the HTML deck instead — never a fabricated file.
5. In either format, never use a full-slide screenshot/image standing in
   for the whole slide. Photographic/illustrative images may remain images.
6. Validate with `python3 scripts/validate_course.py courses/<course-id>/`
   before calling it done, and record each file path in the manifest's
   `slides:` entry.

## Validation
- [ ] Every slide's content traces to this session's actual Topics/Explanation
- [ ] No slide is a verbatim copy of the outline or instructor guide
- [ ] Deck frame present: Trainer Intro second, Contact penultimate,
      Closing "Thank You" last
- [ ] Every activity in the session's activities file has its own slide
- [ ] Deck format came from the request, the manifest or config, or the
      instructor was asked — never assumed
- [ ] Stage 2 produced the chosen format(s), passing
      `scripts/validate_course.py` — never a fabricated file
