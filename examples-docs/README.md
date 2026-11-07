# Example documents with the label embedded

Generated 2026-11-07 from the label core (`assets/label.js`) by `tools/gen_docx.py` and `tools/gen_rest.py`. Each file carries a yellow "Instructions for faculty" box saying where the label goes; delete it before sharing.

- `01-syllabus-with-label.docx` — Syllabus (Word): Once, under the AI policy heading, at whole-course scope. One-line version in the page footer.
- `02-assignment-sheet-with-label.docx` — Assignment sheet (Word): After the directions, before the submission instructions. One-line version in the footer.
- `03-exam-with-label.docx` — Exam or student work (Word): A separate No AI processing label: top of page one and the footer of every page.
- `04-reading-handout-with-label.pdf` — Reading handout (PDF): Footer of every page in small type; the full block once on page one.
- `05-slides-with-label.pptx` — Slide deck (PowerPoint): Badge in the footer of the title and last slides; the label as text on the last slide; the notice in the speaker notes.
- `06-lms-assignment-page.html` — LMS assignment page (HTML): Paste the HTML export after the directions and before the submission box; check that the grey text survived saving.
- `07-email-announcement.txt` — Email or announcement (plain text): Two sentences and the links in the body; the notice under a divider at the end.

Regenerate after a label change: `python3 tools/gen_docx.py examples-docs && python3 tools/gen_rest.py examples-docs` from the `tools/` folder with `labels.json` and the badge PNGs present.
