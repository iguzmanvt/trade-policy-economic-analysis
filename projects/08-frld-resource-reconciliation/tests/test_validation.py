"""Behavior checks run against normal and optimized Python; no network needed."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def exercise(self, mutator=None, valid=False):
        for optimized in (False, True):
            with self.subTest(optimized=optimized), tempfile.TemporaryDirectory() as temp:
                temp = Path(temp)
                with (ROOT/'data'/'reported_metrics.csv').open(newline='') as f:
                    reader = csv.DictReader(f); fields = reader.fieldnames; rows = list(reader)
                if mutator:
                    mutator(rows)
                data = temp/'input.csv'
                with data.open('w',newline='') as f:
                    writer = csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
                out = temp/'out'; out.mkdir(); sentinel = out/'metrics.json'; sentinel.write_text('previous result')
                cmd = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/'analyze.py'),'--data',str(data),'--output',str(out)]
                result = subprocess.run(cmd,cwd=temp,capture_output=True,text=True)
                if valid:
                    self.assertEqual(result.returncode,0,result.stderr)
                    self.assertIn('59.05',result.stdout)
                    self.assertEqual(len(list(out.iterdir())),4)
                else:
                    self.assertNotEqual(result.returncode,0)
                    self.assertEqual(sentinel.read_text(),'previous result')
                    self.assertEqual(len(list(out.iterdir())),1)

    def test_valid(self): self.exercise(valid=True)
    def test_duplicate(self): self.exercise(lambda r:r.append(dict(r[0])))
    def test_missing_record(self): self.exercise(lambda r:r.pop())
    def test_missing_not_zero(self): self.exercise(lambda r:r[4].update(value='0'))
    def test_incompatible_date(self): self.exercise(lambda r:r[0].update(reference_date='2026-10-26'))
    def test_counts(self): self.exercise(lambda r:r[6].update(value='175'))
    def test_allocation(self): self.exercise(lambda r:r[11].update(value='350'))
    def test_nonfinite(self): self.exercise(lambda r:r[0].update(value='NaN'))
    def test_unit(self): self.exercise(lambda r:r[5].update(unit='USD million'))
    def test_rounded_precision(self): self.exercise(lambda r:r[8].update(precision='0.01 million'))


if __name__ == '__main__': unittest.main()
