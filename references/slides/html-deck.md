# HTML Deck: Engine and Teaching Patterns

Used by: `slide-designer` when the deck format is `html` or `both`
(`slide-patterns.md#stage-2-targets`). Part 1 is the engine every HTML deck
runs on. Part 2 is how a topic and its examples are presented on it. Colors,
fonts and spacing are not here: they come from `config/presentation-style.md`.

An HTML deck is not a PowerPoint in a browser. It reveals an idea one step
at a time, lets the learner change an input and watch the result, and runs
the code on the slide. Use those abilities; a deck of static bullet slides
wastes the format.

## Part 1 — The engine

Start every deck from `templates/html-deck-shell.html`. Keep everything
outside `#slides` unchanged; replace the sample slides with the spec's
slides; fill the `:root` tokens from `config/presentation-style.md`.

### Stage and chrome

| Feature | Behavior |
|---|---|
| Stage | Fixed 1600×900 box scaled to fit the window. Nothing scrolls. |
| Header | Course/session name on one side; on the other the current part, the counter (`07 / 42`) and an Overview button. |
| Part label | Comes from the slide's `data-part="LABEL|NAME"` and changes as the deck moves between parts. |
| Overview | A grid of every slide by number and `data-title`; click one to jump. Opens with the button or `O`. |
| Step bar | On stepped slides: `STEP 2 / 4 · REVEAL`, then `· NEXT SLIDE` on the last step. |
| Navigation | `→` / Space / PageDown forward, `←` / PageUp back, Home / End, edge arrows, swipe. In a right-to-left deck the arrow keys swap. |
| Typing guard | Navigation keys do nothing while the cursor is in an input or code editor, so learners can type on the slide. |
| Speaker notes | `<aside class="notes">` per slide, hidden, toggled with `N`. |
| Other | `F` fullscreen, `Esc` closes overlays, the slide number is kept in the URL hash, print gives one fully revealed slide per page. |

### Slide markup

```html
<section class="slide" data-title="What is a token?" data-part="PART 03|TOKENS" data-steps="4">
  <div class="kicker">Tokenization · 01</div>
  <h1>What is a <em>token?</em></h1>
  <div class="subtitle">One line that frames the slide.</div>
  <div class="body">
    <div class="st" data-st="1">…</div>
    <div class="st" data-st="2">…</div>
  </div>
  <aside class="notes">What the instructor says.</aside>
</section>
```

- `data-title` is required on every slide (the overview and the validator
  use it).
- **Progressive reveal:** `data-steps="N"` on the slide, and `class="st"
  data-st="n"` on each element that appears at step `n`. Several elements
  may share a step. Forward reveals the next step before leaving the slide;
  going back enters the previous slide fully revealed. An `.st` element on a
  slide without `data-steps` never appears, and `scripts/validate_course.py`
  rejects it.
- A slide without steps can stagger its entrance with `class="appear"
  style="--d:160ms"`.
- `class="slide divider"` is the section divider: part label, large title,
  one bridge sentence.

### Components in the shell

| Component | Class | Use |
|---|---|---|
| Card grid | `.grid.cols-2/3/4` + `.card` | Applications, problems, reasons; reveal one card per step |
| Artifact | `.artifact` with `<mark>` | A real-looking document, message or record, with the relevant parts marked |
| Story cards | `.story-card.question/.use/.idea` | The question, where it is used, the idea |
| Notes | `.note`, `.note.good`, `.note.warn` | What it does, when it is good, when to be careful |
| Definition | `.bigdef` | The one-sentence definition, shown last |
| Chips | `.chip.good/.bad` | Tokens, items kept or dropped |
| Numbered step | `.step-head` | A worked procedure, one numbered step per reveal |
| Pros and cons | `.card.pro`, `.card.con` | Advantages and drawbacks side by side |
| Verdict | `.verdict` + `.tag` | "Used in real life?" with a short answer and where |
| Comparison table | `table.cmp`, rows as `tr.st` | Methods compared, one row per step |
| Before → after demo | `[data-demo]` + `.case` | Case tabs, a toggle that applies the operation, feedback |
| Code cell | `.code-cell` | Editable code with Run and Reset |
| Code overlay | `[data-code-overlay="id"]` + `<template id>` | Longer code opened on demand, off the main slide |
| Split | `.split` → `.story` + `.work` | Story on one side, the learner's work on the other |

### Code cells

- The editor holds the code; `data-out` holds its exact output, produced by
  actually running the code when the deck is built. Never write the output by
  hand.
