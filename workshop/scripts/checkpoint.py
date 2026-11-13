#!/usr/bin/env python3
"""Checkpoints for the 90-minute workshop (exercises/README.md).

Every checkpoint resets workshop/ to a defined state. Before it changes
anything, it packs everything you wrote (specification, code, notes) into
.workshop-backup/<time>-<checkpoint>.tar.gz, so nothing is lost.

  workshop-start   reference specification from git HEAD + baseline MI1 executable
  ex1-start        same as workshop-start
  ex1-solution     + ADR-0005 and LIM-0004 (points on the fence count as inside)
  ex2-start        same as ex1-solution
  ex2-solution     + boundary error paths and scenarios in MI1 (RED)
  ex3-start        ex2-solution with five planted specification defects
  ex3-solution     same as ex2-solution (defects removed)
  ex4-start        ex2-solution with all application code burned
  ex4-solution     ex2-solution with the reference Python implementation
  bonus-start      ex2-solution (RED) with a dishonest bdd/steps/geofence_steps.py
  bonus-solution   restores the honest bdd/steps/geofence_steps.py from git HEAD

  spec-check       compares governance/ and bdd/ with the state of the last checkpoint
"""
import datetime
import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Reference solutions live outside workshop/ in a compressed archive, so that
# coding agents working in workshop/ (and their `git show`) do not see them.
sys.path.insert(0, str(ROOT.parent / "facilitator"))
import solutions  # noqa: E402

BACKUP = ROOT / ".workshop-backup"
MANIFEST = ROOT / ".workshop-spec.json"
SPEC = ["governance", "bdd"]
GIT_APP = ["cmd", "internal", "go.mod", "go.sum", "Dockerfile"]
# Ignored by git, so `git clean` keeps them; checkpoints handle them explicitly.
IGNORED_APP = ["bin", ".burned"]
NOT_BACKED_UP = ("node_modules/", "target/", "__pycache__/", ".venv/", ".workshop-backup/")


def say(msg):
    print(f"[workshop] {msg}")


def git_out(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"[workshop] git {' '.join(args)} failed:\n{result.stderr.strip()}\n"
                 "[workshop] Nothing was deleted. Earlier backups are in .workshop-backup/.")
    return result.stdout


def git(*args):
    git_out(*args)


def untracked():
    """Files git does not know and does not ignore (paths relative to workshop/)."""
    return [p for p in git_out("ls-files", "--others", "--exclude-standard").splitlines()
            if not p.startswith(NOT_BACKED_UP)]


def backup(label):
    files = set(git_out("ls-files", "--modified").splitlines()) | set(untracked())
    for name in SPEC + IGNORED_APP:
        path = ROOT / name
        if path.is_file():
            files.add(name)
        elif path.is_dir():
            files.update(str(p.relative_to(ROOT)) for p in path.rglob("*") if p.is_file())
    files = sorted(f for f in files if (ROOT / f).is_file() and "/__pycache__/" not in f"/{f}")
    if not files:
        return
    BACKUP.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    target = BACKUP / f"{stamp}-{label}.tar.gz"
    n = 1
    while target.exists():
        target = BACKUP / f"{stamp}-{label}-{n}.tar.gz"
        n += 1
    with tarfile.open(target, "x:gz") as tar:
        for f in files:
            tar.add(ROOT / f, arcname=f, recursive=False)
    rel = target.relative_to(ROOT)
    say(f"Backed up your files to {rel}")
    say(f"  list: tar -tzf {rel}   restore a file: tar -xzf {rel} <path>")


def remove(name):
    path = ROOT / name
    if path.is_dir() and not path.is_symlink():
        import shutil
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def reset_workspace():
    """Every tracked file back to git HEAD, everything else in workshop/ removed (it is in the backup)."""
    extra = [p for p in untracked() if not p.startswith(tuple(f"{s}/" for s in SPEC))]
    # Restore first and only then delete: if git fails, nothing has been deleted.
    git("checkout", "HEAD", "--", ".")
    git("clean", "-fdq", "--", ".")
    for name in IGNORED_APP:
        remove(name)
    if extra:
        shown = ", ".join(extra[:5]) + (f" and {len(extra) - 5} more" if len(extra) > 5 else "")
        say(f"Removed files that are not part of the workshop (they are in the backup): {shown}")


