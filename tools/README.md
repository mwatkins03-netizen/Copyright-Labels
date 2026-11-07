# tools/

Generators for the fixed sample documents in `../examples-docs/`.

- `gen_docx.py OUT` builds the three Word files from `labels.json` and the badge PNGs (needs `python-docx`).
- `gen_rest.py OUT` builds the PDF handout (needs `reportlab`), the PowerPoint deck (needs `python-pptx`), the LMS page and the email text.
- `labels.json` is produced from `../assets/label.js` in Node; the base URL baked into the links is the `BASE` constant in that snippet (see the session notes in `../tests/README.md` for the one-liner). Change it to your Pages address and regenerate.
- `badge-*.png` were rasterized from the builder's SVG with headless Chrome.

The live downloads on the site do not use any of this; they are generated in the browser by `../assets/docgen.js`.
