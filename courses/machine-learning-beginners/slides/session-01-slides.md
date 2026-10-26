# Slide Spec: Session 1 — What Is Machine Learning?

Wrapped in the deck frame from `references/slides/slide-patterns.md#deck-frame`.
Stage 2 output: `slides/session-01-slides.pptx`.

## Slide 1: Title
- **Purpose:** Orient learners; set expectations for the session.
- **Main Content:** "Machine Learning — Session 1: What Is Machine Learning?" / Session 1 of 6 · In person · 120 min / instructor name (from `config/instructor-profile.md`) and date.
- **Visual Recommendation:** Title slide per `config/presentation-style.md` (dark background, eyebrow with session number, format and duration).
- **Speaker Notes:** Welcome; no content yet.
- **Interaction:** None.

## Slide 2: Trainer Intro
- **Purpose:** Establish who is teaching and why they're credible, in three lines.
- **Main Content:** Three stacked items: name / professional title / instructor title, from `config/instructor-profile.md` (bracketed placeholders until the profile is filled in).
- **Visual Recommendation:** Three full-width stacked cards, very large text, one icon per card, no paragraphs.
- **Speaker Notes:** Tell your story out loud in 60 seconds: background, why you teach this, one real ML project you worked on.
- **Interaction:** None.

## Slide 3: Agenda
- **Purpose:** Show the shape of the 120 minutes so learners know when the break and hands-on work come.
- **Main Content:** What is ML? (20) · Pattern game (15) · Types + workflow (20) · Break (10) · Environment setup (35) · Exit ticket (5) · Recap (10). From `sessions/session-01-agenda.md`.
- **Visual Recommendation:** Timeline of agenda blocks with minutes.
- **Speaker Notes:** Point out that the second hour is hands-on.
- **Interaction:** None.

## Slide 4: Objectives
- **Purpose:** State what learners will be able to do by the end.
- **Main Content:** 1) Explain what ML is vs. rule-based programming. 2) Name the three types of ML with an example each. 3) Describe the workflow: data → train → evaluate → use. 4) Have a working Python + Jupyter + scikit-learn environment. From `sessions/session-01.md`.
- **Visual Recommendation:** Four numbered cards.
- **Speaker Notes:** Say you'll come back to these four at the recap.
- **Interaction:** None.

## Slide 5: Roadmap
- **Purpose:** Show where this session sits in the whole course.
- **Main Content:** 6-box horizontal timeline, Session 1 highlighted: "ML Basics → Data → First Classifier → Comparing Models → Improving → Project".
- **Visual Recommendation:** Horizontal step diagram, 6 boxes.
- **Speaker Notes:** "By Session 6 you'll build and present your own classifier — today we lay the foundation."
- **Interaction:** None.

## Slide 6: Traditional Programming vs. ML (Concept)
- **Purpose:** Establish the core distinction before naming it "ML".
- **Main Content:** Two columns — "Traditional: rules → program → output" vs. "ML: data + answers → model learns rules → predicts on new data".
- **Visual Recommendation:** Side-by-side flow diagrams.
- **Speaker Notes:** Use the tax calculator vs. spam filter example live.
- **Interaction:** Question — "Can anyone think of a task where writing explicit rules would be really hard?"

## Slide 7: What Machine Learning Is (Definition)
- **Main Content:** "A program that improves at a task by learning patterns from example data, rather than following rules a human wrote."
- **Purpose:** Anchor the precise definition after the intuition-building above.
- **Visual Recommendation:** Single bold definition, minimal decoration.
- **Speaker Notes:** Tie back to the traditional-vs-ML comparison just shown.
- **Interaction:** None.

## Slide 8: Instructions — Pattern-Recognition Activity
- **Purpose:** Set up the upcoming activity.
- **Main Content:** "In pairs: 8 training cards, find the pattern. Then predict 4 test cards. 15 minutes."
- **Visual Recommendation:** Simple numbered instructions, example card image.
- **Speaker Notes:** Clarify: don't guess out loud yet, write your rule down first.
- **Interaction:** Pause for activity.

