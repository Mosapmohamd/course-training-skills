---
name: course-designer
description: The main orchestrator. Parses course requirements, creates and maintains course state and the course manifest, invokes the specialized skills in dependency order, manages approval checkpoints in interactive mode (the default) or runs autonomously in full mode, tracks dependencies, triggers downstream regeneration on change, and runs the final quality review. Use this first for any new course request or full-course adaptation.
---

# course-designer

## Purpose
Own the workflow, state, and manifest for a course. Orchestrate the other
nine skills — never duplicate their content-generation logic itself.

## Trigger
- Any new course request ("create a course on X...").
- `/create-course` (interactive, default) or `/create-course --full` (full mode).
- `/adapt-course` for an existing course.

## Non-trigger conditions
- Do not generate outline/session/activity/exercise/notebook/slide/
  assessment/instructor-guide/review content directly — delegate.
- A request scoped to a single artifact type on an *existing* course
  (e.g. "just redo session 3's exercise") can skip full orchestration and
  route straight to the owning skill, but course-designer still updates
  `status` in the manifest afterward.

## Inputs
Raw user request (course name, audience, level, duration, sessions, session
duration, optional extras — `README.md` §4). For adaptation: an existing
`courses/<id>/course-manifest.yaml` plus the requested change.

## Outputs
`courses/<course-id>/course-manifest.yaml`, course state tracking, and the
orchestration that produces every other artifact in
`references/instructional-design/course-architecture.md`'s output structure.

## Dependencies
None — this is the entry point.

## References
- `references/instructional-design/course-architecture.md` (state/manifest schema)
- `references/adaptation/adaptation-rules.md`
- `references/instructional-design/course-architecture.md#research-policy`

## Templates
Indirectly all of them, via the skills it invokes.

## Downstream consumers
The user; also `course-reviewer` reads the manifest's `status` to know what's
ready to review.

## Procedure

### 1. Parse requirements
Extract required fields; infer reasonable defaults for optional fields
(`README.md` §3: "do not ask unnecessary questions"). Ask a clarifying
question ONLY when a missing/ambiguous value would materially change the
course design (e.g. session count/duration arithmetic doesn't resolve
cleanly, or level is genuinely unclear from context) — not for anything
inferable.

### 2. Determine mode
Default: **interactive**. If the user says `--full` or equivalent ("just
build the whole thing", "don't stop for approval"): **full mode**.

### 3. Create course state + manifest
`course.id` = kebab-case slug of the name. Initialize
`course-manifest.yaml` per the schema in
`references/instructional-design/course-architecture.md`, all `status`
fields `pending`.

### 4. Invoke skills in dependency order
```
course-outline
  → [approval if interactive]
session-designer (per session)
  → [approval if interactive]
activity-designer + practical-work (per session, can run together)
  → [approval if interactive]
notebook-designer (per session, decides applicability itself)
slide-designer (per session)
  → [approval if interactive, only if notebooks/slides substantially change scope]
assessment-designer (per session + final)
instructor-guide (per session)
course-reviewer (whole course)
```
This mirrors `README.md` §5 and §29. In full mode, run straight through,
still validating each phase's output before moving to the next (do not skip
validation just because there's no user checkpoint).

### 5. Approval checkpoints (interactive mode)
After Outline, after Session Design, after Activities+Practical Work, and
after Notebooks+Slides *if the instructor asked to review them* — present
the artifact, accept edits, re-validate, then proceed. Do not create a
checkpoint after every micro-step (`README.md` §29).

### 6. Track dependencies and status
After each skill completes, update `status` in the manifest. When the user
requests a change mid-course or via `/adapt-course`, follow
`references/adaptation/adaptation-rules.md` exactly — identify blast radius,
mark only affected items `pending`, re-invoke only the owning skills for
those items.

### 7. Final review
Once all artifacts are `approved`/generated, invoke `course-reviewer` on the
whole course. Report the result to the user; if it fails, fix what's
fixable and re-run, or surface what needs an instructor decision.

## Validation
- [ ] Manifest passes `scripts/validate_manifest.py`
- [ ] No skill was asked to produce content outside its declared responsibility
- [ ] Every approval checkpoint (interactive mode) was honored, not skipped
- [ ] `status` accurately reflects what's actually been generated
