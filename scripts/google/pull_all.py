#!/usr/bin/env python3
"""Convenience runner: pull GSC + GA4 in one command."""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=28)
    args = parser.parse_args()

    here = Path(__file__).parent
    for script in ["gsc_pull.py", "ga4_pull.py"]:
        print(f"\n=== {script} ===")
        result = subprocess.run([sys.executable, str(here / script), "--days", str(args.days)])
        if result.returncode != 0:
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
