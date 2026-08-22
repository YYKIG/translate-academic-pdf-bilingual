# Formula Detection, Capture, and Placement

## Detection

- Detect both inline and displayed formulas from PDF text operators, font/symbol patterns, layout geometry, and rendered-page inspection.
- Inspect every source page visually after automated detection. Add missed formulas and remove false positives such as page numbers, ordinary italic words, units, and reference labels.
- Assign each formula a stable ID such as `eq-p003-002` and record:
  - source page;
  - PDF-coordinate bounding box `[x0, y0, x1, y1]`;
  - `inline` or `display` kind;
  - equation number when present;
  - preceding and following source anchors;
  - crop filename and capture mode.

## Capture

- Prefer a vector clip from the original PDF when it preserves appearance exactly.
- Otherwise render the source page at 600 DPI; use at least 300 DPI only when 600 DPI is impractical.
- Crop to the tight formula bounding box plus 2–4 px safety padding at the final raster scale.
- Include the equation number in the same crop when it is visually part of the displayed equation.
- Exclude surrounding English prose, headers, footers, unrelated labels, rules, and adjacent equations.
- Preserve the original foreground and background. Do not sharpen, denoise, recolor, erase, reconstruct, or typeset the formula.
- Save losslessly as PNG. Allow SVG or clipped PDF only for true vector captures.

## Placement in Chinese translation

- Insert the crop immediately after the translated sentence or clause that precedes the source formula.
- Center displayed formulas. Align inline formulas to the Chinese text baseline and scale them only uniformly.
- Preserve aspect ratio. Never stretch width and height independently.
- Do not enlarge beyond the formula's effective source resolution; reduce size only if necessary to fit the Chinese panel.
- Insert every formula exactly once. Do not reuse one crop for visually similar formulas.
- Preserve source equation numbering; do not generate a new Chinese equation number.

## Formula manifest

Write `<stem>-formula-manifest.json`:

```json
{
  "formulas": [
    {
      "id": "eq-p003-002",
      "page": 3,
      "bbox": [72.1, 312.4, 481.6, 368.9],
      "kind": "display",
      "equation_number": "(2)",
      "source_anchor": "p003-b008",
      "crop_file": "formula-crops/eq-p003-002.png",
      "capture_mode": "raster_crop",
      "render_dpi": 600,
      "inserted": true
    }
  ]
}
```

Use `capture_mode` values `raster_crop` or `vector_clip`. For vector clips, omit `render_dpi`.

## Visual QA

- Render the completed bilingual PDF to PNG with Poppler.
- Compare every inserted crop against its source region at high zoom.
- Reject a crop if any symbol, accent, fraction bar, radical, matrix bracket, delimiter, superscript, subscript, or equation number is clipped or altered.
- Reject blur, pixelation at normal zoom, non-uniform scaling, accidental borders, duplicated formulas, or surrounding prose in the crop.
- Record detection count, inserted count, missing count, duplicates, and every exception in QA.

