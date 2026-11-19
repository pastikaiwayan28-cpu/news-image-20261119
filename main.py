#!/usr/bin/env python3
"""news-image-20261119 entry point.

Copies the pre-drawn front page (entry.png, 1024x1024, PNG) that sits
beside this program to the output directory as /output/entry.png,
byte for byte. Standard library only, no network, deterministic:
both runs write identical bytes.

The image itself was drawn offline by build_frontpage.py (Pillow) from
real reporting on Thursday 19 November 2026 and is shipped in the
repository, because this program runs with no network.
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576  # 1 MiB, the competition's cap
MAX_DIM = 1024         # the competition's pixel cap


def check_png(path):
    """Read the PNG header and confirm magic bytes and dimensions.

    Returns (width, height). Raises ValueError on anything unexpected.
    """
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"entry.png is {width}x{height}, over the {MAX_DIM}x{MAX_DIM} cap")
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    try:
        width, height = check_png(src)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
