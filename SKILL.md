---
name: translate-academic-pdf-bilingual
description: Translate English academic literature and research-paper PDFs into typeset, polished Simplified Chinese and deliver a page-aligned bilingual PDF with Chinese on the left and the visually unchanged original English page on the right. Precisely detect every formula, crop its original visual appearance, and place the formula image at the corresponding location in the Chinese translation. Append source English abbreviations to translated professional terms and preserve citations, figures, tables, searchable text, Unicode copy order, and non-ligated copying. Use for academic PDF translation, formula-preserving Chinese typesetting, bilingual comparison, OCR, original-layout preservation, or print-ready PDFs.
---

# Academic PDF Bilingual Translation

Produce a faithful, academically polished Chinese translation and a searchable English-Chinese comparison PDF. Treat translation quality, source alignment, and document completeness as separate gates.

## Required outputs

Unless the user requests otherwise, deliver:

1. `<stem>-bilingual.pdf` — primary page-aligned PDF with Chinese on the left and the unchanged English page on the right.
2. `<stem>-bilingual.html` — editable and auditable source for the PDF.
3. `<stem>-terminology.csv` — English term, approved Chinese rendering, first location, notes.
4. `<stem>-qa.json` — extraction, pairing, rendering, and spot-check results.
5. `<stem>-formula-manifest.json` — formula page, bounding box, crop file, capture mode, insertion status, and QA metadata.

Keep intermediate files in a dedicated work directory. Never overwrite the source PDF.

## Workflow

### 1. Inspect the source

- Confirm the PDF opens, page count, text layer availability, page geometry, and whether it is born-digital, scanned, or mixed.
- Detect multi-column layouts, headers, footers, footnotes, equations, tables, figures, captions, references, and supplementary material.
- Detect inline and displayed formulas separately; record each formula's page, exact bounding box, equation number, surrounding text anchor, and reading-order position.
- Use native text extraction first. Apply OCR only to pages or regions without a usable text layer.
- Record source page and block anchors for every extracted paragraph.
- Stop and report if the document is encrypted, corrupt, or extraction quality is too poor for reliable translation.

### 2. Build the source map

- Reconstruct reading order; do not trust raw PDF object order on multi-column pages.
- Remove repeated running headers and footers without removing real body text.
- Preserve section hierarchy and assign stable IDs such as `p003-b012`.
- Keep equations, citation markers, URLs, DOIs, variable names, units, table/figure numbers, and reference entries unchanged unless a localized label is clearly appropriate.
- Extract each figure/table once and associate it with its caption and first substantive discussion.
- Treat every formula as a protected visual asset. Do not rebuild, redraw, translate, or normalize its visible mathematical notation.

### 3. Establish terminology

- Read [references/translation-standard.md](references/translation-standard.md) before translating.
- Sample the title, abstract, keywords, headings, introduction, methods, and conclusion.
- Create the terminology CSV before bulk translation.
- Prefer established Chinese disciplinary terminology.
- For every professional term that has an established or source-defined English abbreviation, write every translated occurrence as `中文术语（ABBR）`, for example `卷积神经网络（CNN）`. Do not drop the abbreviation after the first definition.
- Preserve the abbreviation's source spelling and case. Do not invent an abbreviation when the source and authoritative usage provide none.
- Keep one approved rendering per concept. Update the terminology file deliberately; never allow silent drift.

### 4. Translate and academically polish

Translate by coherent paragraph or short subsection, not isolated PDF lines.

For every unit:

1. Analyze the claim, logic, referents, terminology, and disciplinary register.
2. Draft a faithful Chinese translation.
3. Review against the English for omissions, additions, polarity, quantities, hedging, causality, and citation attachment.
4. Polish into natural academic Chinese without strengthening claims or inventing interpretation.
5. Preserve the stable source anchor.

Do not summarize, simplify away qualifications, fabricate missing text, translate formulas or code, or silently repair a suspected source error. Flag uncertain text in the QA report.

For formulas, translate only the surrounding prose. Insert the exact source formula crop at the corresponding logical position in the Chinese text.

### 5. Assemble the bilingual document

