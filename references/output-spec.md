# Bilingual PDF Output Specification

## Default layout

Use a two-page spread for every source page:

1. Put the polished Chinese page in the left panel.
2. Put the visually unchanged original English page in the right panel.
3. Use a landscape sheet whose aspect ratio fits two source pages at equal scale. For an A4 source, default to A3 landscape.
4. Map spread `N` to source page `N`; do not shift the original page to a different spread.
5. Keep both panels equal in size and separate them with a narrow gutter and rule.

The right panel is a facsimile, not a reconstructed approximation. Preserve its visual geometry exactly. Never change its visible line breaks, columns, pagination, fonts, equations, figures, tables, headers, footers, or whitespace.

Flow the complete translation inside the left panel. Preserve source reading order and use subtle region markers where the Chinese length prevents exact line-level alignment. Continue overflow in a clearly labeled left-panel continuation spread while repeating or referencing the corresponding right source page; never shrink Chinese below the minimum readable size.

## Document order

1. Bilingual title and source metadata
2. Terminology note, if necessary
3. Abstract and keywords
4. Main sections in source order
5. Figures and tables near their first substantive discussion
6. Acknowledgements, declarations, data/code availability
7. References
8. Appendices and supplementary text included in the source

## Figures and tables

- Preserve the original figure/table exactly in the right English panel.
- In the left Chinese panel, reproduce the figure/table only when needed for direct comprehension; otherwise use its number and translated caption with a clear pointer to the right panel.
- Preserve table values exactly. Translate textual headers and notes with the same terminology ledger.
- If a table is too wide, use landscape orientation for that page or place it as a full-width block; do not shrink below legibility.

## Formulas

- Apply [formula-capture.md](formula-capture.md).
- Use the source formula crop as the authoritative visual representation in the left Chinese panel.
- Preserve formula symbols, spacing, fraction bars, radical extents, matrices, superscripts, subscripts, accents, delimiters, and equation numbers exactly.
- Insert each crop at the logical location of the formula in the translated paragraph sequence.
- Do not re-typeset a formula from OCR, LaTeX inference, or Unicode reconstruction.

## Typography

- Apply [chinese-typesetting.md](chinese-typesetting.md) to the left panel.
- Use an available serif family for English and a Simplified Chinese serif family for Chinese.
- Minimum body size: 9.5 pt for print; prefer 10.5–11 pt.
- Use 1.35–1.55 line height and visible separation between pairs.
- Do not use color alone to distinguish languages.
- Disable ligatures in every generated selectable text layer with `font-variant-ligatures: none` and OpenType `liga`, `clig`, `dlig`, and `hlig` disabled.
- Keep `中文术语（ABBR）` together when practical; do not leave the abbreviation alone at the start of a new line.

## PDF acceptance criteria

- Searchable and selectable English and Chinese text.
- English is copied in logical reading order with decomposed Unicode characters; `fi`, `fl`, `ff`, and similar sequences must not paste as ligature presentation characters.
- Formulas retain correct visible layout and provide the most granular reliable Unicode selection layer; QA identifies any formula that cannot be copied accurately.
- Every detected formula has a validated crop and appears exactly once in the Chinese panel at the correct source anchor.
- The right panel is visually unchanged from the source page.
- Correct Simplified Chinese glyphs with no tofu boxes.
- Chinese text follows the defined academic hierarchy and every glossary-controlled professional term carries its English abbreviation.
- No clipping, overlap, missing pages, blank trailing pages, or orphan captions.
- Page numbers and section hierarchy are visible.
- Source anchors allow a reader to trace the translation back to the original page.
- Metadata includes the original title and identifies the file as an AI-assisted translation requiring scholarly verification where appropriate.

