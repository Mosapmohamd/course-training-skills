# Arabic Content and Right-to-Left (RTL) Output

Used by: `course-designer` (detects the course language), every content skill
(language and dialect of what they write), `slide-designer`,
`notebook-designer`, `course-designer`'s spreadsheets (direction of each file
format), `course-reviewer` (Language & direction check).

Settings live in `config/defaults.yaml` under `language:` and in
`config/teaching-preferences.md`.

## 1. Decide the language once, at requirements time

- `language.content: auto` (default): the course language is the language of
  the course request. An Arabic request produces an Arabic course; an
  English request produces an English one. An explicit instruction in the
  request ("write it in English") wins.
- Record it in the manifest: `delivery.language: ar` and
  `delivery.direction: rtl` (or `en` / `ltr`). Every skill reads it from
  there and never re-guesses.
- Arabic means **right-to-left for every learner- and instructor-facing
  artifact**: markdown, notebooks' markdown cells, slides, spreadsheets.
  File names, folder names, YAML keys and code stay English/LTR.

## 2. Which Arabic

- `language.arabic_variety: egyptian` (default) or `msa`.
- Spoken and classroom material (slides, activity instructions, speaker
  notes, instructor guide, exercises) follows the configured variety.
- Formal and institutional documents (course-bag submission draft, official
  course descriptions, certificates) are always Modern Standard Arabic, even
  when the variety is `egyptian`.
- Don't mix varieties inside one artifact.
- Technical and platform terms stay in English when that is how
  practitioners say them (CV, ATS, LinkedIn, Headline, Python, Prompt).
  Don't invent Arabic translations for established English terms, and don't
  transliterate them into Arabic script.

## 3. Numbers

- Use Western digits (0–9) everywhere. They are standard in Egyptian
  technical and training material, and `scripts/validate_course.py` parses
  agenda tables with Western digits only.
- Times and durations: `15 دقيقة`, `3 ساعات`. Keep the number before the unit.

## 4. Mixed Arabic + English text (bidi)

Arabic sentences that contain English terms are where RTL breaks.

- Keep English terms short and inline; don't start an Arabic paragraph or
  bullet with an English word when you can reorder the sentence. A paragraph
  whose first strong character is Latin is laid out left-to-right by most
  renderers.
- Wrap code, file names, commands and URLs in backticks (markdown) or a
  separate LTR element (slides) so punctuation doesn't jump to the wrong side.
- Punctuation goes at the logical end of the Arabic sentence; use Arabic
  punctuation (`،` `؛` `؟`) in Arabic sentences.
- Lists of English items (for example skills on a CV) go in their own LTR
  block, not interleaved word by word with Arabic.

## 5. Per-format rules

### Markdown (`.md`)

GitHub and most viewers render markdown left-to-right unless told otherwise.

- Wrap the whole body of an Arabic file in a right-to-left block, with blank
  lines around the markers so the markdown inside still renders:

  ```markdown
  <div dir="rtl">

  # عنوان الملف
  ...

  </div>
  ```
- Headings mirror the template headings. Where a template heading is a
  field name other tools or reviewers look for, keep the English field name
  in parentheses after the Arabic: `## أهداف المحاضرة (Session Objectives)`.
- Tables inside the block render right-to-left automatically (first column
  on the right).
- Code blocks: wrap in `<div dir="ltr">` … `</div>` (blank lines around) so
  code stays left-aligned.

### Jupyter notebooks (`.ipynb`)

- Markdown cells: same `<div dir="rtl">` wrapper per cell.
- Code cells, code comments, variable names and printed output stay English
  and LTR. Explain in the markdown cell above, in Arabic.

### Slides (`.pptx` and native decks)

Content rules are in `references/slides/slide-patterns.md#right-to-left-arabic-decks`.
Stage 2 technical rules:

- Every Arabic paragraph is an RTL paragraph: OOXML `<a:pPr rtl="1" algn="r">`.
  With pptxgenjs: `rtlMode: true, align: "right"` on every Arabic text box,
  and `lang: "ar-EG"` (or `ar-SA` for MSA-only decks).
- Pure-English lines (code, URLs, sample English sentences) stay LTR:
  no `rtlMode`, `align: "left"`.
- Mirror the layout, not just the text: titles and body anchor to the right
  margin; the first card/step in a row sits on the right; numbered steps
  run right → left; "next" arrows point left (`←`).
- Fonts must have Arabic glyphs. Use `config/presentation-style.md`'s fonts.
  If they're not common system fonts (for example Cairo, IBM Plex Sans
  Arabic), say so in the hand-off and in the course README, so the
  instructor installs them or swaps in a font that ships with Office and
  supports Arabic (Arial, Tahoma, Segoe UI, Sakkal Majalla).
- Slide numbers and footers move to the mirrored side (number bottom-left,
  footer text bottom-right).
- Arabic text uses the theme's **complex-script** font (`<a:cs>` and the
  `script="Arab"` slot in `ppt/theme/theme1.xml`), not the Latin font. Set
  both to the deck's Arabic fonts. pptxgenjs leaves them empty, which makes
  PowerPoint fall back to its default Arabic font.
- pptxgenjs ignores `rtlMode` on slide-master/layout objects (footers,
  placeholders). Post-process the layout XML so those paragraphs carry
  `rtl="1"` too. `scripts/validate_course.py` checks slides, layouts and
  masters.
- Prefer drawn list rows (a small dot shape on the right + an RTL text box)
  over automatic bullets: bullet placement for RTL paragraphs differs
  between PowerPoint, Keynote and LibreOffice.
- Don't start an Arabic slide title with an English word; it flips the
  title's alignment in some renderers. Put the Arabic first:
  `تذكرة الخروج (Exit ticket)`.

### Spreadsheets (`.xlsx`, e.g. the course-bag timetable)

- Set the sheet direction right-to-left (openpyxl:
  `ws.sheet_view.rightToLeft = True`) and right-align Arabic cells.
- Column headers in Arabic; the first column (lecture number) ends up on the
  right.

### Word documents (`.docx`, if generated)

- Paragraphs carry `<w:bidi/>`, runs carry `<w:rtl/>`, alignment right.

## 6. Self-check before hand-off

- [ ] `delivery.language` and `delivery.direction` set in the manifest
- [ ] Every Arabic `.md` file body is inside `<div dir="rtl">`
- [ ] Every Arabic notebook markdown cell is inside `<div dir="rtl">`
- [ ] Every Arabic slide paragraph is RTL and right-aligned; English-only
      lines are LTR
- [ ] Spreadsheets are right-to-left
- [ ] One Arabic variety per artifact; formal documents in MSA
- [ ] Western digits in all tables

`scripts/validate_course.py` checks the markdown, notebook, slide and
spreadsheet direction rules automatically for courses whose manifest says
`delivery.direction: rtl`.
