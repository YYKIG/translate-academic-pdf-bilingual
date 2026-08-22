#!/usr/bin/env python3
"""Validate paragraph-aligned bilingual paper JSON and write a QA report."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ANCHOR_RE = re.compile(r"^p(?P<page>\d{3,})-b\d{3,}$")
FORMULA_ID_RE = re.compile(r"^eq-p(?P<page>\d{3,})-\d{3,}$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LIGATURE_RE = re.compile(r"[\ufb00-\ufb06]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Pair JSON to validate")
    parser.add_argument("--terminology", type=Path, help="Terminology CSV with target_term and abbreviation columns")
    parser.add_argument("--formula-manifest", type=Path, help="Formula capture manifest JSON")
    parser.add_argument("--report", type=Path, help="Write QA JSON here")
    return parser.parse_args()


def load_terminology(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"target_term", "abbreviation"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError("terminology CSV missing columns: " + ", ".join(sorted(missing)))
        return [
            {"target_term": (row.get("target_term") or "").strip(),
             "abbreviation": (row.get("abbreviation") or "").strip()}
            for row in reader
            if (row.get("target_term") or "").strip() and (row.get("abbreviation") or "").strip()
        ]


def abbreviation_violations(text: str, terms: list[dict[str, str]]) -> list[str]:
    violations: list[str] = []
    for term in terms:
        target = term["target_term"]
        abbreviation = term["abbreviation"]
        occurrences = len(re.findall(re.escape(target), text))
        compliant = len(re.findall(
            re.escape(target) + r"\s*[（(]\s*" + re.escape(abbreviation) + r"\s*[）)]",
            text,
        ))
        if occurrences != compliant:
            violations.append(f"{target}（{abbreviation}）: {occurrences - compliant} occurrence(s) missing abbreviation")
    return violations


def validate_formula_manifest(path: Path, source_pages: int | None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"count": 0, "inserted": 0, "errors": [str(exc)], "warnings": []}

    formulas = data.get("formulas") if isinstance(data, dict) else None
    if not isinstance(formulas, list):
        return {"count": 0, "inserted": 0, "errors": ["formula manifest must contain a formulas array"], "warnings": []}

    ids: list[str] = []
    inserted_count = 0
    allowed_suffixes = {".png", ".svg", ".pdf"}
    manifest_root = path.parent.resolve()

    for index, formula in enumerate(formulas):
        label = f"formulas[{index}]"
        if not isinstance(formula, dict):
            errors.append(f"{label} must be an object")
            continue

        formula_id = formula.get("id")
        page = formula.get("page")
        bbox = formula.get("bbox")
        kind = formula.get("kind")
        crop_file = formula.get("crop_file")
        capture_mode = formula.get("capture_mode")
        inserted = formula.get("inserted")

        match = FORMULA_ID_RE.match(formula_id) if isinstance(formula_id, str) else None
        if not match:
            errors.append(f"{label}.id must match eq-pNNN-NNN")
        else:
            ids.append(formula_id)
            if isinstance(page, int) and int(match.group("page")) != page:
                errors.append(f"{formula_id}: id page and page field differ")

        if not isinstance(page, int) or page < 1:
            errors.append(f"{label}.page must be a positive integer")
        elif isinstance(source_pages, int) and page > source_pages:
            errors.append(f"{label}.page exceeds source_pages")

        valid_bbox = (
            isinstance(bbox, list) and len(bbox) == 4
            and all(isinstance(value, (int, float)) for value in bbox)
            and bbox[2] > bbox[0] and bbox[3] > bbox[1]
        )
        if not valid_bbox:
            errors.append(f"{label}.bbox must be [x0, y0, x1, y1] with positive area")

        if kind not in {"inline", "display"}:
            errors.append(f"{label}.kind must be inline or display")
        if capture_mode not in {"raster_crop", "vector_clip"}:
            errors.append(f"{label}.capture_mode must be raster_crop or vector_clip")
        if capture_mode == "raster_crop":
            render_dpi = formula.get("render_dpi")
            if not isinstance(render_dpi, (int, float)) or render_dpi < 300:
                errors.append(f"{label}.render_dpi must be at least 300 for raster crops")

        if inserted is not True:
            errors.append(f"{label}.inserted must be true")
        else:
            inserted_count += 1

        if not isinstance(crop_file, str) or not crop_file.strip():
            errors.append(f"{label}.crop_file is required")
        else:
            crop_path = (manifest_root / crop_file).resolve()
            try:
                crop_path.relative_to(manifest_root)
            except ValueError:
                errors.append(f"{label}.crop_file must stay within the manifest directory")
            else:
                if crop_path.suffix.lower() not in allowed_suffixes:
                    errors.append(f"{label}.crop_file must be PNG, SVG, or PDF")
                elif not crop_path.is_file() or crop_path.stat().st_size == 0:
                    errors.append(f"{label}.crop_file is missing or empty: {crop_file}")

    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append("duplicate formula ids: " + ", ".join(duplicates))
    if ids != sorted(ids):
        warnings.append("formula ids are not in ascending source order")

    return {
        "count": len(formulas),
        "inserted": inserted_count,
        "errors": errors,
        "warnings": warnings,
    }


def validate(data: object, terms: list[dict[str, str]] | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return {"status": "fail", "errors": ["Root value must be an object"], "warnings": []}

    source_pages = data.get("source_pages")
    pairs = data.get("pairs")
    if not isinstance(source_pages, int) or source_pages < 1:
        errors.append("source_pages must be a positive integer")
    if not isinstance(pairs, list) or not pairs:
        errors.append("pairs must be a non-empty array")
        pairs = []

    ids: list[str] = []
    page_counts: Counter[int] = Counter()
    source_chars = 0
    translation_chars = 0
    terminology_violation_count = 0
    terms = terms or []

    for index, pair in enumerate(pairs):
        label = f"pairs[{index}]"
        if not isinstance(pair, dict):
            errors.append(f"{label} must be an object")
            continue

        anchor = pair.get("id")
        page = pair.get("page")
        source = pair.get("source")
        translation = pair.get("translation")

        if not isinstance(anchor, str) or not ANCHOR_RE.match(anchor):
            errors.append(f"{label}.id must match pNNN-bNNN")
        else:
            ids.append(anchor)
            anchor_page = int(ANCHOR_RE.match(anchor).group("page"))
            if isinstance(page, int) and anchor_page != page:
                errors.append(f"{anchor}: anchor page and page field differ")

        if not isinstance(page, int) or page < 1:
            errors.append(f"{label}.page must be a positive integer")
        else:
            page_counts[page] += 1
            if isinstance(source_pages, int) and page > source_pages:
                errors.append(f"{label}.page exceeds source_pages")

        if not isinstance(source, str) or not source.strip():
            errors.append(f"{label}.source is empty")
        else:
            source_chars += len(source.strip())
            if LIGATURE_RE.search(source):
                errors.append(f"{anchor or label}: source contains presentation ligatures; decompose them for copyable text")

        if not isinstance(translation, str) or not translation.strip():
            errors.append(f"{label}.translation is empty")
        else:
            translation_chars += len(translation.strip())
            if not CJK_RE.search(translation):
                warnings.append(f"{anchor or label}: translation contains no CJK characters")
            for violation in abbreviation_violations(translation, terms):
                errors.append(f"{anchor or label}: {violation}")
                terminology_violation_count += 1

    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        errors.append("duplicate ids: " + ", ".join(duplicate_ids))

    if ids != sorted(ids):
        warnings.append("pair ids are not in ascending source order")

    missing_pages: list[int] = []
    if isinstance(source_pages, int) and source_pages > 0:
        missing_pages = [page for page in range(1, source_pages + 1) if page_counts[page] == 0]
        if missing_pages:
            warnings.append("pages without mapped text blocks: " + ", ".join(map(str, missing_pages)))

    ratio = round(translation_chars / source_chars, 3) if source_chars else None
    if ratio is not None and (ratio < 0.25 or ratio > 2.5):
        warnings.append(f"unusual translation/source character ratio: {ratio}")

    return {
        "status": "fail" if errors else "pass_with_warnings" if warnings else "pass",
        "statistics": {
            "source_pages": source_pages,
            "pair_count": len(pairs),
            "source_characters": source_chars,
            "translation_characters": translation_chars,
            "translation_source_ratio": ratio,
            "pages_without_text_blocks": missing_pages,
            "terminology_rules": len(terms),
            "terminology_violations": terminology_violation_count,
        },
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        terms = load_terminology(args.terminology) if args.terminology else []
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {"status": "fail", "errors": [str(exc)], "warnings": []}
    else:
        report = validate(data, terms)
        if args.formula_manifest:
            formula_report = validate_formula_manifest(args.formula_manifest, data.get("source_pages") if isinstance(data, dict) else None)
            report["formula_captures"] = {
                "count": formula_report["count"],
                "inserted": formula_report["inserted"],
            }
            report["errors"].extend(formula_report["errors"])
            report["warnings"].extend(formula_report["warnings"])
            report["status"] = "fail" if report["errors"] else "pass_with_warnings" if report["warnings"] else "pass"

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())

