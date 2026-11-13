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
Afterwards it replays participant mistakes found in acceptance reviews (staged
edits, Unicode file names, edited .gitignore, staged implementations and ADRs,
own commits) and checks that nothing is lost and nothing survives a reset.
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
        failures += mistakes(ws)
    sys.exit(1 if failures else 0)


def latest_backup(ws):
    return tarfile.open(sorted((ws / ".workshop-backup").iterdir())[-1])


def in_backup(ws, member, text):
    with latest_backup(ws) as tar:
        return member in tar.getnames() and text in tar.extractfile(member).read().decode()


def mistakes(ws):
    failures = 0

    def check(name, ok):
        nonlocal failures
        failures += not ok
        print(f"{'OK  ' if ok else 'FAIL'} mistake: {name}")

    git = lambda *a: run(["git", *a], ws)  # noqa: E731
    make = lambda t: run(["make", "-s", t], ws)  # noqa: E731

    # Staged edit, Unicode file name, file hidden by an edited .gitignore.
    with open(ws / "README.md", "a") as f:
        f.write("staged participant edit\n")
    git("add", "README.md")
    (ws / "notes").mkdir(exist_ok=True)
    (ws / "notes" / "résumé.md").write_text("unicode note\n")
    with open(ws / ".gitignore", "a") as f:
        f.write("secret.txt\n")
    (ws / "secret.txt").write_text("ignored note\n")
    make("workshop-start")
    check("staged edit backed up and reset", in_backup(ws, "README.md", "staged participant edit")
          and "staged participant edit" not in (ws / "README.md").read_text())
    check("Unicode file backed up and removed", in_backup(ws, "notes/résumé.md", "unicode note")
          and not (ws / "notes").exists())
    check("file hidden by own .gitignore backed up and removed", in_backup(ws, "secret.txt", "ignored note")
          and not (ws / "secret.txt").exists())

    # A staged implementation must not survive ex4-start.
    make("ex4-solution")
    git("add", "-f", "app", "build.sh")
    make("ex4-start")
    test = run(["make", "-s", "test-mi1"], ws)
    check("staged implementation burned by ex4-start", not (ws / "app").exists() and not (ws / "build.sh").exists()
          and "RED: Executable" in test.stdout + test.stderr)

    # A staged, differently named ADR must not survive ex3-start.
    (ws / "governance" / "adr" / "0005-participant-outside.md").write_text("# outside\n")
    git("add", "governance/adr/0005-participant-outside.md")
    make("ex3-start")
    check("staged own ADR backed up and removed by ex3-start",
          not (ws / "governance" / "adr" / "0005-participant-outside.md").exists()
          and in_backup(ws, "governance/adr/0005-participant-outside.md", "outside"))

    # Staged and working-tree versions of the same file differ: both must be in the backup.
    with open(ws / "README.md", "a") as f:
        f.write("version A staged\n")
    git("add", "README.md")
    (ws / "README.md").write_text((ws / "README.md").read_text().replace("version A staged", "version B on disk"))
    make("workshop-start")
    check("distinct staged and working-tree versions both backed up",
          in_backup(ws, "README.md", "version B on disk") and in_backup(ws, ".staged/README.md", "version A staged"))

    # A committed dishonest step file must not come back from bonus-solution.
    make("bonus-start")
    git("add", "bdd/steps/geofence_steps.py")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "save bonus state")
    make("bonus-solution")
    test = run(["make", "-s", "test-mi1"], ws)
    check("bonus-solution restores honest steps after a commit", "26 scenarios passed, 6 failed" in test.stdout + test.stderr)
    git("reset", "-q", "--hard", "HEAD~1")

    # Own commits on a local branch without upstream: checkpoints still restore the published material.
    git("switch", "-q", "-c", "my-work")
    make("ex2-solution")
    (ws / "governance" / "adr" / "0005-participant-outside.md").write_text("# outside\n")
    git("add", "-A", ".")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "my exercise work")
    make("workshop-start")
    test = run(["make", "-s", "test-mi1"], ws)
    check("local branch without upstream: workshop-start gives the starting point",
          "16 scenarios passed, 0 failed" in test.stdout + test.stderr)
    make("ex3-start")
    adrs = sorted(p.name for p in (ws / "governance" / "adr").glob("0005-*.md"))
    check("local branch without upstream: ex3-start keeps only the reference ADR",
          adrs == ["0005-points-on-the-fence-count-as-inside.md"])
    git("switch", "-q", "-")

    # Own commits stay in git, but checkpoints restore the published material.
    (ws / "governance" / "adr" / "0099-own.md").write_text("# own\n")
    git("add", "governance/adr/0099-own.md")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "own work")
    make("workshop-start")
    test = run(["make", "-s", "test-mi1"], ws)
    check("own commit kept in git, published state restored",
          not (ws / "governance" / "adr" / "0099-own.md").exists()
          and "own work" in git("log", "-1", "--format=%s").stdout
          and "16 scenarios passed, 0 failed" in test.stdout + test.stderr)
    return failures


if __name__ == "__main__":
    main()
