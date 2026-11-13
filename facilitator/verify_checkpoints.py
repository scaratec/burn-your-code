#!/usr/bin/env python3
"""Verifies every workshop checkpoint on a fresh clone of the committed repository.

Usage (from the repository root, after `make -C workshop setup`):
    python3 facilitator/verify_checkpoints.py

It clones HEAD into a temporary directory, walks through all checkpoints and
checks for each one:
  - the MI1 result matches the numbers promised in the exercise guides,
  - a participant's edit to a step file and a personal note survive in the backup,
  - the backup is a compressed archive (no plaintext copies agents could grep),
  - `make spec-check` agrees that governance/ and bdd/ match the checkpoint.
Your working tree is never touched.
"""
import re
import subprocess
import tarfile
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BEHAVE = REPO / "workshop" / ".venv" / "bin" / "behave"
EXPECTED = [
    ("workshop-start", "16 passed, 0 failed"),
    ("ex1-start", "16 passed, 0 failed"),
    ("ex1-solution", "16 passed, 0 failed"),
    ("ex2-start", "16 passed, 0 failed"),
    ("ex2-solution", "26 passed, 6 failed"),
    ("ex3-start", "25 passed, 5 failed"),
    ("ex3-solution", "26 passed, 6 failed"),
    ("ex4-start", "RED: no executable"),
    ("ex4-solution", "32 passed, 0 failed"),
    ("bonus-start", "32 passed, 0 failed"),
    ("bonus-solution", "26 passed, 6 failed"),
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
            marker = f"participant edit before {target}"
            (ws / "my-notes.txt").write_text(marker + "\n")
            with open(ws / "bdd" / "steps" / "geofence_steps.py", "a") as steps:
                steps.write(f"# {marker}\n")
            step = run(["make", "-s", target], ws)
            if step.returncode != 0:
                print(f"FAIL {target:15} make failed: {step.stderr.strip()[:200]}")
                failures += 1
                continue
            problems = []
            backups = sorted((ws / ".workshop-backup").iterdir())
            if any(not b.name.endswith(".tar.gz") for b in backups):
                problems.append("plaintext backup")
            with tarfile.open(backups[-1]) as tar:
                names = tar.getnames()
                for member in ("my-notes.txt", "bdd/steps/geofence_steps.py"):
                    if member not in names or marker not in tar.extractfile(member).read().decode():
                        problems.append(f"edit to {member} not in backup")
            test = run(["make", "-s", "test-mi1"], ws)
            out = test.stdout + test.stderr
            m = re.search(r"(\d+) scenarios? passed, (\d+) failed", out)
            got = f"{m.group(1)} passed, {m.group(2)} failed" if m else "no summary"
            if "RED: Executable './bin/geofence-lib-test' not found" in out and expected.startswith("RED"):
                got = expected
            if got != expected:
                problems.append(f"expected {expected}, got {got}")
            if run(["make", "-s", "spec-check"], ws).returncode != 0:
                problems.append("spec-check reports changes")
            failures += bool(problems)
            print(f"{'FAIL' if problems else 'OK  '} {target:15} {got:22} {'; '.join(problems)}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
