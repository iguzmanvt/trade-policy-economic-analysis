#!/usr/bin/env python3
"""Verify official source bytes, PDF page counts, printed pages and text anchors.

Requires pypdf and the adjacent analyze.py. These checks supplement independent
context review; matching strings do not validate semantics or legal conclusions.
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from analyze import ROOT, validate_project


def normalized(text):
    text = unicodedata.normalize("NFKC", text or "").replace("\u00ad", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_missing(source, path):
    """Install a missing source only after hash validation; never replace cache."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        request = Request(source["url"], headers={"User-Agent": "NTE-Portfolio-Source-Verification/1.0"})
        with urlopen(request, timeout=60) as response:
            destination = urlparse(response.geturl())
            if destination.scheme != "https" or destination.hostname not in {"ustr.gov", "www.ustr.gov"}:
                raise ValueError("download redirected outside official HTTPS USTR domain")
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".nte-download-", suffix=".tmp", delete=False) as output:
                temporary = Path(output.name)
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
        actual = file_hash(temporary)
        if actual != source["sha256"]:
            raise ValueError("downloaded source hash differs from pinned source; cached target was not installed")
        if path.exists():
            raise FileExistsError("cache target appeared during download; existing file was preserved")
        # Exclusive creation prevents replacing an existing cache, including a
        # file created by another process between the check and installation.
        with temporary.open("rb") as origin, path.open("xb") as target:
            for chunk in iter(lambda: origin.read(1024 * 1024), b""):
                target.write(chunk)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def printed_page_labels(text):
    prepared = unicodedata.normalize("NFKC", text or "")
    patterns = (r"FOREIGN\s+TRADE\s+BARRIERS\s*\|\s*(\d+)(?!\d)",
                r"(?<!\d)(\d+)\s*\|\s*FOREIGN\s+TRADE\s+BARRIERS")
    return sorted({int(match) for pattern in patterns for match in re.findall(pattern, prepared, flags=re.IGNORECASE)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path, help="Official PDF cache, outside the release package")
    parser.add_argument("--download", action="store_true", help="Download only missing sources and require the pinned hash")
    parser.add_argument("--project-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.project_dir.resolve()
    data, errors = validate_project(root)
    result = {"status": "FAIL", "source_hashes_verified": [], "source_checks": [], "page_anchors_verified": 0,
              "locator_checks_verified": 0, "printed_page_checks_verified": 0, "record_ids": [], "locator_checks": [],
              "errors": list(errors),
              "scope": "Pinned byte hashes, PDF page counts, printed-page footer/header labels and per-page anchor presence supplement manual context review. They do not validate summaries, coding judgments, policy implementation, economic effects or legal claims."}
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None
        result["errors"].append("Missing dependency: install the project's requirements-source-verification.txt")
    if not result["errors"]:
        readers = {}
        for source in data["sources"]:
            sid = source["source_id"]
            path = args.source_dir / source["filename"]
            item = {"source_id": sid, "filename": source["filename"], "status": "FAIL", "expected_sha256": source["sha256"], "expected_pdf_pages": source["pdf_pages"]}
            try:
                if not path.exists():
                    if not args.download:
                        raise FileNotFoundError("missing source; supply the pinned PDF or use --download")
                    download_missing(source, path)
                actual = file_hash(path)
                item["actual_sha256"] = actual
                if actual != source["sha256"]:
                    raise ValueError("cached source hash mismatch; existing cache was preserved")
                reader = PdfReader(path)
                item["actual_pdf_pages"] = len(reader.pages)
                if len(reader.pages) != source["pdf_pages"]:
                    raise ValueError("PDF page count differs from source index")
                readers[sid] = reader
                item["status"] = "PASS"
                result["source_hashes_verified"].append({"source_id": sid, "sha256": actual, "pdf_pages": len(reader.pages), "filename": source["filename"]})
            except Exception as exc:
                item["error"] = str(exc)
                result["errors"].append(f"{sid}: {exc}")
            result["source_checks"].append(item)

        text_cache, by_record = {}, {}
        for check in data["locators"]:
            sid, rid, page = check["source_id"], check["record_id"], int(check["pdf_page"])
            item = {"check_id": check["check_id"], "record_id": rid, "source_id": sid, "pdf_page": page,
                    "expected_printed_page": int(check["printed_page"]), "anchor_type": check["anchor_type"], "status": "FAIL"}
            if sid not in readers:
                item.update(status="BLOCKED_SOURCE_FAILURE", error="source bytes/page count not verified")
            else:
                try:
                    key = (sid, page)
                    if key not in text_cache:
                        text_cache[key] = readers[sid].pages[page - 1].extract_text() or ""
                    text = text_cache[key]
                    observed = printed_page_labels(text)
                    item["observed_printed_pages"] = observed
                    item["printed_page_match"] = int(check["printed_page"]) in observed
                    item["anchor_match"] = normalized(check["anchor"]) in normalized(text)
                    if item["printed_page_match"] and item["anchor_match"]:
                        item["status"] = "PASS"
                    else:
                        parts = []
                        if not item["printed_page_match"]:
                            parts.append("expected printed page absent from FOREIGN TRADE BARRIERS footer/header")
                        if not item["anchor_match"]:
                            parts.append("normalized anchor not found on its specific physical page")
                        item["error"] = "; ".join(parts)
                        result["errors"].append(f"{check['check_id']}: {item['error']}")
                except Exception as exc:
                    item["error"] = str(exc)
                    result["errors"].append(f"{check['check_id']}: {exc}")
            result["locator_checks"].append(item)
            by_record.setdefault(rid, []).append(item)
        passed_records = sorted(rid for rid, checks in by_record.items() if checks and all(item["status"] == "PASS" for item in checks))
        result["record_ids"] = passed_records
        # Preserve the existing key's meaning: complete evidence records, not
        # number of anchors. The new key gives the actual per-page check count.
        result["page_anchors_verified"] = len(passed_records)
        result["records_with_all_locators_verified"] = len(passed_records)
        result["locator_checks_verified"] = sum(item["status"] == "PASS" for item in result["locator_checks"])
        result["printed_page_checks_verified"] = sum(item.get("printed_page_match", False) for item in result["locator_checks"])
        result["physical_pages_extracted"] = len(text_cache)
        if not result["errors"] and len(passed_records) == len(data["rows"]):
            result["status"] = "PASS"
    output = root / "results"
    output.mkdir(parents=True, exist_ok=True)
    (output / "source_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), file=sys.stdout if result["status"] == "PASS" else sys.stderr)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
