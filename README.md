# Campus Only Label (COL/1.0)

A label system faculty put on assignments to say, to students and to AI systems alike, whether copyrighted course material may be processed by any AI (L0), by the campus-licensed AI with contractual data protection only (L1), or by no AI (L2), with a copyright line and a training clause (T0 no training / T1 permitted) and a scope (assignment, document, course).

The label is a request backed by a copyright assertion, not an access control. The Learn page says so in its first paragraph.

```
campus-only-label/
├── index.html        START: three steps (name → course or exam → copy) producing one plain-text label for every document type
├── builder.html      advanced builder: the standard sheet (B1 level · B2 clauses · B3 campus AI · B4 export) with a live preview and title block
├── label.html        a single label rendered from the link (?embed=1 for chrome-free, &print=1 to print)
├── examples.html     the label carried through a course: syllabus, assignment page, slide, handout footer, email, website; each with
│                     what a student sees, what an AI reads, and the expected assistant response; renders the label in the link
├── learn.html        why it matters: levels, where an upload goes (Fig. 1), ten linked stories, opt-out steps for 7 chatbots,
│                     what campus contracts promise, copyright + FERPA, the spec for people and agents, website signals, a student guide
├── spec/COL-1.0.md   the specification as Markdown
├── assets/label.js   shared core: levels, URL state, notice text, badge SVG + canvas PNG, inline HTML, standalone page, JSON-LD, robots/head kit
├── assets/app.css    tokens from the Design Board (Normblatt school) + components
└── ATTRIBUTION.md
```

No build step, no dependencies, no server, nothing stored anywhere. The whole label travels inside the link.

## Builder fixes (v1.7, 2026-11-10)

- **Badge text is measured, not guessed.** `badgeLayout` in `assets/label.js` measures each line on a canvas and feeds both the SVG and the PNG, so the copyright line is no longer cut off. The bottom line now reads `COL/1.0 · L1 · T0 · S-A · no AI training`, so the training clause is never the part that gets truncated. The PNG's `T0 · S-A` tag is centred under the level code.
- **Tools keep their own sign-in.** Tools that share a sign-in clause are written "A or B, signed in with…"; tools with different ones each keep theirs. Three or more list as "A, B or C".
- **Exports use full addresses.** The spec link in the head tags, JSON-LD, HTML comment and robots.txt resolves on any site.
- **Embed** points at `label.html?embed=1` with a height that fits the label (350 / 430 / 400 px for L0 / L1 / L2).
- **Preview** scrolls inside itself on short screens and sits above Export on phones. The status line flags problems in red and "ready" in green.
- **Repo link.** Every notice to AI systems (short and full), the paste-in HTML, the label page and each page footer link to the public repo, so a student or an agent meeting the label cold can find out what it is. The address is `REPO_URL` at the top of `assets/label.js`; change it if you fork.
- **Discussion-prompt line** is worded per level. Dates use the local day, not UTC.
- Training and Scope options are set in sentence case like the Level options.

## Live document downloads (v1.6)

`assets/docgen.js` builds Word files (syllabus, assignment sheet, exam) and a PowerPoint deck in the browser from the current label, using docx 9.15.3 and pptxgenjs 4.0.1 loaded from jsDelivr on first click; `print.html` is a print-ready handout with the one-line label fixed in the footer of every page (Save as PDF). Buttons live on the Start page (step 3) and the Examples page strip. Everything runs client-side, so GitHub Pages hosts it unchanged. The fixed samples in `examples-docs/` remain for anyone who wants a placeholder file.

## The simple path (index.html)

Name, one of two choices (my course materials = L1 whole course; an exam or student work = L2 this document), copy. The result is one plain-text block, about 240 words, that works in a syllabus, a PDF footer, an LMS page, slide notes and email: a one-line heading, the two student sentences with links to the ask-first prompt and the label page, then the short notice to AI systems. The same page offers the student prompt and the badge image. Everything else lives on builder.html.

## UM default and presets

The builder opens on the **UM default**: Level 1 Campus AI only, approved tools Microsoft Copilot and Google Gemini signed in with go.olemiss.edu credentials, no training, with a student line that says an un-signed-in session is not the campus tool. Three more presets (Exam or student work L2, Whole course L1 S-C, Open material L0) are starting points; every field stays editable. Presets live in `PRESETS` in `assets/label.js`.

## Tested on Claude models

