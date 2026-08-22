# Chinese Academic Typesetting

## Page and panel

- Typeset only the left Chinese panel; never change the right original English panel.
- Use the full available left-panel width with 4–6 mm internal padding.
- Keep at least 9.5 pt body text. Prefer 10.5–11 pt; never reduce type merely to force one-to-one page height.
- Continue overflow on a labeled Chinese continuation spread and retain the source-page reference.

## Fonts and hierarchy

- Prefer `Source Han Serif SC` or `Noto Serif CJK SC`; fall back to `SimSun`.
- Use `Source Han Sans SC`, `Noto Sans CJK SC`, or `Microsoft YaHei` for headings when available.
- Typeset the translated title at 18–20 pt, bold, centered, with no first-line indent.
- Typeset level-1 headings at 14–15 pt bold, level-2 at 12–13 pt bold, and level-3 at 11–12 pt semibold.
- Keep a heading with at least two following lines; never leave a heading at the bottom of a page.

## Body paragraphs

- Use 1.45–1.55 line height, justified alignment, and a two-Chinese-character first-line indent (`2em`).
- Do not indent the first paragraph after a heading, displayed equation, figure, or table.
- Use 0.35–0.55em paragraph spacing; do not insert blank paragraphs for spacing.
- Set widow and orphan control to at least two lines, preferably three.
- Use Chinese punctuation and full-width parentheses for Chinese prose. Keep Latin abbreviations, variables, DOI strings, URLs, and units half-width.
- Avoid forced spaces between Chinese and Latin text. Use font metrics or CSS spacing rather than literal spaces.

## Professional terms

- Wrap glossary-controlled terms in a `.term` span and render them as `中文术语（ABBR）` at every occurrence.
- Keep the Chinese term and its abbreviation on the same line when practical with `white-space: nowrap`; allow a break before the complete term when needed.
- Preserve source capitalization: `人工智能（AI）`, `大型语言模型（LLM）`, `支持向量机（SVM）`.
- Do not generate abbreviations for terms without an established or source-defined abbreviation.

## Abstract, keywords, citations, and notes

- Label the abstract as `摘要` and use a slightly smaller or equal body size with no first-line indent.
- Label keywords as `关键词：`; separate Chinese keywords with semicolons.
- Preserve citation style and keep citation markers attached to the translated claim.
- Use 8.5–9 pt for footnotes, translator notes, figure captions, and table notes.
- Mark translator notes explicitly as `译者注：`; do not mix them into the author's prose.

## Equations, figures, and tables

- Insert formula captures according to [formula-capture.md](formula-capture.md); do not re-typeset them.
- Center displayed formula captures and preserve the equation number inside the crop.
- Align inline formula captures to the surrounding Chinese baseline and prevent clipping above or below the line box.
- Keep a displayed formula capture with the preceding explanatory line and at least one following line when practical.
- Use `图 N` and `表 N` consistently. Put the Chinese caption below figures and above tables unless the source convention must be retained.
- Repeat table headers after page breaks when supported. Never split a short table row across pages.

## Acceptance checks

- No clipped Chinese glyphs, tofu boxes, overlaps, crowded lines, isolated headings, or dangling one-line paragraphs.
- All headings have consistent levels and spacing.
- Paragraph indents, alignment, line spacing, captions, notes, citations, and formulas follow one consistent style.
- Every formula crop is sharp, complete, correctly anchored, and free of surrounding English prose.
- Every glossary-controlled abbreviation-bearing term appears as `中文术语（ABBR）`.