- Read [references/output-spec.md](references/output-spec.md).
- Read [references/chinese-typesetting.md](references/chinese-typesetting.md) and apply it to the complete left Chinese panel.
- Read [references/formula-capture.md](references/formula-capture.md) and insert every detected formula crop into the left Chinese panel.
- Default to two equal page panels: polished Chinese on the left and the original English page on the right.
- Keep the right panel visually identical to the source page, including line breaks, columns, fonts, equations, figures, tables, headers, footers, and page numbers. Do not reflow or re-typeset its visible content.
- Align each Chinese panel to the corresponding English source page. Keep the same section and reading sequence; use region-level alignment within the Chinese panel when practical.
- Use [assets/bilingual-paper.css](assets/bilingual-paper.css) as the base print stylesheet.
- Preserve title, authors, affiliations, abstract, headings, body, acknowledgements, declarations, references, figures, tables, captions, and appendices.
- Show a subtle source-page anchor for each pair.
- Place each figure/table once, followed by its English caption and Chinese caption.
- Place each formula crop once at the matching Chinese anchor; preserve its original equation number inside the crop when present.
- Do not duplicate reference lists; preserve the original reference entries and translate only section labels unless requested.

### 6. Export PDF

- Read [references/text-layer.md](references/text-layer.md) before building or validating the PDF.
- Render source pages with Poppler or the bundled PDF runtime and crop formulas from the rendered page or original vector page according to [references/formula-capture.md](references/formula-capture.md).
- Prefer direct PDF composition for the unchanged English panel. Reuse the original page as a vector/form layer when its Unicode text mapping passes copy tests. Otherwise use an exact page rendering as the visible layer and add a reconstructed transparent Unicode text layer.
- Normalize English ligatures to separate characters and position selectable text in reading order. Do not rely on visual glyph substitution for copyable content.
- Disable discretionary, standard, contextual, and historical ligatures in generated text. Require valid `ToUnicode` mappings for embedded fonts.
- Use the precise crop as the authoritative visible formula in the Chinese panel. Add a character- or token-level Unicode text layer only when extraction is reliable; never replace the crop with re-typeset mathematics.
- Use the workspace's supported document/PDF runtime. Load workspace dependencies when available rather than installing packages.
- Embed or select fonts containing Simplified Chinese glyphs.
- Enable background graphics, print CSS, bookmarks/headings when supported, and consistent A4 margins.
- Never rasterize the full deliverable unless the user explicitly requests an image-only facsimile.

### 7. Validate

- Represent paragraph pairs in JSON and validate them against the terminology CSV:

  `python scripts/validate_bilingual.py <pairs.json> --terminology <stem>-terminology.csv --formula-manifest <stem>-formula-manifest.json --report <stem>-qa.json`

- Visually inspect the first page, one dense body page, one equation page, one figure/table page, and the last page.
- Check every page for clipped text, missing glyphs, overlaps, blank pages, broken equations, orphan captions, and unreadably small text.
- Copy-test representative English prose containing `fi`, `fl`, `ff`, and punctuation. The pasted result must contain separate Unicode characters, not presentation ligatures or joined words.
- Copy-test at least three formulas. Selection and paste order must follow the formula's logical character order; do not accept a single joined ligature glyph where separate characters exist.
- Compare every Chinese-panel formula crop with the corresponding source bounding box. Reject clipped operators, missing superscripts/subscripts, lost delimiters, altered equation numbers, surrounding prose inside the crop, blur, or unintended scaling distortion.
- Confirm every formula-manifest entry has a non-empty crop file and is inserted exactly once at its Chinese anchor.
- Confirm that the right panel matches the source page visually and that the left/right page mapping is one-to-one.
- Confirm every glossary term with an abbreviation appears as `中文术语（ABBR）` throughout the Chinese translation.
- Inspect Chinese hierarchy, paragraph indentation, justification, line spacing, punctuation, citation attachment, heading breaks, widow/orphan control, and formula alignment.
- Spot-check at least the title, abstract, one methods paragraph, one results paragraph, and the conclusion against the source.
- Do not claim completion while the validator reports errors or visual defects remain.

## Pair JSON contract

Use this minimal structure for validation:

```json
{
  "source_file": "paper.pdf",
  "source_pages": 12,
  "pairs": [
    {
      "id": "p001-b001",
      "page": 1,
      "kind": "title",
      "source": "English source text",
      "translation": "中文学术译文"
    }
  ]
}
```

Allowed `kind` values are open-ended; common values are `title`, `heading`, `paragraph`, `caption`, `footnote`, and `table-cell`.

## Quality priorities

Resolve trade-offs in this order:

1. No missing or invented meaning.
2. Correct terminology, quantities, polarity, and claim strength.
3. Exact source-to-translation alignment and traceability.
4. Natural, publication-quality academic Chinese.
5. Readable, stable PDF layout.

If the original layout cannot be preserved without harming bilingual readability, preserve content structure and figures rather than pixel-level geometry, and disclose the change.

