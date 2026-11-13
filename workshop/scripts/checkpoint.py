#!/usr/bin/env python3
"""Checkpoints for the 90-minute workshop (exercises/README.md).

Every checkpoint resets workshop/ to a defined state: the published workshop
material (the commit your branch was cloned from, even if you committed on top)
plus the files of that checkpoint. Before it changes anything, it packs
everything you wrote or changed (specification, code, notes, staged or not)
into .workshop-backup/<time>-<checkpoint>.tar.gz and checks the archive.

  workshop-start   published specification + baseline MI1 executable
  ex1-start        same as workshop-start
  ex1-solution     + ADR-0005 and LIM-0004 (points on the fence count as inside)
  ex2-start        same as ex1-solution
  ex2-solution     + boundary error paths and scenarios in MI1 (RED)
  ex3-start        ex2-solution with five planted specification defects
  ex3-solution     same as ex2-solution (defects removed)
  ex4-start        ex2-solution with all application code burned
  ex4-solution     ex2-solution with the reference Python implementation
  bonus-start      ex2-solution (RED) with a dishonest bdd/steps/geofence_steps.py
  bonus-solution   restores the honest bdd/steps/geofence_steps.py from the published workshop state

  spec-check       compares governance/ and bdd/ with the state of the last checkpoint
"""
import datetime
import hashlib
import io
import json
import os
import shutil
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
STAGED = ".staged"
SPEC = ["governance", "bdd"]
GIT_APP = ["cmd", "internal", "go.mod", "go.sum", "Dockerfile"]
APP_OUTPUTS = ["app", "src", "build.sh", "bin", ".burned"] + GIT_APP
# Never backed up and never deleted: environments, caches, earlier backups, Terraform state.
KEEP_DIRS = {".git", ".venv", ".workshop-backup", "node_modules", "target", "__pycache__"}
KEEP_PREFIXES = ("terraform/.terraform/", "terraform/terraform.tfstate")


def say(msg):
    print(f"[workshop] {msg}")


def fail(msg):
    sys.exit(f"[workshop] {msg}\n[workshop] Nothing was deleted. Earlier backups are in .workshop-backup/.")


def git_z(*args):
    """Run git and return its NUL-separated output as a list (safe for any file name)."""
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed:\n{result.stderr.decode(errors='replace').strip()}")
    return [p.decode() for p in result.stdout.split(b"\0") if p]


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


_REF = None


def reference():
    """The published workshop state that checkpoints restore.

    It is the fork point of HEAD from the published branch: the upstream of the current
    branch if it has one, otherwise origin's default branch. Own commits, on main or on
    a local branch, stay in git, but checkpoints always restore the published material.
    """
    global _REF
    if _REF is None:
        for published in ("@{upstream}", "refs/remotes/origin/HEAD", "refs/remotes/origin/main"):
            base = subprocess.run(["git", "merge-base", "HEAD", published], cwd=ROOT, capture_output=True, text=True)
            if base.returncode == 0 and base.stdout.strip():
                _REF = base.stdout.strip()
                break
        else:
            fail("cannot find the published workshop state: this clone has no upstream branch and no "
                 "'origin'.\n[workshop] Clone the repository with 'git clone' (see PREPARATION.md), or run "
                 "'git branch --set-upstream-to=<remote>/main' once.")
        if _REF != git("rev-parse", "HEAD"):
            say(f"Restoring the published workshop material ({_REF[:8]}); your own commits stay in git.")
    return _REF


def reference_files():
    prefix = git("rev-parse", "--show-prefix").rstrip("/")
    tree = f"{reference()}:{prefix}" if prefix else reference()
    files = set(git_z("ls-tree", "-r", "--name-only", "-z", "--full-tree", tree))
    if "AGENTS.md" not in files or "scripts/checkpoint.py" not in files:
        fail(f"cannot read the published workshop files from git ({tree}).")
    return files


def kept(rel):
    return rel.startswith(KEEP_PREFIXES)


