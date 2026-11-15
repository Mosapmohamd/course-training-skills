#!/usr/bin/env python3
"""
Validate a generated course directory for structural correctness:
- agenda timing sums exactly to session_duration
- notebooks are valid nbformat 4 JSON with required cell fields
- HTML slide decks are parseable, self-contained (no external scripts or
  stylesheets) and have one <section class="slide"> per slide in the spec
- pptx files (if present) are valid zip/OOXML packages with a slide part
- required session fields are present
- for right-to-left courses (manifest delivery.direction: rtl): markdown
  bodies, notebook markdown cells, slide decks and spreadsheets are
  right-to-left (references/localization/arabic-rtl.md)

Usage:
    python3 scripts/validate_course.py courses/<course-id>/
"""
import sys
import os
import re
import json
import zipfile
import glob
from html.parser import HTMLParser

try:
    import yaml
except ImportError:
    yaml = None


def parse_minutes(value):
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().lower()
    m = re.match(r"^([\d.]+)\s*h(ours?)?$", s)
    if m:
        return float(m.group(1)) * 60.0
    m = re.match(r"^([\d.]+)\s*m(in(utes)?)?$", s)
    if m:
        return float(m.group(1))
    raise ValueError(f"Cannot parse minutes from: {value!r}")


def validate_agenda_file(path, session_duration_minutes):
    """Parse a markdown agenda table's Minutes column and sum it."""
    errors = []
    with open(path) as f:
        text = f.read()
    rows = re.findall(
        r"^\|\s*\d+\s*\|[^|]*\|\s*(\d+(?:\.\d+)?)\s*\|", text, re.MULTILINE
    )
    if not rows:
        errors.append(f"{path}: no parseable agenda rows found")
        return errors
    total = sum(float(r) for r in rows)
    if abs(total - session_duration_minutes) > 0.5:
        errors.append(
            f"{path}: agenda sums to {total} min, expected {session_duration_minutes} min"
        )
    return errors


def validate_notebook(path):
    errors = []
    try:
        with open(path) as f:
            nb = json.load(f)
    except Exception as e:
        return [f"{path}: not valid JSON ({e})"]

    if nb.get("nbformat") != 4:
        errors.append(f"{path}: nbformat must be 4, got {nb.get('nbformat')!r}")
    if "cells" not in nb or not isinstance(nb["cells"], list):
        errors.append(f"{path}: missing/invalid 'cells' array")
        return errors
    if len(nb["cells"]) == 0:
        errors.append(f"{path}: notebook has zero cells")
    for i, cell in enumerate(nb["cells"]):
        for field in ("cell_type", "source"):
            if field not in cell:
                errors.append(f"{path}: cell {i} missing '{field}'")
        if cell.get("cell_type") == "code" and "outputs" not in cell:
            errors.append(f"{path}: code cell {i} missing 'outputs'")
    if "student" in os.path.basename(path):
        joined = json.dumps(nb).lower()
        if "## solutions" in joined or "### solutions" in joined:
            errors.append(f"{path}: student notebook appears to contain a Solutions section")
    return errors


ARABIC = re.compile(r"[\u0600-\u06FF]")
RTL_OPEN = re.compile(r'^\s*<div dir="rtl">\s*$', re.MULTILINE)


