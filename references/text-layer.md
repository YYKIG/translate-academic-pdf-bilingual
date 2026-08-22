# Copyable English and Formula Text Layer

## Rendering model

Separate appearance from selection when necessary:

1. Preserve the original English page as the visible right-panel layer.
2. Reuse its native text only when character mapping, reading order, and copy/paste tests pass.
3. Otherwise flatten only the visible English appearance and overlay transparent Unicode text at the original coordinates.
4. Keep the overlay invisible but selectable; do not create duplicate selectable layers.

## Character mapping

- Embed fonts with complete `ToUnicode` CMaps.
- Normalize compatibility and presentation ligatures before writing the text layer:
  - `ﬀ` → `ff`
  - `ﬁ` → `fi`
  - `ﬂ` → `fl`
  - `ﬃ` → `ffi`
  - `ﬄ` → `ffl`
  - `ﬅ` → `ft`
  - `ﬆ` → `st`
- Disable OpenType ligature substitution: `liga=0`, `clig=0`, `dlig=0`, `hlig=0`.
- Preserve real spaces, hyphens, paragraph boundaries, and reading order. Remove soft line-end hyphens only when the source word is semantically continuous.
- Position prose at word or character granularity. Never encode an entire line, formula, or paragraph as a single glyph/string object solely to mimic appearance.

## Formulas

- Preserve the formula's visible vector or raster crop unchanged and use it as the visible formula in the Chinese panel.
- Build the selectable layer from source PDF text operators, MathML/LaTeX source, or careful OCR, in that preference order.
- Map Latin and Greek letters, digits, operators, superscripts, subscripts, parentheses, and delimiters to Unicode when reliable.
- Store selection content in logical mathematical order rather than paint order.
- Do not invent inaccessible symbols. Mark unreliable formula regions in QA with page number, bounding box, and reason.
- Keep the selectable overlay aligned with the crop, but never let OCR or inferred text alter the visible crop.

## Copy tests

Test pasted plain text, not only visual selection:

1. Select a normal English sentence across a line break.
2. Select words containing `office`, `figure`, `flow`, `effect`, and `affiliation` when present.
3. Verify pasted text contains ordinary characters such as `f` + `i`, never `ﬁ`.
4. Select three representative formulas: inline, displayed, and symbol-dense.
5. Compare pasted characters and their order with the visible formula.
6. Check that selection does not capture the same text twice.

Record every failure in the QA report and do not label the output fully copyable until the failures are fixed or explicitly disclosed.

