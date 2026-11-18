#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261118.

The front page itself is the file entry.png beside this script, drawn at
build time from the verified news of Wednesday 18 November 2026. This
program only copies it to the output directory, so both graded runs
produce exactly the same bytes. Standard library only, no network.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def sha256_of(path):
    """Return the hex sha256 of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    """Copy entry.png to the output directory and verify the copy."""
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(TARGET)
    if source_hash != target_hash:
        print("copy verification failed: hashes differ", file=sys.stderr)
        return 1
    size = TARGET.stat().st_size
    print(f"wrote {TARGET} ({size} bytes, sha256 {target_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
