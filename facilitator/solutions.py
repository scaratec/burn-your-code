#!/usr/bin/env python3
"""Reference solutions of the workshop, kept in one compressed archive.

Coding agents like to run `git show` and `git log -p`. Plain-text solutions in the
repository would show up in those diffs, so the solutions live in
facilitator/solutions.tar.gz, which git treats as binary.

  python3 facilitator/solutions.py answers   print the facilitator answer key
  python3 facilitator/solutions.py unpack    extract into facilitator/solutions-src/ for editing
  python3 facilitator/solutions.py pack      rebuild solutions.tar.gz from solutions-src/ (deterministic)
  python3 facilitator/solutions.py list      list the archive contents
"""
import gzip
import io
import shutil
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "solutions.tar.gz"
SRC = HERE / "solutions-src"


def read(name):
    """Return the bytes of one member of the archive (used by workshop/scripts/checkpoint.py)."""
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        member = tar.extractfile(name)
        if member is None:
            raise KeyError(name)
        return member.read()


def members(prefix):
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        return [m.name for m in tar.getmembers() if m.isfile() and m.name.startswith(prefix)]


def pack():
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for path in sorted(p for p in SRC.rglob("*") if p.is_file()):
            info = tarfile.TarInfo(str(path.relative_to(SRC)))
            data = path.read_bytes()
            info.size = len(data)
            info.mode = 0o755 if path.stat().st_mode & 0o100 else 0o644
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    with open(ARCHIVE, "wb") as out:
        with gzip.GzipFile(fileobj=out, mode="wb", mtime=0, filename="") as gz:
            gz.write(buf.getvalue())
    print(f"packed {ARCHIVE.name}")


def unpack():
    if SRC.exists():
        shutil.rmtree(SRC)
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        try:
            tar.extractall(SRC, filter="data")
        except TypeError:  # Python < 3.11.4 has no extraction filters
            tar.extractall(SRC)
    print(f"unpacked to {SRC.relative_to(HERE.parent)}/")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "answers":
        sys.stdout.write(read("answers.md").decode())
    elif cmd == "pack":
        pack()
    elif cmd == "unpack":
        unpack()
    elif cmd == "list":
        print("\n".join(members("")))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
