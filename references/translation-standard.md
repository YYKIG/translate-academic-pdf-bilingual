# Academic English-to-Chinese Translation Standard

## Fidelity

- Preserve the proposition, logical relation, scope, modality, negation, comparison, and evidential status of every sentence.
- Preserve hedging: distinguish `may`, `might`, `suggest`, `indicate`, `demonstrate`, and `prove`.
- Preserve tense when it carries methodological or evidential meaning.
- Keep all numbers, statistical symbols, confidence intervals, p-values, units, ranges, and signs exact.
- Keep citations attached to the claim they support.
- Never add background knowledge to the translation. Put indispensable clarification in an explicitly marked translator note.

## Academic Chinese

- Prefer precise, conventional disciplinary language over literal English syntax.
- Reconstruct long sentences when necessary, while retaining logical dependencies.
- Avoid conversational fillers, promotional language, empty intensifiers, and mechanical “的” chains.
- Use consistent names for methods, datasets, instruments, constructs, and variables.
- Preserve authorial stance and do not upgrade correlation to causation or possibility to certainty.

## Terminology

- Prefer terminology used in Chinese standards, authoritative textbooks, or mainstream disciplinary publications.
- For a professional term with an established or source-defined English abbreviation, render every Chinese occurrence as `中文术语（ABBR）`; do not limit the suffix to first occurrence.
- Use full-width Chinese parentheses around the abbreviation and preserve the abbreviation's exact source case, digits, hyphens, and punctuation.
- If the source supplies both a full English term and an abbreviation, store both but display the abbreviation after the Chinese term, for example `大型语言模型（LLM）`, not `大型语言模型（large language model）`.
- If no accepted abbreviation exists, do not fabricate one. For an uncommon or ambiguous term, use `中文术语（full English term）` on first occurrence only, then the approved Chinese term.
- Do not attach abbreviations to ordinary vocabulary, proper names, chemical formulas, gene symbols, model names, dataset names, or units unless they function as a defined professional term in the paper.
- Preserve product names, dataset names, model names, code identifiers, gene/protein symbols, chemical formulas, and Latin taxonomic names unless an authoritative Chinese name is required.
- Record each decision in the terminology CSV with these columns:

  `source_term,target_term,abbreviation,first_anchor,keep_english,notes`

## Protected content

Do not translate or alter:

- equations and inline mathematical notation;
- code, commands, file paths, URLs, DOI strings, accession numbers, and identifiers;
- bibliography entries, except a user-requested translated-title annotation;
- variable names, table values, figure labels embedded in images, and measurement units.

Translate surrounding labels such as “Figure”, “Table”, “Appendix”, and “Supplementary” consistently.

## Review checklist

For each translated unit, check:

1. Every source claim is present exactly once.
2. No new causal, evaluative, or explanatory claim was introduced.
3. Negation, comparison direction, magnitude, and uncertainty match.
4. Pronouns and references resolve to the same entity.
5. Terminology matches the approved glossary and every abbreviation-bearing target term uses `中文术语（ABBR）`.
6. Citations, equations, numbers, and units are intact.
7. Chinese reads as edited academic prose rather than translationese.

