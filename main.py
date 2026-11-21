#!/usr/bin/env python3
"""the-passport-page-of-a-countr-2-20261121-0318 entry: write the invented
passport spread to /output/entry.png.

The picture is a programmatically drawn passport spread for the Republic
of Kavara, a fictional South Pacific atoll nation with no airport:
data page with a stylised portrait of holder Mereana Sela Tavake, a
machine-readable zone (ICAO 9303 check digits verified), a red
"NOT VALID FOR TRAVEL BY AIR — SEA PASSAGE ONLY" endorsement, a chart
of the nine atolls, and a visas page with six chronologically consistent
arrival/departure stamps (Fiji, Tonga, New Zealand) plus a ferry-tax
stamp. It is bundled with this entry as entry.png (PNG, 1024x1024) and
copied byte-for-byte to the output.

Deterministic by construction: a fixed file, no input, no randomness, no
clock, no network, no model calls. Every run writes the same bytes.
Standard library only.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# Same convention as the kit's starter: MAKEFUN_OUTPUT_DIR stands in for
# /output outside the grader's container; default is /output.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def _png_dimensions(path):
    """(width, height) of a PNG from its IHDR chunk, or None if not a PNG."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    dims = _png_dimensions(SRC)
    if dims is None:
        print("entry.png is not a whole PNG", file=sys.stderr)
        return 1
    width, height = dims
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    if width > MAX_DIM or height > MAX_DIM:
        print(f"entry.png is {width}x{height}, over the 1024x1024 cap",
              file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, "entry.png")
    with open(SRC, "rb") as src, open(dest, "wb") as out:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
    print(f"wrote {dest} ({size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
