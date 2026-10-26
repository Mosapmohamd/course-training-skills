# Configuration

Instructor-specific settings live here. The skills read them; they never
hardcode personal details themselves.

| File | What it controls |
|---|---|
| `instructor-profile.md` | Your name, titles and contact channels (trainer intro, contact and closing slides) |
| `teaching-preferences.md` | Default delivery mode, activity pacing, assessment style, content language and tone |
| `presentation-style.md` | Fonts, colors and slide-type styles for the generated decks |
| `defaults.yaml` | Workflow defaults and optional features, such as the course-bag program rules |

## Personal overrides (`*.local.*`)

To keep your own details out of a public fork, copy any file and add `.local`
before the extension:

```text
config/instructor-profile.md   →  config/instructor-profile.local.md
config/defaults.yaml           →  config/defaults.local.yaml
```

Rules:

- If a `.local` file exists, the skills read it **instead of** the base file.
- `.local` files are git-ignored, so they are never pushed.
- `bash scripts/build_claude_ai_skill_package.sh` copies each `.local` file
  over its base file inside the zip. The zip you upload to claude.ai then
  carries your details while the public repo stays generic.

If you have forked the repo and don't mind your details being public, you can
edit the base files directly instead.
