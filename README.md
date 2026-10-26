# Course Training Skills

**Turn a few course requirements into a complete, ready-to-teach training package with Claude.**

You give it a course name, audience, level and schedule. It produces a course
plan, timed session agendas, in-class activities and training games,
practical exercises, Jupyter notebooks (when the topic needs code), slide
content, assessments, and an instructor guide. Then it reviews everything for
consistency.

Built for instructors and trainers who spend days preparing each course and
would rather spend that time teaching.

> **Everything it produces is a draft.** It is a strong starting point, not a
> replacement for your judgment. Review the content before you teach it,
> especially facts, examples, and anything tied to a specific institution.

[العربية ↓](#بالعربي)

---

## What you get

Example request:

```text
Create a Machine Learning course.
Audience: University students
Level: Beginner
Duration: 12 hours, 6 sessions of 2 hours
```

Output (one folder per course):

```text
courses/machine-learning-beginners/
├── course-manifest.yaml     # single source of truth for the course
├── course-plan.md           # overview, objectives, prerequisites, structure
├── sessions/                # per-session design + agenda that sums to the exact duration
├── activities/              # activities and games, each with a learning purpose
├── exercises/               # practical work (student version + instructor solution)
├── notebooks/               # student + instructor .ipynb, only when code helps
├── slides/                  # slide content, plus an editable deck when a slide tool is available
├── assessments/             # every question mapped to a learning objective
├── instructor-guide/        # misconceptions, questions to ask, transitions, recovery plans
└── review/                  # automated quality review of the whole package
```

**See a real example:** [`courses/machine-learning-beginners/`](courses/machine-learning-beginners/).
Session 1 is fully generated, including an editable 19-slide deck ([`session-01-slides.pptx`](courses/machine-learning-beginners/slides/session-01-slides.pptx)); Sessions 2–6 are at outline and agenda level
([details](examples/machine-learning/README.md)).

### How it works

- **Interactive by default.** It stops for your approval after the outline,
  after session design, and after activities, so you can steer before it
  builds the rest. Say "build the whole thing" to run it end to end without
  stopping.
- **Consistent across files.** If a notebook uses a concept that was never
  taught, or an assessment tests it, the reviewer flags it.
- **Small changes stay small.** Ask to go from 6 sessions to 4, or from
  in-person to online, and it updates only the affected parts.
- **Timing is checked.** Agendas must add up to the exact session length.

---

## Requirements

You need **one** of these:

- **Claude on the web, desktop or mobile** on a Pro, Max, Team or Enterprise
  plan, with code execution and file creation turned on. Skills are not
  available on the free plan.
- **Claude Code**.

---

## Install

### Option A: Claude (claude.ai)

1. Download `course-training-skills-CLAUDE-SKILL-UPLOAD.zip` from the
   [Releases page](https://github.com/Mosapmohamd/course-training-skills/releases),
   or build it yourself: `bash scripts/build_claude_ai_skill_package.sh`
   (output goes to `dist/`).
2. In Claude, open **Settings → Capabilities**, find **Skills**, and click
   **Upload skill**. Select the zip.
3. Start a new chat and ask for a course (see [Usage](#usage)).

Team and Enterprise plans may need an admin to enable skills first.

### Option B: Claude Code

```text
/plugin marketplace add Mosapmohamd/course-training-skills
/plugin install course-training-skills@course-training-skills
```

To try a local clone without installing:

```bash
git clone https://github.com/Mosapmohamd/course-training-skills
claude --plugin-dir ./course-training-skills
```

---

## Usage

Just describe the course in plain language, in Arabic or English:

```text
Design a 3-hour in-person workshop on writing a professional CV
for fresh graduates. One session. Arabic content.
```

```text
صمّم كورس Python من الصفر لطلاب جامعة، 6 محاضرات كل واحدة 3 ساعات ونص.
```

Useful follow-ups:

- "Build the whole thing without stopping."
- "Make it 4 sessions instead of 6."
- "Review the course."
- "Create the slides for session 2."

---

## Make it yours

All personal and stylistic settings live in [`config/`](config/README.md):

| File | Change it to set |
|---|---|
| `instructor-profile.md` | Your name, titles and contact channels for the intro, contact and thank-you slides |
| `teaching-preferences.md` | Delivery mode, activity pacing, assessment style, language and tone |
| `presentation-style.md` | Fonts, colors and slide layouts |
| `defaults.yaml` | Workflow defaults and optional institution rules |

Until you fill in your profile, the slides show bracketed placeholders such as
`[Your full name]`. Nothing is invented.

To keep your details out of a public fork, put them in `*.local.*` copies
(for example `config/instructor-profile.local.md`). Those files are
git-ignored and get baked into the zip when you build it. See
[`config/README.md`](config/README.md).

### Optional: Egypt "حقيبة الكورسات" (Course Bag) program

If you submit courses to this program, set
`institutional_requirements.course_bag_program: true` in `config/defaults.yaml`.
The toolkit will then check the program's minimum hours and certificate
threshold up front, and generate the submission draft and `timetable.xlsx`.
It is off by default. The rules were last checked in October 2026; always
confirm against the program's current form
([rules file](references/institutional-requirements/course-bag-program.md)).
You can add your own institution's rules the same way.

---

## Known limitations

- **Editable slide decks** need a slide-making capability in your Claude
  environment. Without one, you get a detailed slide specification
  (content, visuals and speaker notes per slide) instead of a deck file.
- **Quality depends on the topic.** It is strongest for subjects Claude knows
  well. For fast-moving or niche topics, ask it to research, and check the
  facts yourself.
- **It is long-running.** A full multi-session course is a lot of content, so
  interactive mode, with a session at a time, usually gives better results
  than one giant run.

---

## Contributing and feedback

Found a bug, or a course that came out wrong?
[Open an issue](https://github.com/Mosapmohamd/course-training-skills/issues/new/choose).
Pull requests are welcome; read [`CLAUDE.md`](CLAUDE.md) first for how the
repo is organized.

Run the checks before opening a PR:

```bash
pip install pytest pyyaml
python3 scripts/check_structure.py
python3 -m pytest tests/
```

The full design specification is in [`docs/specification.md`](docs/specification.md).

---

## بالعربي

**Course Training Skills** أداة مجانية مفتوحة المصدر بتشتغل مع Claude. بتاخد منك
اسم الكورس، والجمهور، والمستوى، وعدد الساعات والمحاضرات، وبتطلعلك حقيبة تدريبية
كاملة: خطة الكورس، أجندة كل محاضرة بالدقيقة، أنشطة وألعاب تدريبية، تمارين عملية،
Notebooks لو الموضوع فيه كود، محتوى السلايدز، اختبارات، ودليل للمدرب. وفي الآخر
بتراجع كل ده وتتأكد إنه متسق.

**المتطلبات:** اشتراك Claude مدفوع (Pro أو Max أو Team أو Enterprise) مع تفعيل
Code execution and file creation، أو Claude Code.

**التثبيت على Claude:**

1. نزّل ملف الـ zip من صفحة
   [Releases](https://github.com/Mosapmohamd/course-training-skills/releases).
2. افتح **Settings ← Capabilities**، وفي قسم **Skills** اضغط **Upload skill**
   واختار الملف.
3. افتح شات جديد واكتب طلبك عادي، مثلًا:
   «صمّم ورشة 3 ساعات حضوري عن كتابة الـ CV لحديثي التخرج».

**خلّيها بتاعتك:** اكتب اسمك وألقابك وطرق التواصل في
`config/instructor-profile.md`، وغيّر الألوان والخطوط من
`config/presentation-style.md`. ولو بتقدّم على برنامج «حقيبة الكورسات» فعّل
`course_bag_program: true` في `config/defaults.yaml`.

**مهم:** اللي بتطلعه الأداة مسودة قوية، مش نسخة نهائية. راجع المحتوى قبل ما تدرّسه.

عندك مشكلة أو اقتراح؟ افتح
[Issue](https://github.com/Mosapmohamd/course-training-skills/issues/new/choose).

---

## Author

Built by [Mosap Abdel-Ghany](https://www.linkedin.com/in/mosap-abdel-ghany),
AI engineer and trainer. Released under the [MIT License](LICENSE).