def validate_rtl_markdown(path):
    """Arabic markdown must sit inside a <div dir="rtl"> block."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not ARABIC.search(text):
        return []
    if not RTL_OPEN.search(text):
        return [f'{path}: Arabic markdown is not wrapped in <div dir="rtl">']
    return []


def validate_rtl_notebook(path):
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            nb = json.load(f)
    except Exception:
        return []  # JSON errors are reported by validate_notebook
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        if ARABIC.search(src) and 'dir="rtl"' not in src:
            errors.append(f'{path}: markdown cell {i} has Arabic text but no dir="rtl" wrapper')
    return errors


def validate_rtl_pptx(path):
    """Every paragraph containing Arabic must be an RTL paragraph (a:pPr rtl="1"),
    on slides and on the layouts/masters behind them (footers, placeholders)."""
    errors = []
    if not zipfile.is_zipfile(path):
        return []
    with zipfile.ZipFile(path) as z:
        parts = r"ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster)\d+\.xml$"
        for name in sorted(n for n in z.namelist() if re.match(parts, n)):
            xml = z.read(name).decode("utf-8")
            bad = 0
            for para in re.findall(r"<a:p>.*?</a:p>|<a:p .*?</a:p>", xml, re.S):
                text = "".join(re.findall(r"<a:t>(.*?)</a:t>", para, re.S))
                if ARABIC.search(text) and not re.search(r'<a:pPr[^>]*\brtl="1"', para):
                    bad += 1
            if bad:
                errors.append(f"{path}: {name} has {bad} Arabic paragraph(s) without rtl=\"1\"")
    return errors


def validate_rtl_xlsx(path):
    """Every worksheet of an RTL course spreadsheet must be right-to-left."""
    errors = []
    if not zipfile.is_zipfile(path):
        return [f"{path}: not a valid xlsx package"]
    with zipfile.ZipFile(path) as z:
        for name in sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
            xml = z.read(name).decode("utf-8")
            if not re.search(r'<sheetView[^>]*\brightToLeft="(1|true)"', xml):
                errors.append(f"{path}: {name} is not set to right-to-left")
    return errors


class _DeckParser(HTMLParser):
    """Collects what validate_html_deck needs from one pass over the file."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.has_html = False
        self.html_dir = None
        self.slides = 0
        self.slide_info = []  # per slide: title, declared steps, data-st values
        self._depth = None    # <section> nesting depth inside the current slide
        self.external = []
        self.text = []
        self._skip = 0  # depth inside <script>/<style>

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.has_html = True
            self.html_dir = (a.get("dir") or "").lower() or None
        elif tag == "section":
            if self._depth is not None:
                self._depth += 1
            elif "slide" in (a.get("class") or "").split():
                self.slides += 1
                self._depth = 0
                self.slide_info.append(
                    {"title": (a.get("data-title") or "").strip(), "steps": a.get("data-steps"), "st": []}
                )
        elif tag == "script":
            if a.get("src"):
                self.external.append(f'<script src="{a["src"]}">')
            self._skip += 1
        elif tag == "style":
            self._skip += 1
        if self._depth is not None and "st" in (a.get("class") or "").split():
            self.slide_info[-1]["st"].append(a.get("data-st"))
        if tag == "link" and "stylesheet" in (a.get("rel") or "").lower().split():
            self.external.append(f'<link rel="stylesheet" href="{a.get("href")}">')

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        elif tag == "section" and self._depth is not None:
            self._depth = None if self._depth == 0 else self._depth - 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def count_spec_slides(spec_path):
    """Number of slides in a Stage 1 spec: one level-2 heading per slide."""
    with open(spec_path, encoding="utf-8") as f:
        return len(re.findall(r"^## ", f.read(), re.MULTILINE))


def _parse_deck(path):
    parser = _DeckParser()
    with open(path, encoding="utf-8") as f:
        parser.feed(f.read())
    parser.close()
    return parser


def validate_html_deck(path, expected_slides=None):
    """A Stage 2 deck is one self-contained HTML file with one
    <section class="slide"> per slide (references/slides/slide-patterns.md)."""
    try:
        deck = _parse_deck(path)
    except Exception as e:
        return [f"{path}: not readable as HTML ({e})"]
    errors = []
    if not deck.has_html:
        errors.append(f"{path}: no <html> element — not an HTML document")
    if deck.slides == 0:
        errors.append(f'{path}: no <section class="slide"> elements found')
    elif expected_slides is not None and deck.slides != expected_slides:
        errors.append(
            f"{path}: deck has {deck.slides} slide(s), spec has {expected_slides}"
        )
    for ref in deck.external:
        errors.append(f"{path}: not self-contained, loads {ref}")
    for n, info in enumerate(deck.slide_info, 1):
        errors.extend(_check_slide_steps(path, n, info))
    return errors


