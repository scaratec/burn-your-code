#!/usr/bin/env python3
"""Checkpoints for the 90-minute workshop (exercises/README.md).

Every command first copies the files it is about to overwrite to
.workshop-backup/<timestamp>-<command>/, so nothing you wrote is lost.

  workshop-start   reference specification from git HEAD + baseline MI1 executable
  ex1-start        same as workshop-start
  ex1-solution     + ADR-0005 and LIM-0004 (points on the fence count as inside)
  ex2-start        same as ex1-solution
  ex2-solution     + error path rows 1.5-1.8 and the boundary scenarios in MI1
  ex3-start        ex2-solution with five planted specification defects
  ex3-solution     same as ex2-solution (defects removed)
  ex4-start        ex2-solution with all application code burned
  ex4-solution     ex2-solution with the reference Python implementation
  bonus-start      ex2-solution (RED) with a dishonest bdd/steps/geofence_steps.py
  bonus-solution   restores the honest bdd/steps/geofence_steps.py from git HEAD
"""
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Reference solutions live outside workshop/ in a compressed archive, so that
# coding agents working in workshop/ (and their `git show`) do not see them.
sys.path.insert(0, str(ROOT.parent / "facilitator"))
import solutions  # noqa: E402
BACKUP = ROOT / ".workshop-backup"
SPEC = ["governance", "bdd"]
APP = ["bin", "build.sh", "src", "app", "lib", "cmd", "internal", "go.mod", "go.sum", "Dockerfile",
       "package.json", "package-lock.json", "tsconfig.json", "node_modules", "dist", "Cargo.toml",
       "Cargo.lock", "target", "pyproject.toml"]
GIT_APP = ["cmd", "internal", "go.mod", "go.sum", "Dockerfile"]


def say(msg):
    print(f"[workshop] {msg}")


def backup(label):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    target = BACKUP / f"{stamp}-{label}"
    for name in SPEC + APP + [".burned"]:
        src = ROOT / name
        if not src.exists() or name in ("node_modules", "target"):
            continue
        dst = target / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, symlinks=True)
        else:
            shutil.copy2(src, dst)
    if target.exists():
        say(f"Backed up your current files to {target.relative_to(ROOT)}/")


def git(*args):
    subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)


def remove(name):
    path = ROOT / name
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


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
        sys.exit(f"[workshop] cannot plant defect in {rel}: expected text not found")
    path.write_text(text.replace(old, new, 1))


def drop_line(rel, needle):
    path = ROOT / rel
    lines = path.read_text().splitlines(keepends=True)
    kept = [line for line in lines if needle not in line]
    if len(kept) == len(lines):
        sys.exit(f"[workshop] cannot plant defect in {rel}: line with {needle!r} not found")
    path.write_text("".join(kept))


def reference_spec():
    for name in SPEC:
        remove(name)
    git("checkout", "HEAD", "--", *SPEC)


def baseline_app():
    for name in APP:
        remove(name)
    remove(".burned")
    git("checkout", "HEAD", "--", *GIT_APP)
    (ROOT / "bin").mkdir()
    install("baseline/geofence-lib-test", ROOT / "bin" / "geofence-lib-test", executable=True)


def burn_app():
    for name in APP:
        remove(name)
    (ROOT / ".burned").touch()


def state_start():
    reference_spec()
    baseline_app()


def state_ex1():
    state_start()
    overlay("ex1")


def state_ex2():
    state_ex1()
    overlay("ex2")


def plant_defects():
    for defect in json.loads(solutions.read("ex3-defects.json")):
        if "drop_line" in defect:
            drop_line(defect["file"], defect["drop_line"])
        else:
            edit(defect["file"], defect["old"], defect["new"])


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    states = {
        "workshop-start": (state_start, "Workshop starting point. Next: exercises/ex1-fence-decision/README.md"),
        "ex1-start": (state_start, "Ready for exercise 1. Open exercises/ex1-fence-decision/README.md"),
        "ex1-solution": (state_ex1, "Loaded the exercise 1 reference solution (ADR-0005, LIM-0004)."),
        "ex2-start": (state_ex1, "Ready for exercise 2. Open exercises/ex2-red-scenarios/README.md"),
        "ex2-solution": (state_ex2, "Loaded the exercise 2 reference solution. 'make test-mi1' is RED (4 scenarios)."),
        "ex3-start": (lambda: (state_ex2(), plant_defects()), "Ready for exercise 3: five defects are hidden in the specification."),
        "ex3-solution": (state_ex2, "Loaded the defect-free specification (exercise 3 solution)."),
        "ex4-start": (lambda: (state_ex2(), burn_app()), "Ready for exercise 4: all application code is burned. 'make test-mi1' is RED."),
        "ex4-solution": (lambda: (state_ex2(), burn_app(), remove(".burned"), overlay("ex4")),
                         "Loaded the exercise 4 reference implementation (Python). 'make test-mi1' is GREEN."),
    }
    if cmd in states:
        backup(cmd)
        func, msg = states[cmd]
        func()
        say(msg)
    elif cmd == "bonus-start":
        backup(cmd)
        state_ex2()
        install("bonus/geofence_steps_dishonest.py", ROOT / "bdd" / "steps" / "geofence_steps.py")
        say("Loaded the RED state of exercise 2 with a dishonest bdd/steps/geofence_steps.py. Open exercises/bonus-step-honesty/README.md")
    elif cmd == "install-baseline":
        install("baseline/geofence-lib-test", ROOT / "bin" / "geofence-lib-test", executable=True)
        say("Installed the baseline MI1 executable.")
    elif cmd == "bonus-solution":
        git("checkout", "HEAD", "--", "bdd/steps/geofence_steps.py")
        say("Restored the honest bdd/steps/geofence_steps.py. 'make test-mi1' is RED again (4 scenarios).")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
