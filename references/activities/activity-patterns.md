# Activity Patterns

Used by: `activity-designer`.

## Selection inputs (all required before choosing an activity)

`Topic, Audience, Level, Class Size, Session Duration, Delivery Mode, Learning Objective`

An activity is only valid if you can state, in one sentence, which specific
learning objective it serves and how the debrief proves it happened. If you
cannot, do not include the activity (see `README.md` §38: "do not generate
activities without educational purpose").

## Pattern catalog

| Pattern | Best for | Typical duration | Class size fit | Notes |
|---|---|---|---|---|
| Icebreaker | Session opening, low-stakes retrieval of prior knowledge | 5–10 min | any | Only in Session 1 or after a break of several days — not every session |
| Knowledge check | Quick formative check after Explanation | 3–7 min | any | Not graded; feeds into `assessment-designer` only if explicitly promoted |
| Think-Pair-Share | Conceptual reasoning, low material needs | 8–15 min | any, ideal 10–40 | Pair, think alone first, then share |
| Debugging challenge | Code/technical courses, post-explanation | 15–25 min | small teams (2–3) | Seed a realistic bug, not a trick |
| Case study | Applied judgment, non-single-right-answer topics | 20–40 min | teams of 3–5 | Needs a real or realistic scenario document |
| Role play | Soft skills, negotiation, interviews, stakeholder scenarios | 15–30 min | pairs/small groups | Needs clear role briefs |
| Build challenge | Hands-on synthesis after several concepts taught | 25–45 min | individual or pairs | Overlaps with `practical-work` — use activity framing only if ungraded and time-boxed as a game |
| Scenario challenge | Systems/design thinking | 20–35 min | teams of 3–5 | Present constraints, not a single correct architecture |
| Concept mapping | Consolidating a cluster of related concepts | 10–20 min | individual or pairs | Good before a summative assessment |
| Prediction activity | Priming before revealing a result/demo | 5–10 min | any | "What do you think will happen if...?" before running code/demo |
| Error analysis | Teaching common misconceptions directly | 10–20 min | individual or pairs | Show broken output/code/reasoning, ask learners to diagnose |
| Review game | End of session or course, retrieval practice | 10–20 min | any | Rotate format across sessions — do not reuse the same game every time |
| Team competition | High-energy retrieval or application practice | 15–25 min | teams of 3–5 | Use sparingly; not every session needs competitive framing |

## Anti-patterns (README §38)

- Selecting an activity for energy/fun alone with no traceable objective.
- Reusing the exact same activity type in every session (monotony; also a
  `course-reviewer` flag).
- Choosing team competitions or role play for a 1-on-1 or very small class
  where they don't functionally work — check class size fit.
- An activity that requires internet/tools not declared available in
  `delivery`.

## Required fields per activity

`Name, Objective, Duration, Participants, Materials, Instructions, Expected
Outcome, Debrief, Difficulty` — see `templates/activity-template.md`.
