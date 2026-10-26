#!/usr/bin/env python3
"""Validate and reproduce descriptive tables for the selected NTE cheese issues.

Uses Python's standard library. Coding and review decisions are inputs; this
program checks their consistency, not the truth or legal validity of claims.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
YEARS = (2024, 2025, 2026)
CODED = "CODED_SOURCE_REVIEWED"
NO_MENTION = "SECTION_REVIEWED_NO_MENTION"
COVERAGE_STATES = {CODED, NO_MENTION}
INPUT_FIELDS = {
    "rows": ("nte_cheese_sample.csv", "record_id edition_year report_chapter jurisdiction issue_id topic product printed_pages pdf_pages source_id source_url anchor reported_status source_instrument summary verification report_subsection source_description ustr_position analyst_interpretation measure_stage verification_date".split()),
    "topics": ("taxonomy.csv", "topic definition coding_rule".split()),
    "statuses": ("reported_status_dictionary.csv", "reported_status definition".split()),
    "issues": ("selected_issues.csv", "issue_id report_chapter jurisdiction topic issue_label selection_reason follow_up_evidence continuity_rule".split()),
    "coverage": ("coverage_review.csv", "issue_id edition_year coverage_status source_id reviewed_printed_pages reviewed_pdf_pages record_id review_scope review_note review_date".split()),
    "locators": ("locator_checks.csv", "check_id record_id source_id pdf_page printed_page anchor anchor_type".split()),
}


def page_numbers(value):
    """Parse positive page numbers/ranges; commas and semicolons join ranges."""
    text = str(value).strip().translate(str.maketrans({"–": "-", "—": "-", "−": "-"}))
    if not text:
        raise ValueError("empty page locator")
    pages = []
    for part in re.split(r"[;,]", text):
        match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", part)
        if not match:
            raise ValueError("invalid page locator: " + text)
        first, last = int(match[1]), int(match[2] or match[1])
        if first < 1 or last < first:
            raise ValueError("nonpositive or reversed page range: " + text)
        if last - first > 10000:
            raise ValueError("unreasonably large page range: " + text)
        pages.extend(range(first, last + 1))
    if len(pages) != len(set(pages)) or pages != sorted(pages):
        raise ValueError("overlapping or unordered page ranges: " + text)
    return pages


def _read_csv(root, key, errors):
    filename, required = INPUT_FIELDS[key]
    try:
        with (root / "data" / filename).open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)):
                errors.append(filename + ": duplicate column names")
            missing = sorted(set(required) - set(headers))
            if missing:
                errors.append(filename + ": missing columns " + ", ".join(missing))
            rows = list(reader)
        for index, row in enumerate(rows, 2):
            if None in row:
                errors.append(f"{filename}:{index}: extra unlabelled CSV values")
            for field in required:
                if key == "coverage" and field == "record_id":
                    continue
                if not str(row.get(field) or "").strip():
                    errors.append(f"{filename}:{index}: empty {field}")
        return rows
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(filename + ": " + str(exc))
        return []


def _unique(rows, fields, label, errors):
    keys = [tuple(str(row.get(field) or "") for field in fields) for row in rows]
    for key, count in Counter(keys).items():
        if count > 1:
            errors.append(f"{label}: duplicate key {key}")


def _year(value, label, errors):
    try:
        year = int(value)
        if year not in YEARS:
            raise ValueError("outside the declared editions")
        return year
    except (TypeError, ValueError):
        errors.append(label + ": invalid edition year " + str(value))
        return None


def _date(value, label, errors, earliest_year=None):
    try:
        parsed = date.fromisoformat(str(value))
        if earliest_year and parsed.year < earliest_year:
            raise ValueError("date before report edition")
        return parsed
    except ValueError:
        errors.append(label + ": invalid or inconsistent ISO date " + str(value))
        return None


def _pages(value, label, errors, bound=None):
    try:
        pages = page_numbers(value)
        if bound and any(page > bound for page in pages):
            raise ValueError("physical page exceeds source page count")
        return pages
    except (TypeError, ValueError) as exc:
        errors.append(label + ": " + str(exc))
        return []


def validate_project(root):
    """Return parsed inputs and all detected structural errors; no writes."""
    errors = []
    data = {key: _read_csv(root, key, errors) for key in INPUT_FIELDS}
    try:
        metadata = json.loads((root / "sources.json").read_text(encoding="utf-8-sig"))
        if not isinstance(metadata, dict):
            raise ValueError("source index must be an object")
        sources = metadata.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(s, dict) for s in sources):
            raise ValueError("sources must be a list of objects")
    except (OSError, ValueError, TypeError) as exc:
        errors.append("sources.json: " + str(exc))
        metadata, sources = {}, []
    data.update(metadata=metadata, sources=sources)
    for field in ("information_cutoff_local", "reference_date_local", "execution_date_local"):
        if field in metadata:
            _date(metadata[field], "sources " + field, errors)
    if not data["rows"] or not data["issues"] or not sources:
        errors.append("Evidence, selected-issue catalogue and source index must not be empty")
    _unique(sources, ["source_id"], "sources", errors)
    _unique(sources, ["filename"], "sources filenames", errors)
    source_map = {}
    for s in sources:
        sid = str(s.get("source_id") or "")
        for field in ("source_id", "edition_year", "url", "pdf_pages", "sha256", "filename", "retrieval_date_local"):
            if not str(s.get(field) or "").strip():
                errors.append(f"sources {sid}: missing {field}")
        year = _year(s.get("edition_year"), "sources " + sid, errors)
        _date(s.get("retrieval_date_local"), "sources " + sid, errors, year)
        if "latest_verification_date_local" in s:
            _date(s["latest_verification_date_local"], "sources latest verification " + sid, errors, year)
        filename = str(s.get("filename") or "")
        if Path(filename).name != filename or "/" in filename or "\\" in filename or not filename.lower().endswith(".pdf"):
            errors.append(f"sources {sid}: filename must be a single PDF basename")
        url = urlparse(str(s.get("url") or ""))
        if url.scheme != "https" or url.hostname not in {"ustr.gov", "www.ustr.gov"}:
            errors.append(f"sources {sid}: expected an official HTTPS USTR URL")
        if not re.fullmatch(r"[0-9a-f]{64}", str(s.get("sha256") or "")):
            errors.append(f"sources {sid}: invalid SHA-256")
        if not isinstance(s.get("pdf_pages"), int) or s["pdf_pages"] < 1:
            errors.append(f"sources {sid}: pdf_pages must be a positive integer")
        source_map[sid] = s
    data["source_map"] = source_map

    _unique(data["topics"], ["topic"], "taxonomy", errors)
    topics = {row.get("topic") for row in data["topics"]}
    _unique(data["statuses"], ["reported_status"], "reported status dictionary", errors)
    statuses = {row.get("reported_status") for row in data["statuses"]}
    _unique(data["issues"], ["issue_id"], "selected issues", errors)
    issue_map = {r.get("issue_id"): r for r in data["issues"]}
    data["issue_map"] = issue_map
    for issue in data["issues"]:
        if issue.get("topic") not in topics:
            errors.append(f"Issue {issue.get('issue_id')}: unknown topic")

    _unique(data["rows"], ["record_id"], "evidence", errors)
    _unique(data["rows"], ["issue_id", "edition_year"], "evidence issue-edition", errors)
    _unique(data["rows"], ["source_id", "report_chapter", "report_subsection", "pdf_pages"], "document-section-locator", errors)
    record_map, record_pages = {}, {}
    for row in data["rows"]:
        rid = str(row.get("record_id") or "")
        label = "Record " + rid
        year = _year(row.get("edition_year"), label, errors)
        review_date = _date(row.get("verification_date"), label, errors, year)
        issue = issue_map.get(row.get("issue_id"))
        if issue is None:
            errors.append(label + ": issue absent from selection catalogue")
        else:
            for field in ("report_chapter", "jurisdiction", "topic"):
                if row.get(field) != issue.get(field):
                    errors.append(label + ": " + field + " disagrees with selection catalogue")
        if row.get("topic") not in topics:
            errors.append(label + ": unknown taxonomy category")
        if not re.fullmatch(r"[a-z][a-z0-9_]*", str(row.get("reported_status") or "")):
            errors.append(label + ": reported_status must be a stable snake_case code")
        if row.get("reported_status") not in statuses:
            errors.append(label + ": reported_status absent from status dictionary")
        s = source_map.get(row.get("source_id"))
        bound = None
        if s is None:
            errors.append(label + ": unknown source_id")
        else:
            if year != s.get("edition_year"):
                errors.append(label + ": source edition mismatch")
            if row.get("source_url") != s.get("url"):
                errors.append(label + ": source URL mismatch")
            bound = s.get("pdf_pages") if isinstance(s.get("pdf_pages"), int) else None
            try:
                if review_date and review_date < date.fromisoformat(s["retrieval_date_local"]):
                    errors.append(label + ": verification date predates recorded source retrieval")
            except (KeyError, ValueError, TypeError):
                pass
        physical = _pages(row.get("pdf_pages"), label + " physical pages", errors, bound)
        printed = _pages(row.get("printed_pages"), label + " printed pages", errors)
        if len(physical) != len(printed):
            errors.append(label + ": unequal physical and printed page counts")
        record_pages[rid] = dict(zip(physical, printed))
        record_map[rid] = row
    data.update(record_map=record_map, record_pages=record_pages)

    _unique(data["coverage"], ["issue_id", "edition_year"], "coverage issue-edition", errors)
    coverage_keys, linked_records = set(), []
    for row in data["coverage"]:
        issue_id = row.get("issue_id")
        label = f"Coverage {issue_id}/{row.get('edition_year')}"
        year = _year(row.get("edition_year"), label, errors)
        _date(row.get("review_date"), label, errors, year)
        coverage_keys.add((issue_id, year))
        if issue_id not in issue_map:
            errors.append(label + ": unknown selected issue")
        status = row.get("coverage_status")
        if status not in COVERAGE_STATES:
            errors.append(label + ": unknown coverage_status")
        s = source_map.get(row.get("source_id"))
        bound = s.get("pdf_pages") if s and isinstance(s.get("pdf_pages"), int) else None
        if not s or s.get("edition_year") != year:
            errors.append(label + ": unknown or wrong-edition source")
        physical = _pages(row.get("reviewed_pdf_pages"), label + " physical pages", errors, bound)
        printed = _pages(row.get("reviewed_printed_pages"), label + " printed pages", errors)
        rid = str(row.get("record_id") or "").strip()
        if status == CODED:
            evidence = record_map.get(rid)
            if evidence is None:
                errors.append(label + ": coded cell must link to an evidence record")
            else:
                linked_records.append(rid)
                if evidence.get("issue_id") != issue_id or str(evidence.get("edition_year")) != str(year):
                    errors.append(label + ": linked evidence belongs to another issue or edition")
                if evidence.get("source_id") != row.get("source_id"):
                    errors.append(label + ": linked evidence source differs")
                mapping = record_pages.get(rid, {})
                if not set(mapping).issubset(physical) or not set(mapping.values()).issubset(printed):
                    errors.append(label + ": reviewed pages do not cover linked record pages")
        elif status == NO_MENTION and rid:
            errors.append(label + ": no-mention cell must leave record_id empty")
    expected_keys = {(issue, year) for issue in issue_map for year in YEARS}
    if coverage_keys != expected_keys:
        errors.append("Coverage matrix must contain every selected issue in each declared edition; missing=" + str(sorted(expected_keys - coverage_keys, key=str)) + "; unexpected=" + str(sorted(coverage_keys - expected_keys, key=str)))
    if Counter(linked_records) != Counter(record_map.keys()):
        errors.append("Every evidence record must be linked exactly once by a coded coverage cell")

    _unique(data["locators"], ["check_id"], "locator checks", errors)
    _unique(data["locators"], ["record_id", "source_id", "pdf_page", "anchor"], "locator content", errors)
    located = defaultdict(set)
    for check in data["locators"]:
        label = "Locator " + str(check.get("check_id"))
        rid = check.get("record_id")
        row = record_map.get(rid)
        if row is None:
            errors.append(label + ": unknown record_id")
            continue
        if check.get("source_id") != row.get("source_id"):
            errors.append(label + ": source differs from evidence record")
        try:
            physical, printed = int(check.get("pdf_page")), int(check.get("printed_page"))
        except (TypeError, ValueError):
            errors.append(label + ": physical and printed page must each be one integer")
            continue
        mapping = record_pages.get(rid, {})
        if physical not in mapping or mapping[physical] != printed:
            errors.append(label + ": page pair is outside or inconsistent with record locator")
        located[rid].add(physical)
    for rid, mapping in record_pages.items():
        if located[rid] != set(mapping):
            errors.append(f"Record {rid}: each physical page requires a locator check")
    return data, errors


def write_csv(directory, filename, rows, fields):
    with (directory / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.project_dir.resolve()
    data, errors = validate_project(root)
    output = root / "results"
    output.mkdir(parents=True, exist_ok=True)
    validation = {"status": "FAIL" if errors else "PASS", "errors": errors,
                  "scope": "Structural consistency, documentary coverage and locator metadata. No semantic or legal adjudication."}
    (output / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    if errors:
        (output / "summary.json").write_text(json.dumps({"status": "FAIL", "errors": errors, "validation": "FAILED; other result tables have not been refreshed."}, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(validation, indent=2), file=sys.stderr)
        return 1
    rows, issues, coverage = data["rows"], data["issues"], data["coverage"]
    topic_rows = []
    for topic in sorted(r["topic"] for r in data["topics"]):
        selected = [r for r in rows if r["topic"] == topic]
        topic_rows.append({"topic": topic, "coded_records": len(selected), "distinct_issues": len({r["issue_id"] for r in selected})})
    write_csv(output, "topic_summary.csv", topic_rows, ["topic", "coded_records", "distinct_issues"])
    annual = []
    for year in YEARS:
        selected = [r for r in rows if int(r["edition_year"]) == year]
        cells = [r for r in coverage if int(r["edition_year"]) == year]
        annual.append({"edition_year": year, "coded_records": len(selected), "selected_chapters": len({r["report_chapter"] for r in selected}), "reviewed_issue_cells": len(cells), "section_reviewed_no_mention": sum(r["coverage_status"] == NO_MENTION for r in cells)})
    write_csv(output, "selected_coverage.csv", annual, ["edition_year", "coded_records", "selected_chapters", "reviewed_issue_cells", "section_reviewed_no_mention"])
    continuity, matrix, comparison = [], [], []
    coverage_map = {(r["issue_id"], int(r["edition_year"])): r for r in coverage}
    for issue in sorted(issues, key=lambda r: r["issue_id"]):
        iid = issue["issue_id"]
        observed, unmentioned = [], []
        comparative = {k: issue[k] for k in ("issue_id", "report_chapter", "jurisdiction", "topic", "issue_label", "continuity_rule", "follow_up_evidence")}
        for year in YEARS:
            cell = coverage_map[(iid, year)]
            record = data["record_map"].get(cell["record_id"], {})
            (observed if cell["coverage_status"] == CODED else unmentioned).append(year)
            matrix.append({**issue, **cell, "source_url": data["source_map"][cell["source_id"]]["url"], "reported_status": record.get("reported_status", ""), "measure_stage": record.get("measure_stage", "")})
            values = {"coverage_status": cell["coverage_status"], "record_id": cell["record_id"], "source_id": cell["source_id"], "printed_pages": record.get("printed_pages", cell["reviewed_printed_pages"]), "pdf_pages": record.get("pdf_pages", cell["reviewed_pdf_pages"]), "reported_status": record.get("reported_status", "NOT_APPLICABLE_NO_CODED_PASSAGE"), "source_instrument": record.get("source_instrument", "NOT_APPLICABLE_NO_CODED_PASSAGE"), "source_url": data["source_map"][cell["source_id"]]["url"]}
            comparative.update({f"{key}_{year}": value for key, value in values.items()})
        continuity.append({"issue_id": iid, "observed_editions": ";".join(map(str, observed)), "coded_edition_count": len(observed), "section_reviewed_no_mention_editions": ";".join(map(str, unmentioned))})
        comparison.append(comparative)
    write_csv(output, "issue_continuity.csv", continuity, ["issue_id", "observed_editions", "coded_edition_count", "section_reviewed_no_mention_editions"])
    matrix_fields = ["issue_id", "edition_year", "report_chapter", "jurisdiction", "topic", "issue_label", "coverage_status", "source_id", "source_url", "reviewed_printed_pages", "reviewed_pdf_pages", "record_id", "reported_status", "measure_stage", "review_scope", "review_note", "review_date"]
    write_csv(output, "coverage_matrix.csv", matrix, matrix_fields)
    write_csv(output, "comparison_table.csv", comparison, list(comparison[0]))
    timeline = sorted((r for r in rows if r["issue_id"] in {"EU-GI-NAMES", "CHL-PRIOR-USERS"}), key=lambda r: (r["issue_id"], int(r["edition_year"])))
    temporal_fields = ["issue_id", "edition_year", "source_instrument", "reported_status", "printed_pages", "pdf_pages", "source_url", "measure_stage"]
    write_csv(output, "temporal_cases.csv", timeline, temporal_fields)
    inputs = ["sources.json"] + ["data/" + name for name, _ in INPUT_FIELDS.values()]
    stats = {"status": "PASS", "records": len(rows), "distinct_issues": len(issues), "editions": list(YEARS),
             "chapters": sorted({r["report_chapter"] for r in rows}), "jurisdictions": sorted({r["jurisdiction"] for r in rows}),
             "topics": len(data["topics"]), "source_documents": len(data["sources"]),
             "reported_status_counts": dict(sorted(Counter(r["reported_status"] for r in rows).items())),
             "coverage_cells": len(coverage), "coverage_status_counts": dict(sorted(Counter(r["coverage_status"] for r in coverage).items())),
             "locator_check_rows": len(data["locators"]), "input_sha256": hashlib.sha256((root / "data/nte_cheese_sample.csv").read_bytes()).hexdigest(),
             "input_hashes": {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs},
             "interpretation": "Purposive coded sample counts, not barrier prevalence, severity, economic cost or legal findings. No-mention cells describe documented review, not zero barriers or repeal.",
             "validation": "Passed explicit structural, date, catalogue, source, page-range and complete selected-issue coverage checks. PDF bytes and page anchors are checked separately by verify_sources.py."}
    (output / "summary.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
