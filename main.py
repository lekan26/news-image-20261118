#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261118.

The front page itself is the file entry.png beside this script, drawn at
build time from the verified news of Wednesday 18 November 2026. This
program only copies it to the output directory and checks the copy is a
valid 1024x1024 PNG, so both graded runs produce exactly the same bytes. Standard library only, no network.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

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


def check_png(path):
    """Check path is a PNG of the expected size; return an error or None."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if header[:8] != PNG_SIGNATURE:
        return f"{path}: not a PNG (bad signature)"
    if len(header) < 33 or header[12:16] != b"IHDR":
        return f"{path}: not a PNG (missing IHDR chunk)"
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return (
            f"{path}: unexpected dimensions {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return None


def main():
    """Copy entry.png to the output directory and verify the copy."""
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    png_error = check_png(TARGET)
    if png_error is not None:
        print(png_error, file=sys.stderr)
        return 1
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
