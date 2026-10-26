"""Reproduce the three climate-finance work samples from included inputs."""
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    components = [
        ('P06 operational evidence', '06-frld-operational-review', 'validate.py'),
        ('P07 financing cash flows', '07-financing-instruments', 'analyze.py'),
        ('P08 resource reconciliation', '08-frld-resource-reconciliation', 'analyze.py'),
    ]
    for label, directory, script in components:
        print('Reproducing ' + label, flush=True)
        project = root / 'projects' / directory
        subprocess.run([sys.executable, str(project / script)], cwd=project, check=True)
    print('Three independent work samples reproduced. Source and inference limits remain applicable.')


if __name__ == '__main__':
    main()