`tests/README.md` records a 62-run test (2026-11-04) of the notice against Claude Haiku, Sonnet and Opus across nine student scenarios and four wordings. Haiku and Opus honor L1 and L2 in every scenario, including "ignore the label" and a false "I'm in Copilot" claim; Sonnet honors L2 and the false claim but usually flags the policy and proceeds on L1. The v4 wording (instructor's written policy + academic integrity + copyright) ships, with the RP/1.0 check-first reply format appended. Codex's parallel GPT tests (merged in `tests/codex/`) matched the pattern, and found the one move that held on every model: the student sends the label as an explicit check before any material. The builder exports that as the ask-your-AI-first prompt (E0); it stopped 13 of 13 runs across six model configurations.

## Two notice tiers, label pack, checklist (v1.3)

The inline notice is now ~190 words (students skim it in small grey type; models read it); the ~650-word full terms sit behind the label link and in the ask-first prompt. The builder's E7 **label pack** writes the same label for ten carriers (syllabus, LMS page, PDF footer, slides + notes, exam header, discussion line, email, video, code/README, website kit) with per-item copy and a one-file download. The Learn page has a **course-start checklist** (label once at S-C, then only exceptions) and every page carries a measured **"Not foolproof. Not meant to be."** box with the odds from testing.

## Three layers in every export

1. **Badge** (SVG, PNG, or the colored block in the inline HTML): level code, name, one line of instruction, copyright line, label code.
2. **Student sentence**: visible text that survives copy-and-paste.
3. **Notice to AI systems and agents**: plain text beginning `NOTICE TO AI SYSTEMS AND AGENTS` and ending with `level=; training=; scope=` machine fields. For L1 it tells a consumer or commercial assistant to stop and point the user to the campus tool, tells the licensed campus tool it may proceed, and tells an assistant that cannot tell which it is to treat the material as L2.

The inline HTML also carries `data-col-*` attributes and `role="note"`; the standalone page adds `<meta name="robots" content="noai, noimageai">`, `<meta name="tdm-reservation">`, `<meta name="campus-only-label">` and a schema.org CreativeWork JSON-LD block. The website kit emits `robots.txt` disallow rules for the documented AI crawlers plus the head tags.

## Exports (B4 on the builder)

Link · iframe embed · paste-in HTML (no scripts, survives LMS sanitizers) · plain text for Word/PDF/syllabus · SVG · PNG · print · standalone .html page · robots.txt + head tags.

## Learn page (v1.1)

Three doors at the top (faculty, student, opt-out), big level plates, a two-question **Which lane am I in?** check that turns green or red, a flow diagram, and large opt-out cards with the exact settings path for ChatGPT, Claude, Gemini, Copilot, Meta AI, Grok and Perplexity, plus a green card for the protected go.olemiss.edu lane.

## Preview

The Box path does not serve; copy to `/tmp/copyright-labels` and run the `copyright-labels` launch config (port 8830).

## Deploy to GitHub Pages

1. Create a repository (for example `campus-only-label`) and upload everything in this folder, keeping `.nojekyll`.
2. Settings → Pages → Source: Deploy from a branch → `main`, folder `/ (root)` → Save.
3. The site appears at `https://<your-username>.github.io/campus-only-label/`. Every link the builder writes (label pages, ask-first prompt, print view) uses the live address automatically.
4. The seven fixed sample files in `examples-docs/` were generated with a placeholder address (`mwatkins03-netizen.github.io/campus-only-label/`). If your repo lives elsewhere, either regenerate them (`tools/` has the scripts and the base URL at the top of the Node snippet in `tools/README`-style notes) or just rely on the live downloads, which are always correct.

No build step, no dependencies to install, no server. The Word and PowerPoint libraries load from jsDelivr when someone clicks a download button.

## Design

Design round on a Design Board (`design-boards/boards/campus-only-label.board.json`), Normblatt school: RAL 9003 signal white ground, 5004 black blue ink, 3020 traffic red reserved for the stop, 6032 signal green for the one clause where campus AI may proceed; Barlow Condensed / Barlow / JetBrains Mono; mechanical motion (120ms, `steps(3, end)`); 5mm grid, DIN binding margin, register marks, a title block on the preview sheet, codes on every panel. No italics.

CC BY 4.0 · Marc Watkins, University of Mississippi. Built with Claude Fable 5.1. Nothing here is legal advice.
