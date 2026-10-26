# Example: CV Writing for Fresh Graduates (Arabic, RTL, 3h × 1)

The repository's Arabic example: a complete single-session course written in
Egyptian Arabic, right-to-left in every file, built by following the
toolkit's skills.

```text
اعمل ورشة 3 ساعات حضوري عن كتابة الـ CV لحديثي التخرج، محاضرة واحدة.
```

The package lives at
[`courses/cv-writing-fresh-graduates-ar/`](../../courses/cv-writing-fresh-graduates-ar/):

- `course-manifest.yaml` — `delivery.language: ar`, `delivery.direction: rtl`
- `course-plan.md`, `sessions/session-01.md`, `sessions/session-01-agenda.md`
  (180 minutes, validated)
- `activities/session-01-activities.md` — 4 activities (2 embedded in
  explanation blocks)
- `exercises/session-01-exercise.md` — learners rewrite their own CV;
  instructor solution with a fictional before/after
- `assessments/session-01-assessment.md` — 10-point peer-review checklist +
  3-question exit ticket
- `instructor-guide/session-01-guide.md` — misconceptions, interventions,
  10/20-minute recovery plan, transitions
- `slides/session-01-slides.md` + `slides/session-01-slides.pptx` — 23
  editable RTL slides (mirrored layout, Arabic fonts set in the theme)
- `review/course-review.md` — all checks PASS; two instructor decisions noted

All names and CVs in the examples are fictional. Trainer and contact slides
show bracketed placeholders until `config/instructor-profile.md` is filled in.

## Fonts

The deck uses Cairo (headings) and IBM Plex Sans Arabic (body) from
`config/presentation-style.md`. Both are free on Google Fonts. Install them
before presenting, or PowerPoint substitutes another Arabic font.

## Validate it yourself

```bash
python3 scripts/validate_manifest.py courses/cv-writing-fresh-graduates-ar/course-manifest.yaml
python3 scripts/validate_course.py courses/cv-writing-fresh-graduates-ar/
```

`validate_course.py` also checks the RTL rules: every Arabic markdown file is
wrapped in `<div dir="rtl">`, and every Arabic paragraph on the slides and
their layouts is right-to-left.