def install(member, dst, executable=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(solutions.read(member))
    if executable:
        dst.chmod(0o755)


def overlay(name):
    for member in solutions.members(f"{name}/"):
        rel = member[len(name) + 1:]
        install(member, ROOT / rel, executable=rel.endswith((".sh", "geofence-lib-test")))


def edit(rel, old, new):
    path = ROOT / rel
    text = path.read_text()
    if old not in text:
        sys.exit(f"[workshop] cannot load exercise 3 in {rel}: expected text not found")
    path.write_text(text.replace(old, new, 1))


def drop_line(rel, needle):
    path = ROOT / rel
    lines = path.read_text().splitlines(keepends=True)
    kept = [line for line in lines if needle not in line]
    if len(kept) == len(lines):
        sys.exit(f"[workshop] cannot load exercise 3 in {rel}: line with {needle!r} not found")
    path.write_text("".join(kept))


def baseline_app():
    install("baseline/geofence-lib-test", ROOT / "bin" / "geofence-lib-test", executable=True)


def burn_app():
    for name in GIT_APP + IGNORED_APP:
        remove(name)
    (ROOT / ".burned").touch()


def state_start():
    reset_workspace()
    baseline_app()


def state_ex1():
    state_start()
    overlay("ex1")


def state_ex2():
    state_ex1()
    overlay("ex2")


def state_ex4():
    state_ex2()
    burn_app()


def state_ex4_solution():
    state_ex4()
    remove(".burned")
    overlay("ex4")


def plant_defects():
    for defect in json.loads(solutions.read("ex3-defects.json")):
        if "drop_line" in defect:
            drop_line(defect["file"], defect["drop_line"])
        else:
            edit(defect["file"], defect["old"], defect["new"])


def spec_hashes():
    hashes = {}
    for name in SPEC:
        for path in sorted((ROOT / name).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def write_manifest(checkpoint):
    MANIFEST.write_text(json.dumps({"checkpoint": checkpoint, "files": spec_hashes()}, indent=1) + "\n")


def spec_check():
    if not MANIFEST.exists():
        sys.exit("[workshop] No checkpoint recorded yet. Run a checkpoint such as 'make ex4-start' first.")
    recorded = json.loads(MANIFEST.read_text())
    before, now = recorded["files"], spec_hashes()
    added = sorted(set(now) - set(before))
    removed = sorted(set(before) - set(now))
    changed = sorted(f for f in set(now) & set(before) if now[f] != before[f])
    if not (added or removed or changed):
        say(f"governance/ and bdd/ are unchanged since '{recorded['checkpoint']}'.")
        return
    say(f"governance/ and bdd/ differ from the state of '{recorded['checkpoint']}':")
    for label, items in (("added", added), ("removed", removed), ("changed", changed)):
        for item in items:
            print(f"  {label:8} {item}")
    sys.exit(1)


def bonus_start():
    state_ex2()
    install("bonus/geofence_steps_dishonest.py", ROOT / "bdd" / "steps" / "geofence_steps.py")


def bonus_solution():
    git("checkout", "HEAD", "--", "bdd/steps/geofence_steps.py")


STATES = {
    "workshop-start": (state_start, "Workshop starting point. Next: exercises/ex1-fence-decision/README.md"),
    "ex1-start": (state_start, "Ready for exercise 1. Open exercises/ex1-fence-decision/README.md"),
    "ex1-solution": (state_ex1, "Loaded the exercise 1 reference solution (ADR-0005, LIM-0004)."),
    "ex2-start": (state_ex1, "Ready for exercise 2. Open exercises/ex2-red-scenarios/README.md"),
    "ex2-solution": (state_ex2, "Loaded the exercise 2 reference solution. 'make test-mi1' is RED."),
    "ex3-start": (lambda: (state_ex2(), plant_defects()),
                  "Ready for exercise 3: everybody now works on the reference specification, "
                  "with five defects hidden in it."),
    "ex3-solution": (state_ex2, "Loaded the defect-free specification (exercise 3 solution)."),
    "ex4-start": (state_ex4, "Ready for exercise 4: all application code is burned. 'make test-mi1' is RED."),
    "ex4-solution": (state_ex4_solution,
                     "Loaded the exercise 4 reference implementation (Python). 'make test-mi1' is GREEN."),
    "bonus-start": (bonus_start, "Loaded the RED state of exercise 2 with a dishonest bdd/steps/geofence_steps.py. "
                                 "Open exercises/bonus-step-honesty/README.md"),
    "bonus-solution": (bonus_solution, "Restored the honest bdd/steps/geofence_steps.py. "
                                       "'make test-mi1' is RED again, as it should be."),
}


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in STATES:
        backup(cmd)
        func, msg = STATES[cmd]
        func()
        write_manifest(cmd)
        say(msg)
    elif cmd == "spec-check":
        spec_check()
    elif cmd == "install-baseline":
        baseline_app()
        say("Installed the baseline MI1 executable.")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