## Slide 9: Types of ML — Supervised (Concept)
- **Main Content:** "Learning from labeled examples → predicting labels on new data. Example: predicting house price from features."
- **Purpose:** First of three ML types, tied directly to what the activity just demonstrated.
- **Visual Recommendation:** Icon + one-line definition + example.
- **Speaker Notes:** "That's exactly what you just did with the cards."
- **Interaction:** None.

## Slide 10: Types of ML — Unsupervised (Concept)
- **Main Content:** "Finding structure with no labels. Example: grouping customers by purchase behavior."
- **Purpose:** Contrast with supervised.
- **Visual Recommendation:** Icon + one-line definition + example.
- **Speaker Notes:** No answer key this time — the model finds groups itself.
- **Interaction:** None.

## Slide 11: Types of ML — Reinforcement (Definition only)
- **Main Content:** "Learning by trial, error, and reward through interaction. Example: a game-playing agent."
- **Purpose:** Complete the taxonomy; explicitly flagged as not used again this course.
- **Visual Recommendation:** Icon + one-line definition + example.
- **Speaker Notes:** "We won't use this again in this course — just know it exists."
- **Interaction:** None.

## Slide 12: The Standard ML Workflow (Process)
- **Main Content:** "Collect/Prepare Data → Train a Model → Evaluate → Use." 4-step process diagram.
- **Purpose:** The spine the rest of the course follows session-by-session.
- **Visual Recommendation:** 4-box horizontal process diagram.
- **Speaker Notes:** "Session 2 is step 1, Sessions 3-5 are steps 2-3, Session 6 is all four."
- **Interaction:** None.

## Slide 13: Break
- **Purpose:** Mark the break and when to return.
- **Main Content:** Break — 10 minutes. Back for hands-on setup.
- **Visual Recommendation:** Dark break slide, large duration number.
- **Speaker Notes:** Ask anyone who hasn't installed Python yet to start the download during the break.
- **Interaction:** None.

## Slide 14: Instructions — Environment Setup
- **Main Content:** Install commands, notebook filename, expected output shape.
- **Purpose:** Hands-off transition into the practical block.
- **Visual Recommendation:** Code block with install command; screenshot-style callout of expected output.
- **Speaker Notes:** Point to `exercises/session-01-exercise.md`'s Hints for common issues.
- **Interaction:** Pause for activity (practical exercise).

## Slide 15: Exit Ticket
- **Purpose:** Run the formative check that maps to all four objectives.
- **Main Content:** "Exit ticket — 5 questions, 5 minutes, ungraded." Questions in `assessments/session-01-assessment.md` (handed out, not projected).
- **Visual Recommendation:** Simple instructions slide with question count and time.
- **Speaker Notes:** Collect and skim them before Session 2 to see which objective needs a 2-minute revisit.
- **Interaction:** Pause for assessment.

## Slide 16: Recap
- **Main Content:** "ML learns patterns from data. 3 types: supervised, unsupervised, reinforcement. Workflow: data → train → evaluate → use. Environment confirmed."
- **Purpose:** Consolidate before ending.
- **Visual Recommendation:** 4-bullet recap, matches the 4 session objectives.
- **Speaker Notes:** Preview Session 2: "Next time — getting our hands on real data with pandas."
- **Interaction:** None.

## Slide 17: Q&A
- **Purpose:** Open the floor before closing.
- **Main Content:** Questions?
- **Visual Recommendation:** Large single word, minimal decoration.
- **Speaker Notes:** Take 2–3 questions; park longer ones for after the session.
- **Interaction:** Open questions.

## Slide 18: Contact
- **Purpose:** Give learners a way to follow up.
- **Main Content:** Every channel under "Contact channels" in `config/instructor-profile.md` (LinkedIn first). Call to action: "Send me your smoke-test screenshot if anything breaks before Session 2."
- **Visual Recommendation:** 2×2 grid of icon cards, LinkedIn highlighted.
- **Speaker Notes:** Encourage them to reach out with setup problems now rather than at the start of Session 2.
- **Interaction:** None.

## Slide 19: Closing
- **Purpose:** End the session on a distinctive, designed slide.
- **Main Content:** "Thank You" / "See you in Session 2: working with real data in pandas." / instructor name and title.
- **Visual Recommendation:** The most designed slide in the deck, per `config/presentation-style.md`.
- **Speaker Notes:** Thank them; remind them of the Session 2 preview.
- **Interaction:** None.