def disk_files():
    files = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in KEEP_DIRS]
        for name in filenames + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]:
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
            if not kept(rel):
                files.add(rel)
    return files


def extra_files():
    """Everything on disk that is not part of the published workshop (staged, untracked or ignored)."""
    return disk_files() - reference_files()


def changed_files():
    """Published files whose content differs from the reference (staged or not)."""
    return {p for p in git_z("diff", "-z", "--name-only", "--relative", reference())
            if os.path.lexists(ROOT / p)}


def staged_versions():
    """Index versions (git add) that differ from the file on disk: the reset would discard them otherwise."""
    versions = {}
    staged = set(git_z("diff", "-z", "--cached", "--name-only", "--relative", "--diff-filter=d"))  # index vs. HEAD
    for f in git_z("diff", "-z", "--name-only", "--relative"):  # index vs. working tree
        if f not in staged or f in versions:
            continue
        blob = subprocess.run(["git", "cat-file", "blob", f":./{f}"], cwd=ROOT, capture_output=True)
        if blob.returncode == 0:
            versions[f] = blob.stdout
    return versions


def backup(label):
    files = changed_files() | extra_files()
    files |= {f for f in disk_files() if f.split("/", 1)[0] in SPEC}
    files = sorted(f for f in files if os.path.isfile(ROOT / f) or os.path.islink(ROOT / f))
    if not files:
        return
    BACKUP.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    target = BACKUP / f"{stamp}-{label}.tar.gz"
    n = 1
    while target.exists():
        target = BACKUP / f"{stamp}-{label}-{n}.tar.gz"
        n += 1
    staged = staged_versions()
    with tarfile.open(target, "x:gz") as tar:
        for f in files:
            tar.add(ROOT / f, arcname=f, recursive=False)
        for f, data in staged.items():
            info = tarfile.TarInfo(f"{STAGED}/{f}")
            info.size, info.mtime = len(data), int(datetime.datetime.now().timestamp())
            tar.addfile(info, io.BytesIO(data))
    expected = sorted(files + [f"{STAGED}/{f}" for f in staged])
    with tarfile.open(target, "r:gz") as tar:
        if sorted(tar.getnames()) != expected:
            fail(f"the backup {target.name} is incomplete; stopping before anything is changed.")
    rel = target.relative_to(ROOT)
    say(f"Backed up your files to {rel}")
    say(f"  list: tar -tzf {rel}   restore a file: tar -xzf {rel} <path>")
    if staged:
        say(f"  staged versions (git add) that differ from your files are under {STAGED}/ in the archive")


def remove(name):
    path = ROOT / name
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif os.path.lexists(path):
        path.unlink()


def remove_empty_dirs():
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
        rel = os.path.relpath(dirpath, ROOT)
        if rel == "." or set(Path(rel).parts) & KEEP_DIRS or kept(rel + "/"):
            continue
        if not os.listdir(dirpath):
            os.rmdir(dirpath)


def reset_workspace():
    """workshop/ back to the published state; everything else removed (it is in the backup)."""
    extra = sorted(extra_files())
    # Restore first and only then delete: if git fails, nothing has been deleted.
    git("reset", "-q", "--", ".")
    git("checkout", reference(), "--", ".")
    for rel in extra:
        remove(rel)
    remove_empty_dirs()
    visible = [p for p in extra if p.split("/", 1)[0] not in SPEC + ["bin"] and p not in (".burned", MANIFEST.name)]
    if visible:
        shown = ", ".join(visible[:5]) + (f" and {len(visible) - 5} more" if len(visible) > 5 else "")
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
    for name in APP_OUTPUTS:
        remove(name)
    (ROOT / ".burned").touch()
    left = [name for name in APP_OUTPUTS if name != ".burned" and os.path.lexists(ROOT / name)]
    if left:
        sys.exit(f"[workshop] could not burn {', '.join(left)}; remove them by hand and run the checkpoint again.")


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
    git("checkout", reference(), "--", "bdd/steps/geofence_steps.py")


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
