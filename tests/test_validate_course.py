"""
Tests for scripts/validate_course.py — agenda timing, notebook JSON
validity, and slide-deck (HTML, pptx) structural validity (docs/specification.md §35: "Agenda timing",
"Output structure").
"""
import json
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import validate_course as vc  # noqa: E402


def write(tmp_path, name, content):
    p = os.path.join(tmp_path, name)
    with open(p, "w") as f:
        f.write(content)
    return p


def test_agenda_sums_correctly(tmp_path):
    content = (
        "# Session 1 Agenda\n\n"
        "| Block | Component | Minutes | Running Total |\n"
        "|---|---|---|---|\n"
        "| 1 | Opening | 10 | 10 |\n"
        "| 2 | Explanation | 50 | 60 |\n"
        "| 3 | Break | 10 | 70 |\n"
        "| 4 | Practice | 50 | 120 |\n"
    )
    path = write(str(tmp_path), "agenda.md", content)
    errors = vc.validate_agenda_file(path, 120)
    assert errors == []


def test_agenda_mismatch_detected(tmp_path):
    content = (
        "| 1 | Opening | 10 | 10 |\n"
        "| 2 | Explanation | 50 | 60 |\n"
    )
    path = write(str(tmp_path), "agenda.md", content)
    errors = vc.validate_agenda_file(path, 120)
    assert len(errors) == 1
    assert "60" in errors[0] and "120" in errors[0]


def test_agenda_no_rows_detected(tmp_path):
    path = write(str(tmp_path), "agenda.md", "no table here\n")
    errors = vc.validate_agenda_file(path, 120)
    assert any("no parseable agenda rows" in e for e in errors)


def _minimal_nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": cells,
    }


def test_valid_notebook_passes(tmp_path):
    nb = _minimal_nb([
        {"cell_type": "markdown", "metadata": {}, "source": ["# Title"]},
        {"cell_type": "code", "metadata": {}, "source": ["print(1)"], "outputs": []},
    ])
    path = os.path.join(str(tmp_path), "session-01-instructor.ipynb")
    with open(path, "w") as f:
        json.dump(nb, f)
    assert vc.validate_notebook(path) == []


def test_notebook_wrong_nbformat_detected(tmp_path):
    nb = _minimal_nb([{"cell_type": "markdown", "metadata": {}, "source": ["x"]}])
    nb["nbformat"] = 3
    path = os.path.join(str(tmp_path), "nb.ipynb")
    with open(path, "w") as f:
        json.dump(nb, f)
    errors = vc.validate_notebook(path)
    assert any("nbformat must be 4" in e for e in errors)


def test_notebook_missing_cells_key_detected(tmp_path):
    path = os.path.join(str(tmp_path), "nb.ipynb")
    with open(path, "w") as f:
        json.dump({"nbformat": 4, "metadata": {}}, f)
    errors = vc.validate_notebook(path)
    assert any("cells" in e for e in errors)


def test_notebook_code_cell_missing_outputs_detected(tmp_path):
    nb = _minimal_nb([
        {"cell_type": "code", "metadata": {}, "source": ["1+1"]},
    ])
    path = os.path.join(str(tmp_path), "nb.ipynb")
    with open(path, "w") as f:
        json.dump(nb, f)
    errors = vc.validate_notebook(path)
    assert any("outputs" in e for e in errors)


def test_student_notebook_with_solutions_flagged(tmp_path):
    nb = _minimal_nb([
        {"cell_type": "markdown", "metadata": {}, "source": ["## Solutions\nhere"]},
    ])
    path = os.path.join(str(tmp_path), "session-01-student.ipynb")
    with open(path, "w") as f:
        json.dump(nb, f)
    errors = vc.validate_notebook(path)
    assert any("Solutions" in e for e in errors)


def test_invalid_json_notebook_detected(tmp_path):
    path = os.path.join(str(tmp_path), "nb.ipynb")
    with open(path, "w") as f:
        f.write("{not valid json")
    errors = vc.validate_notebook(path)
    assert any("not valid JSON" in e for e in errors)


def test_valid_pptx_passes(tmp_path):
    path = os.path.join(str(tmp_path), "deck.pptx")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("ppt/slides/slide1.xml", "<slide/>")
    assert vc.validate_pptx(path) == []


def test_pptx_missing_content_types_detected(tmp_path):
    path = os.path.join(str(tmp_path), "deck.pptx")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("ppt/slides/slide1.xml", "<slide/>")
    errors = vc.validate_pptx(path)
    assert any("Content_Types" in e for e in errors)


def test_pptx_not_a_zip_detected(tmp_path):
    path = os.path.join(str(tmp_path), "deck.pptx")
    with open(path, "w") as f:
        f.write("not a zip file")
    errors = vc.validate_pptx(path)
    assert any("not a valid zip" in e for e in errors)


DECK = (
    '<!DOCTYPE html><html lang="{lang}"{dir}><head><style>.slide{{}}</style></head><body>'
    "{slides}<script>var n = 1;</script></body></html>"
)


def _deck(tmp_path, name, slides, lang="en", direction="", extra=""):
    body = "".join(f'<section class="slide"><h1>{s}</h1></section>' for s in slides) + extra
    d = f' dir="{direction}"' if direction else ""
    return write(str(tmp_path), name, DECK.format(lang=lang, dir=d, slides=body))


