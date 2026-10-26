#!/usr/bin/env python3
"""Validate policy-register lineage and the boundaries of this analytical template.

No live application or institution is scored. The output is file validation only.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALLOWED_STATUSES = {
    "adopted_mandate", "adopted_framework", "reported_operating_scope",
    "elements_endorsed_finalization_pending", "development_pending",
    "mandate_with_background_options",
}
EXPECTED_MODULES = {
    "Authority and access", "Funds and implementation", "Financing and results"
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    source_document = json.loads((ROOT / "sources.json").read_text())
    sources = source_document["sources"]
    source_ids = {s["source_id"] for s in sources}
    require(len(source_ids) == len(sources), "Duplicate source identifier")
    for source in sources:
        for key in ("source_id", "url", "policy_status", "locator", "verification", "accessed_date"):
            require(bool(source.get(key)), "Missing source field: " + key)
        require(source["url"].startswith("https://"), "Source URL must use HTTPS")

    policies = read_csv("policy_register.csv")
    policy_ids = {p["policy_id"] for p in policies}
    require(len(policy_ids) == len(policies), "Duplicate policy identifier")
    require(bool(policies), "Empty policy register")
    for policy in policies:
        require(all(str(v).strip() for v in policy.values()), "Empty policy field")
        require(policy["status"] in ALLOWED_STATUSES, "Unknown policy status")
        require(set(policy["source_ids"].split(";")) <= source_ids, "Unresolved policy source")

    reviews = read_csv("review_matrix.csv")
    review_ids = {r["review_id"] for r in reviews}
    require(len(review_ids) == len(reviews), "Duplicate review identifier")
    require({r["module"] for r in reviews} == EXPECTED_MODULES, "Unexpected review modules")
    for review in reviews:
        require(all(str(v).strip() for v in review.values()), "Empty review field")
        require(set(review["policy_ids"].split(";")) <= policy_ids, "Unresolved review policy")
        require(review["case_evidence_state"] == "not_assessed", "Template cannot claim a case assessment")

    report = {
        "result": "PASS_DOCUMENT_INTEGRITY",
        "source_records": len(sources),
        "policy_records": len(policies),
        "review_checks": len(reviews),
        "modules": {name: sum(r["module"] == name for r in reviews) for name in sorted(EXPECTED_MODULES)},
        "case_assessments": 0,
        "scope": "Identifiers, source linkage, status vocabulary, required fields and non-assessment boundary",
        "does_not_establish": ["policy completeness", "country eligibility", "functional equivalency", "fiduciary approval", "debt sustainability"],
        "source_review_date": source_document["as_of_date"],
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
