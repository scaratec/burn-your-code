#!/usr/bin/env python3
"""Self-test before the workshop (`make check`). Prints one line per check and exits 1 on any failure."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OK, FAIL = "\033[32mOK  \033[0m", "\033[31mFAIL\033[0m"
failures = []


def report(ok, label, hint=""):
    print(f"  {OK if ok else FAIL} {label}" + ("" if ok or not hint else f"\n         -> {hint}"))
    if not ok:
        failures.append(label)


def run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def folder_trusted():
    settings = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"
    try:
        trusted = json.loads(settings.read_text()).get("trustedWorkspaces", [])
    except (OSError, ValueError):
        return False
    here = Path(os.path.realpath(ROOT))
    for entry in trusted:
        base = Path(os.path.realpath(os.path.expanduser(entry)))
        if here == base or base in here.parents:
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    print("Burn Your Code — workshop self-test\n")

    report(sys.version_info >= (3, 11), f"Python {sys.version.split()[0]} (3.11 or newer)",
           "install Python 3.11+ and re-run 'make setup'")
    report((ROOT / ".venv" / "bin" / "behave").exists(), "Python test environment (.venv with behave)",
           "run 'make setup'")
    code, _ = run(["git", "rev-parse", "--is-inside-work-tree"])
    report(code == 0 and shutil.which("git") is not None, "git clone of the repository (checkpoints need git)",
           "clone the repository with 'git clone' instead of downloading a ZIP")

    agy = shutil.which("agy")
    report(agy is not None, "Antigravity CLI installed (agy)",
           "install it from https://antigravity.google and open a new terminal")
    if agy:
        code, out = run(["agy", "models"], timeout=90)
        logged_in = code == 0 and "gemini" in out.lower()
        report(logged_in, "Antigravity CLI signed in", "run 'agy' once and complete the sign-in in your browser")
        if logged_in:
            report(re.search(rf"^{re.escape(args.model)}\b", out, re.M) is not None,
                   f"model {args.model} available", "check your Antigravity plan and run 'agy models'")
        report(folder_trusted(), "this folder is trusted by the Antigravity CLI",
               "run 'agy' in this folder, answer 'Yes, I trust this folder', then /exit")

    code, out = run([str(ROOT / ".venv" / "bin" / "behave"), "bdd/", "--tags=@mi1", "--format=progress",
                     "--no-color"])
    m = re.search(r"(\d+) scenarios? passed, (\d+) failed", out)
    green = code == 0 and m is not None and m.group(2) == "0"
    report(green, f"MI1 test suite green ({m.group(1) if m else 0} scenarios passed)",
           "run 'make workshop-start' to restore the starting point, then 'make check' again")

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. Fix them before the workshop.")
        sys.exit(1)
    print("All checks passed. You are ready for the workshop.")


if __name__ == "__main__":
    main()