def test_valid_html_deck_passes(tmp_path):
    path = _deck(tmp_path, "deck.html", ["One", "Two"])
    assert vc.validate_html_deck(path) == []
    assert vc.validate_html_deck(path, expected_slides=2) == []


def test_html_deck_slide_count_mismatch_detected(tmp_path):
    path = _deck(tmp_path, "deck.html", ["One", "Two"])
    errors = vc.validate_html_deck(path, expected_slides=3)
    assert any("spec has 3" in e for e in errors)


def test_html_deck_without_slides_detected(tmp_path):
    path = write(str(tmp_path), "deck.html", "<html><body><p>hi</p></body></html>")
    assert any("no <section" in e for e in vc.validate_html_deck(path))
    plain = write(str(tmp_path), "plain.html", "just text")
    assert any("no <html>" in e for e in vc.validate_html_deck(plain))


def test_html_deck_external_assets_detected(tmp_path):
    extra = '<script src="https://cdn.example/x.js"></script><link rel="stylesheet" href="a.css">'
    path = _deck(tmp_path, "deck.html", ["One"], extra=extra)
    errors = vc.validate_html_deck(path)
    assert len([e for e in errors if "self-contained" in e]) == 2


def test_count_spec_slides(tmp_path):
    spec = write(str(tmp_path), "s.md", "# Spec\n\n## Slide 1: A\n\n- x\n\n## Slide 2: B\n")
    assert vc.count_spec_slides(spec) == 2


def test_rtl_html_deck_requires_dir(tmp_path):
    good = _deck(tmp_path, "g.html", ["مرحبا"], lang="ar", direction="rtl")
    bad = _deck(tmp_path, "b.html", ["مرحبا"], lang="ar")
    english = _deck(tmp_path, "e.html", ["Hello"])
    assert vc.validate_rtl_html_deck(good) == []
    assert vc.validate_rtl_html_deck(bad)
    assert vc.validate_rtl_html_deck(english) == []


def test_parse_minutes():
    assert vc.parse_minutes("2h") == 120.0
    assert vc.parse_minutes("90m") == 90.0
    assert vc.parse_minutes(45) == 45.0


# --- Right-to-left (Arabic) checks: references/localization/arabic-rtl.md ---

def test_rtl_markdown_requires_wrapper(tmp_path):
    bad = write(str(tmp_path), "bad.md", "# عنوان\n\nنص عربي\n")
    good = write(str(tmp_path), "good.md", '<div dir="rtl">\n\n# عنوان\n\nنص عربي\n\n</div>\n')
    english = write(str(tmp_path), "en.md", "# Title\n\nEnglish only\n")
    assert vc.validate_rtl_markdown(bad)
    assert vc.validate_rtl_markdown(good) == []
    assert vc.validate_rtl_markdown(english) == []


def test_rtl_notebook_markdown_cells(tmp_path):
    nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": ["# عنوان"]},
        {"cell_type": "markdown", "metadata": {}, "source": ['<div dir="rtl">\n\nشرح\n\n</div>']},
        {"cell_type": "code", "metadata": {}, "source": ["print('hi')"], "outputs": [], "execution_count": None},
    ]}
    path = write(str(tmp_path), "nb.ipynb", json.dumps(nb, ensure_ascii=False))
    errors = vc.validate_rtl_notebook(path)
    assert len(errors) == 1 and "cell 0" in errors[0]


def _zip(path, files):
    with zipfile.ZipFile(path, "w") as z:
        for name, data in files.items():
            z.writestr(name, data)


def test_rtl_pptx_paragraphs(tmp_path):
    good = '<p:sld><a:p><a:pPr rtl="1" algn="r"/><a:r><a:t>مرحبا</a:t></a:r></a:p><a:p><a:r><a:t>Hello</a:t></a:r></a:p></p:sld>'
    bad = '<p:sld><a:p><a:pPr algn="r"/><a:r><a:t>مرحبا</a:t></a:r></a:p></p:sld>'
    gp, bp = os.path.join(str(tmp_path), "g.pptx"), os.path.join(str(tmp_path), "b.pptx")
    _zip(gp, {"ppt/slides/slide1.xml": good})
    _zip(bp, {"ppt/slides/slide1.xml": bad})
    assert vc.validate_rtl_pptx(gp) == []
    assert vc.validate_rtl_pptx(bp)


def test_rtl_xlsx_sheet_direction(tmp_path):
    gp, bp = os.path.join(str(tmp_path), "g.xlsx"), os.path.join(str(tmp_path), "b.xlsx")
    _zip(gp, {"xl/worksheets/sheet1.xml": '<worksheet><sheetViews><sheetView rightToLeft="1" workbookViewId="0"/></sheetViews></worksheet>'})
    _zip(bp, {"xl/worksheets/sheet1.xml": '<worksheet><sheetViews><sheetView workbookViewId="0"/></sheetViews></worksheet>'})
    assert vc.validate_rtl_xlsx(gp) == []
    assert vc.validate_rtl_xlsx(bp)


def test_rtl_pptx_checks_layouts(tmp_path):
    bad_layout = '<p:sldLayout><a:p><a:pPr algn="r"/><a:r><a:t>تذييل</a:t></a:r></a:p></p:sldLayout>'
    path = os.path.join(str(tmp_path), "l.pptx")
    _zip(path, {"ppt/slides/slide1.xml": "<p:sld/>", "ppt/slideLayouts/slideLayout1.xml": bad_layout})
    errors = vc.validate_rtl_pptx(path)
    assert errors and "slideLayout1" in errors[0]
