"""Regression tests for the bounded reproduction comparison, standard library only."""
from __future__ import annotations

import csv
from decimal import Decimal, localcontext
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from compare_reproduction import (  # noqa: E402
    ComparisonError, DERIVED_FIELDS, FIELDS, GROWTH_PATH, compare_trees,
)


class ReproductionComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.before, self.after = self.base / "before", self.base / "after"
        for tree in (self.before, self.after):
            path = tree / GROWTH_PATH
            path.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / GROWTH_PATH, path)
            (tree / "source.json").write_bytes(b'{"fixed": 0.249}\n')
            (tree / "other.csv").write_bytes(b"value\r\n1.0\r\n")

    def rows(self, tree=None):
        with ((tree or self.after) / GROWTH_PATH).open(newline="", encoding="utf-8") as source:
            return list(csv.reader(source))

    def write_rows(self, rows, tree=None):
        with ((tree or self.after) / GROWTH_PATH).open("w", newline="", encoding="utf-8") as target:
            csv.writer(target).writerows(rows)

    def perturb(self, column, delta, row=28):
        rows = self.rows()
        index = rows[0].index(column)
        rows[row][index] = str(Decimal(rows[row][index]) + Decimal(delta))
        self.write_rows(rows)

    def rejected(self):
        with self.assertRaises(ComparisonError):
            compare_trees(self.before, self.after)

    def restore(self):
        shutil.copyfile(self.before / GROWTH_PATH, self.after / GROWTH_PATH)

    def test_identity_and_all_204_rows(self):
        result = compare_trees(self.before, self.after)
        self.assertEqual(result["file_count"], 3)
        self.assertEqual(result["byte_identical_files"], 3)
        self.assertEqual(result["growth"]["rows"], 204)
        self.assertEqual(result["growth"]["changed_derived_cells"], 0)

    def test_observed_scale_passes_only_in_each_derived_column(self):
        for column in DERIVED_FIELDS:
            with self.subTest(column=column):
                self.restore()
                self.perturb(column, "3e-14")
                result = compare_trees(self.before, self.after)
                self.assertEqual(result["byte_identical_files"], 2)
                self.assertEqual(result["growth"]["changed_derived_cells"], 1)

    def test_large_change_fails_in_each_derived_column(self):
        for column in DERIVED_FIELDS:
            with self.subTest(column=column):
                self.restore()
                self.perturb(column, "1e-10")
                self.rejected()

    def test_absolute_boundary_is_inclusive(self):
        for delta in ("1e-12", "-1e-12"):
            with self.subTest(delta=delta):
                self.restore()
                self.perturb("output_gap_pct", delta)
                compare_trees(self.before, self.after)

    def test_just_above_absolute_boundary_fails_without_relative_tolerance(self):
        for delta in ("1.00000001e-12", "-1.00000001e-12"):
            with self.subTest(delta=delta):
                self.restore()
                self.perturb("output_per_worker_index", delta)
                self.rejected()

    def test_high_precision_differences_do_not_round_across_boundary(self):
        for sign in (-1, 1):
            for side in (-1, 1):
                with self.subTest(sign=sign, side=side):
                    self.restore()
                    rows = self.rows()
                    index = FIELDS.index("output_per_worker_index")
                    with localcontext() as context:
                        context.prec = 200
                        delta = sign * (Decimal("1e-12") + side * Decimal("1e-80"))
                        rows[28][index] = str(Decimal(rows[28][index]) + delta)
                    self.write_rows(rows)
                    if side > 0:
                        self.rejected()
                    else:
                        compare_trees(self.before, self.after)

    def test_parameter_cells_are_exact_even_for_smaller_changes(self):
        for column in ("investment_share", "efficiency_growth"):
            with self.subTest(column=column):
                self.restore()
                self.perturb(column, "1e-15")
                self.rejected()

    def test_parameter_spelling_is_exact(self):
        rows = self.rows()
        rows[1][FIELDS.index("investment_share")] += "0"
        self.write_rows(rows)
        self.rejected()

    def test_rejects_nonfinite_and_malformed_numbers_even_if_both_trees_match(self):
        for value in ("NaN", "Infinity", "-Infinity", "1_00", "", " 100"):
            with self.subTest(value=value):
                rows = self.rows(self.before)
                rows[1][FIELDS.index("output_per_worker_index")] = value
                self.write_rows(rows, self.after)
                self.rejected()
                self.write_rows(rows, self.before)
                self.rejected()
                shutil.copyfile(ROOT / GROWTH_PATH, self.before / GROWTH_PATH)
                self.restore()

    def test_changed_header_fails(self):
        rows = self.rows()
        rows[0][2] = "capital"
        self.write_rows(rows)
        self.rejected()

    def test_reordered_columns_fail(self):
        rows = self.rows()
        for row in rows:
            row[2], row[3] = row[3], row[2]
        self.write_rows(rows)
        self.rejected()

    def test_changed_key_fails(self):
        for index, value in ((0, "other"), (1, "27.0")):
            with self.subTest(index=index):
                self.restore()
                rows = self.rows()
                rows[28][index] = value
                self.write_rows(rows)
                self.rejected()

    def test_duplicate_key_fails(self):
        rows = self.rows()
        rows[28] = rows[27]
        self.write_rows(rows)
        self.rejected()

    def test_reordered_rows_fail(self):
        rows = self.rows()
        rows[27], rows[28] = rows[28], rows[27]
        self.write_rows(rows)
        self.rejected()

    def test_missing_and_extra_rows_fail(self):
        for extra in (False, True):
            with self.subTest(extra=extra):
                self.restore()
                rows = self.rows()
                if extra:
                    rows.append(rows[-1])
                else:
                    rows.pop()
                self.write_rows(rows)
                self.rejected()

    def test_missing_and_extra_cells_fail(self):
        for extra in (False, True):
            with self.subTest(extra=extra):
                self.restore()
                rows = self.rows()
                if extra:
                    rows[28].append("1.0")
                else:
                    rows[28].pop()
                self.write_rows(rows)
                self.rejected()

    def test_lf_and_missing_final_newline_fail(self):
        for transform in (lambda b: b.replace(b"\r\n", b"\n"), lambda b: b[:-2]):
            with self.subTest(transform=transform):
                self.restore()
                path = self.after / GROWTH_PATH
                path.write_bytes(transform(path.read_bytes()))
                self.rejected()

    def test_changed_quoting_fails(self):
        path = self.after / GROWTH_PATH
        path.write_bytes(path.read_bytes().replace(b"baseline,0,", b'"baseline",0,', 1))
        self.rejected()

    def test_other_csv_has_no_numeric_tolerance(self):
        (self.after / "other.csv").write_bytes(b"value\r\n1.00000000000001\r\n")
        self.rejected()

    def test_other_file_newlines_remain_exact(self):
        (self.after / "source.json").write_bytes(b'{"fixed": 0.249}\r\n')
        self.rejected()

    def test_missing_and_added_files_fail(self):
        (self.after / "source.json").unlink()
        self.rejected()
        shutil.copyfile(self.before / "source.json", self.after / "source.json")
        (self.after / "extra.txt").write_bytes(b"new")
        self.rejected()

    def test_missing_growth_file_in_both_trees_fails(self):
        for tree in (self.before, self.after):
            (tree / GROWTH_PATH).unlink()
        self.rejected()

    def test_git_metadata_is_the_only_excluded_entry(self):
        git_dir = self.after / ".git"
        git_dir.mkdir()
        (git_dir / "index").write_bytes(b"local metadata")
        compare_trees(self.before, self.after)
        cache = self.after / "__pycache__"
        cache.mkdir()
        (cache / "generated.pyc").write_bytes(b"generated")
        self.rejected()

    def test_cli_pass_and_failure_exit_status(self):
        command = [
            sys.executable, "-B", str(ROOT / "compare_reproduction.py"),
            str(self.before), str(self.after),
        ]
        good = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertIn('"status": "passed"', good.stdout)
        self.perturb("output_gap_pct", "1e-10")
        bad = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("exceeds", bad.stderr)


if __name__ == "__main__":
    unittest.main()