- **Run** on unchanged code shows the saved output at once, with no network.
  If the learner edits Python code, the engine loads Python in the browser
  (Pyodide) on first use and runs the edited code; that step needs internet.
  For other languages set `data-lang`; edited code then shows a "reset to see
  the saved result" message.
- **Reset** restores the original code.
- Code and output stay left-to-right in every deck.

### Custom widgets

When a slide needs an interaction the shell does not have (a slider, a live
table computed from the learner's sentence, an animated diagram), write it
in a second inline `<script>` after the engine and attach it with
`Deck.onEnter("slide data-title", fn)` so it resets each time the slide
opens. Keep it inline, free of external libraries, and driven by inputs the
learner can change.

### Limits

- One file, no `<script src>` or `<link rel="stylesheet">`.
- If a slide overflows the stage, split it in the spec; do not shrink text.
- Mixed-direction text: mark each run with `dir="rtl"` or `dir="ltr"`
  (`references/localization/arabic-rtl.md` §5).

## Part 2 — Presenting a topic

These are instructional patterns. Decide them in Stage 1, where they shape
the slide list and each slide's content, and record the reveal order in the
spec's **Reveal Steps** field.

### Deck-level patterns

1. **One running example.** Pick one or two realistic artifacts from the
   learners' world and introduce them early on their own slide. Apply every
   later technique to the same artifacts, so learners compare techniques
   instead of re-reading new examples.
2. **Parts with bridges.** Group the body into parts. Open each with a
   divider slide whose sentence says what the previous part achieved and
   what problem is still open. The agenda slide lists the parts with their
   slide ranges.
3. **Number within the part.** The kicker reads `Part name · 03`, so the
   room always knows where it is.
4. **Titles make a claim or ask a question.** "Frequent is not the same as
   important", "Why not give the model the whole sentence?" — not "TF-IDF"
   or "Tokenization overview". Emphasize the phrase that carries the point.
5. **Close each part by choosing.** End with a comparison table or a
   "which one do I use?" slide, then a limit that motivates the next part.

### Topic sequence

Introduce one technique or concept across one to three slides, in this
order. Each line is one reveal step or one slide.

| Step | What appears | Why |
|---|---|---|
| 1. Concrete case | The artifact with the problem visible in it | The learner sees the need before the name |
| 2. The question | One sentence: what do we need to find, fix or decide? | Turns the case into a task |
| 3. Real-life use | Two or three places this is done in real products | Answers "why should I care" |
| 4. The idea | The concept, named now, with its key rule or syntax | The name lands on something already understood |
| 5. Try it | A code cell, a demo or an input the learner changes | Understanding is tested immediately |
| 6. Good and careful | What it is good at, then where it breaks, each with an example | Every technique is taught with its limit |
| 7. Verdict | "Used in real life?" — yes/no, by whom, for what | Places the technique in practice |

The definition comes after the example, never before it.

### Example patterns

| Pattern | Use it for | Shape |
|---|---|---|
| Before → after | Any transformation | Raw on one side, result on the other, changed parts marked |
| Worked steps | A calculation or algorithm | One numbered step per reveal, with the numbers for this exact input |
| Minimal pair | A distinction | Two inputs that differ in one thing, and what that one thing changes |
| Counter-example | A limit | An input where the technique gives the wrong answer or changes nothing — always include one |
| Case tabs | The same idea across situations | Three to six tabs, the last one a counter-example |
| Learner's own input | Anything computed | Pre-filled with the running example, editable, result updates live |
| Scale | Motivation | The same problem "in 10,000 documents", so doing it by hand is absurd |
| Decide and check | Judgment | The learner picks an option, then sees whether it fits and why |

### Interaction rules

- Every interactive slide says in its subtitle what to press and what to
  watch.
- Pre-fill every input with a working example. A blank box teaches nothing.
- Make the learner predict before the reveal: show the question, then the
  result on the next step.
- Feedback states the consequence, not "correct" or "wrong": what a real
  system would now do.
- One idea per reveal step, and at most about eight steps per slide.

### Mapping to Stage 1

In the spec, each slide records its pattern in **Purpose** ("topic sequence
steps 1–4 for regex anchors"), its ordered reveals in **Reveal Steps**, and
its try-it element in **Interaction** (`code-cell`, `demo`, `live-input`,
`decide-and-check`). Stage 2 builds exactly those; it does not add content.
A `.pptx` built from the same spec keeps the sequence and examples and turns
each interaction into a static worked example.
