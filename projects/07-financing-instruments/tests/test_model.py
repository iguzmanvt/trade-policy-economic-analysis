"""Independent arithmetic and failure tests for the illustrative model."""
import copy
import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("model", ROOT / "analyze.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class CashFlowTests(unittest.TestCase):
    def setUp(self):
        self.a = json.loads((ROOT / "data/assumptions.json").read_text())
        self.out = model.compute(self.a)

    def rows(self, package):
        return [r for r in self.out["annual_cashflows.csv"] if r["package"] == package]

    def test_equal_initial_funding_and_grant_has_no_repayments(self):
        for p in self.a["packages"]:
            self.assertEqual(self.rows(p["id"])[0]["initial_receipt_usd_m"], 100)
        self.assertEqual(sum(r["debt_service_usd_m"] for r in self.rows("grant")), 0)

    def test_principal_identity_and_first_repayment_convention(self):
        rows = self.rows("concessional")
        self.assertTrue(all(r["principal_usd_m"] == 0 for r in rows[1:6]))
        self.assertAlmostEqual(rows[6]["principal_usd_m"], 100 / 15)
        self.assertAlmostEqual(rows[6]["interest_usd_m"], 1)
        self.assertAlmostEqual(rows[-1]["closing_debt_usd_m"], 0)
        self.assertAlmostEqual(sum(r["principal_usd_m"] for r in rows), 100)

    def test_undiscounted_interest_independent_closed_sum(self):
        # 5 interest-only years plus arithmetic sequence of 15 opening balances.
        independent_interest = 5 * 100 * 0.01 + 0.01 * (100 / 15) * (15 * 16 / 2)
        self.assertAlmostEqual(independent_interest, 13)
        self.assertAlmostEqual(sum(r["interest_usd_m"] for r in self.rows("concessional")), 13)
        self.assertAlmostEqual(model.present_value(self.rows("concessional"), 0), 113)

    def test_reference_pv_equals_face_when_coupon_equals_discount(self):
        # Independent bond pricing identity, not an output-to-output comparison.
        self.assertAlmostEqual(model.present_value(self.rows("reference"), 0.05), 100)

    def test_pv_independent_explicit_payment_sum(self):
        independent = sum(1 / 1.05 ** y for y in range(1, 6))
        independent += sum((100 / 15 + (100 - (k - 1) * 100 / 15) * 0.01) / 1.05 ** (5 + k) for k in range(1, 16))
        self.assertAlmostEqual(model.present_value(self.rows("concessional"), 0.05), independent)

    def test_mixed_package_linearity(self):
        for full, half in zip(self.rows("concessional")[1:], self.rows("mixed")[1:]):
            self.assertAlmostEqual(half["debt_service_usd_m"], full["debt_service_usd_m"] / 2)
        pv = model.present_value(self.rows("concessional"), 0.05)
        mixed = [r for r in self.out["discount_sensitivity.csv"] if r["package"] == "mixed" and r["discount_rate_pct"] == 5][0]
        self.assertAlmostEqual(mixed["package_pv_support_pct"], 100 - pv / 2)

    def test_fx_and_envelope_shock_begin_in_year6(self):
        stressed = {r["year"]: r for r in self.out["fiscal_stress.csv"] if r["package"] == "concessional" and r["fiscal_scenario"] == "fx25_envelope20"}
        self.assertEqual(stressed[5]["fx_lcu_per_usd"], 1)
        self.assertEqual(stressed[5]["annual_envelope_lcu_m"], 100)
        self.assertEqual(stressed[6]["fx_lcu_per_usd"], 1.25)
        self.assertEqual(stressed[6]["annual_envelope_lcu_m"], 80)
        self.assertAlmostEqual(stressed[6]["incremental_service_envelope_pct"], (100 / 15 + 1) * 1.25 / 80 * 100)

    def test_discount_sensitivity_decreases_pv(self):
        values = [r["pv_repayment_usd_m"] for r in self.out["discount_sensitivity.csv"] if r["package"] == "concessional"]
        self.assertGreater(values[0], values[1])
        self.assertGreater(values[1], values[2])

    def test_cash_timing_uses_peak_not_sum_of_shortfalls(self):
        results = {r["receipt_month"]: r for r in self.out["timing_sensitivity.csv"]}
        self.assertEqual(results[1]["peak_cash_shortfall_usd_m"], 0)
        self.assertEqual(results[3]["peak_cash_shortfall_usd_m"], 60)
        self.assertEqual(results[6]["peak_cash_shortfall_usd_m"], 90)

    def test_duplicate_ids_nonfinite_and_bad_maturity_rejected(self):
        mutators = [
            lambda a: a["packages"][1].update(id="grant"),
            lambda a: a["packages"][1].update(interest_rate=float("nan")),
            lambda a: a["packages"][1].update(principal_holiday_years=20),
            lambda a: a["fiscal_scenarios"][1].update(baseline_envelope_lcu_m=0),
            lambda a: a["packages"][1].update(loan_usd_m=90),
        ]
        for mutate in mutators:
            with self.subTest(mutation=mutate):
                changed = copy.deepcopy(self.a)
                mutate(changed)
                with self.assertRaises(ValueError):
                    model.compute(changed)

    def test_invalid_input_preserves_previous_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            sentinel = tmp / "package_comparison.csv"
            sentinel.write_text("previous verified output\n")
            bad = copy.deepcopy(self.a)
            bad["packages"][1]["principal_holiday_years"] = 20
            input_file = tmp / "bad.json"
            input_file.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                model.run(input_file, tmp)
            self.assertEqual(sentinel.read_text(), "previous verified output\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
