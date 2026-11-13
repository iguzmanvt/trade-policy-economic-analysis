"""Adverse tests for source meaning, preservation, independent audit and portability."""
import copy
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import analyze
import verify


class FdiValidationTests(unittest.TestCase):
    def setUp(self):
        self.annual, self.partial = analyze.load_inputs()

    def rejects(self, field, value, partial=False):
        rows = copy.deepcopy(self.partial if partial else self.annual)
        rows[0][field] = value
        with self.assertRaises(ValueError):
            analyze.validate_rows(rows, not partial)

    def test_reject_full_year_label_on_half_year(self):
        self.rejects("periodo_origen", "2026-4", partial=True)

    def test_reject_revision_state_mix(self):
        self.rejects("archivo_fuente", "tipo_original.xlsx")

    def test_reject_duplicate_observation(self):
        rows = self.annual + [self.annual[0]]
        with self.assertRaises(ValueError):
            analyze.validate_rows(rows, True)

    def test_reject_missing_component(self):
        with self.assertRaises(ValueError):
            analyze.validate_rows(self.annual[:-1], True)

    def test_reject_confidential_as_published_amount(self):
        self.rejects("estado", "confidencial")

    def test_reject_zero_denominator(self):
        self.rejects("ied_mdd", "0")

    def test_reject_nonfinite_amount(self):
        self.rejects("ied_mdd", "NaN")

    def test_reject_wrong_source_cell(self):
        self.rejects("celda", "E6")

    def test_reject_pinned_input_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            for name in analyze.FILES:
                (path / name).write_bytes((ROOT / "data" / name).read_bytes())
            file = path / analyze.FILES[0]
            file.write_bytes(file.read_bytes().replace(b"21236.853631705799", b"21237.853631705799"))
            with self.assertRaises(ValueError):
                analyze.load_inputs(path)

    def test_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            marker = path / "preserve.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyze.write_outputs(analyze.calculate(self.annual, self.partial), path)
            self.assertEqual(marker.read_text(), "keep")
            self.assertEqual(len(list(path.iterdir())), 1)

    def test_normal_optimized_reproduce_identical_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            dirs = [base / "normal", base / "optimized"]
            for mode, path in zip([[], ["-O"]], dirs):
                subprocess.run([sys.executable, "-B", *mode, str(ROOT / "analyze.py"), "--output", str(path)], check=True, capture_output=True)
                checked = subprocess.run([sys.executable, "-B", *mode, str(ROOT / "verify.py"), "--results", str(path)], check=True, capture_output=True, text=True)
                self.assertEqual(json.loads(checked.stdout)["status"], "PASS")
            self.assertEqual({p.name: p.read_bytes() for p in dirs[0].iterdir()}, {p.name: p.read_bytes() for p in dirs[1].iterdir()})

    def test_independent_auditor_rejects_altered_share_and_residual(self):
        for name, field in [("annual_shares.csv", "share_pct"), ("reconciliation.csv", "residual_usdm")]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "results"
                analyze.write_outputs(analyze.calculate(self.annual, self.partial), path)
                file = path / name
                with file.open(encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle); rows = list(reader); fields = reader.fieldnames
                rows[0][field] = "999"
                with file.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
                with self.assertRaises(ValueError):
                    verify.audit(path)

    def test_figures_reject_unverified_inputs_before_write(self):
        if importlib.util.find_spec("matplotlib") is None:
            self.skipTest("matplotlib is optional")
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            results = base / "results"
            figures = base / "figures"
            analyze.write_outputs(analyze.calculate(self.annual, self.partial), results)
            file = results / "snapshot_2026s1.csv"
            with file.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle); rows = list(reader); fields = reader.fieldnames
            rows[0]["share_pct"] = "99"
            with file.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
            run = subprocess.run([sys.executable, "-B", str(ROOT / "build_figures.py"), "--results", str(results), "--output", str(figures)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(figures.exists())


if __name__ == "__main__":
    unittest.main()