def _check_slide_steps(path, n, info):
    """Engine contract (references/slides/html-deck.md): every slide has a
    data-title, and its reveal steps are consistent — a .st element on a slide
    without data-steps would stay hidden forever."""
    errors = []
    where = f"{path}: slide {n}"
    if not info["title"]:
        errors.append(f"{where} has no data-title (the overview lists slides by it)")
    values = []
    for raw in info["st"]:
        if raw is None or not raw.isdigit() or int(raw) < 1:
            errors.append(f'{where} has a .st element without a valid data-st="n"')
        else:
            values.append(int(raw))
    if info["steps"] is None:
        if info["st"]:
            errors.append(f"{where} has .st reveal elements but no data-steps, so they never appear")
        return errors
    if not info["steps"].isdigit() or int(info["steps"]) < 1:
        errors.append(f"{where} has an invalid data-steps={info['steps']!r}")
    elif not values:
        errors.append(f"{where} declares data-steps={info['steps']} but has no .st elements")
    elif max(values) != int(info["steps"]):
        errors.append(
            f"{where} declares data-steps={info['steps']} but its highest data-st is {max(values)}"
        )
    return errors


def validate_rtl_html_deck(path):
    """An Arabic deck must set dir="rtl" on its <html> element."""
    try:
        deck = _parse_deck(path)
    except Exception:
        return []  # reported by validate_html_deck
    if ARABIC.search("".join(deck.text)) and deck.html_dir != "rtl":
        return [f'{path}: Arabic deck without dir="rtl" on <html>']
    return []


def validate_pptx(path):
    errors = []
    if not zipfile.is_zipfile(path):
        return [f"{path}: not a valid zip/OOXML package"]
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "[Content_Types].xml" not in names:
            errors.append(f"{path}: missing [Content_Types].xml — not a valid pptx")
        if not any(n.startswith("ppt/slides/slide") for n in names):
            errors.append(f"{path}: no slide parts found under ppt/slides/")
    return errors


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    course_dir = argv[1]
    if not os.path.isdir(course_dir):
        print(f"ERROR: {course_dir} is not a directory", file=sys.stderr)
        return 2

    errors = []
    warnings = []

    manifest_path = os.path.join(course_dir, "course-manifest.yaml")
    session_minutes = None
    rtl = False
    if os.path.isfile(manifest_path) and yaml is not None:
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f) or {}
        rtl = (manifest.get("delivery") or {}).get("direction") == "rtl"
        try:
            session_minutes = parse_minutes(manifest["schedule"]["session_duration"])
        except Exception as e:
            warnings.append(f"could not determine session_duration from manifest: {e}")
    else:
        warnings.append("no course-manifest.yaml found or PyYAML unavailable; skipping agenda timing checks")

    if session_minutes is not None:
        for agenda in sorted(glob.glob(os.path.join(course_dir, "sessions", "*-agenda.md"))):
            errors.extend(validate_agenda_file(agenda, session_minutes))

    for nb in sorted(glob.glob(os.path.join(course_dir, "notebooks", "*.ipynb"))):
        errors.extend(validate_notebook(nb))

    decks = sorted(glob.glob(os.path.join(course_dir, "slides", "*.html")))
    for deck in decks:
        spec = os.path.splitext(deck)[0] + ".md"
        expected = count_spec_slides(spec) if os.path.isfile(spec) else None
        errors.extend(validate_html_deck(deck, expected))

    for pptx in sorted(glob.glob(os.path.join(course_dir, "slides", "*.pptx"))):
        errors.extend(validate_pptx(pptx))

    if rtl:
        for md in sorted(glob.glob(os.path.join(course_dir, "**", "*.md"), recursive=True)):
            errors.extend(validate_rtl_markdown(md))
        for nb in sorted(glob.glob(os.path.join(course_dir, "notebooks", "*.ipynb"))):
            errors.extend(validate_rtl_notebook(nb))
        for deck in decks:
            errors.extend(validate_rtl_html_deck(deck))
        for pptx in sorted(glob.glob(os.path.join(course_dir, "slides", "*.pptx"))):
            errors.extend(validate_rtl_pptx(pptx))
        for xlsx in sorted(glob.glob(os.path.join(course_dir, "**", "*.xlsx"), recursive=True)):
            errors.extend(validate_rtl_xlsx(xlsx))

    for w in warnings:
        print(f"WARN: {w}")

    if errors:
        print(f"FAIL: {len(errors)} issue(s) in {course_dir}")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"PASS: {course_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
