#!/usr/bin/env python3
"""Copy the v2 front-page image to the output directory.

The entry image is drawn offline by build_frontpage_v2.py and shipped in
this repository as entry.png. This program validates it thoroughly before
copying it byte for byte to /output/entry.png, then verifies the copy, so
running it twice writes identical bytes.

Validation (all of it, before any copy):
  - PNG magic (8 bytes)
  - first chunk is IHDR, length 13 (so the dimension fields below are real)
  - IHDR width/height are exactly 1024x1024
  - file is at most 1 MiB
  - file ends with a complete IEND chunk (not truncated)
After the copy the destination is read back and compared by size and
sha256 against the validated source; a mismatch is a hard failure.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1048576


def fail(msg):
    sys.exit(f"entry.png invalid: {msg}")


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG (bad magic)")
    if len(data) < 33:
        fail("too short for a PNG header")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if ihdr_len != 13 or data[12:16] != b"IHDR":
        fail("first chunk is not IHDR (length 13)")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail(f"is {width}x{height}, expected 1024x1024")
    if len(data) > MAX_BYTES:
        fail(f"is {len(data)} bytes, over the 1 MiB cap")
    if data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        fail("missing or truncated IEND chunk")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as fh:
        copied = fh.read()
    if len(copied) != len(data):
        fail(f"copy is {len(copied)} bytes, source is {len(data)}")
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        fail("copy sha256 does not match the source")
    print(f"copied {SRC} -> {DST} ({len(data)} bytes, {width}x{height}, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
