#!/usr/bin/env python3
"""Verifies every workshop checkpoint on a fresh clone of the committed repository.

Usage (from the repository root, after `make -C workshop setup`):
    python3 facilitator/verify_checkpoints.py

It clones HEAD into a temporary directory, walks through all checkpoints and
compares the MI1 results with the numbers promised in the exercise guides.
Your working tree is never touched.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BEHAVE = REPO / "workshop" / ".venv" / "bin" / "behave"
EXPECTED = [
    ("workshop-start", "16 passed, 0 failed"),
    ("ex1-solution", "16 passed, 0 failed"),
    ("ex2-solution", "24 passed, 4 failed"),
    ("ex3-start", "23 passed, 3 failed"),
    ("ex3-solution", "24 passed, 4 failed"),
    ("ex4-start", "RED: no executable"),
    ("ex4-solution", "28 passed, 0 failed"),
    ("bonus-start", "28 passed, 0 failed"),
    ("bonus-solution", "24 passed, 4 failed"),
]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    if not BEHAVE.exists():
        sys.exit("Run 'make -C workshop setup' first.")
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "repo"
        run(["git", "clone", "-q", str(REPO), str(clone)], REPO)
        ws = clone / "workshop"
        (ws / ".venv").symlink_to(REPO / "workshop" / ".venv")
        for target, expected in EXPECTED:
            step = run(["make", "-s", target], ws)
            if step.returncode != 0:
                print(f"FAIL {target:15} make failed: {step.stderr.strip()[:200]}")
                failures += 1
                continue
            test = run(["make", "-s", "test-mi1"], ws)
            out = test.stdout + test.stderr
            m = re.search(r"(\d+) scenarios? passed, (\d+) failed", out)
            got = f"{m.group(1)} passed, {m.group(2)} failed" if m else "no summary"
            if "RED: Executable './bin/geofence-lib-test' not found" in out and expected.startswith("RED"):
                got = expected
            ok = got == expected
            failures += not ok
            print(f"{'OK  ' if ok else 'FAIL'} {target:15} expected {expected:22} got {got}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
