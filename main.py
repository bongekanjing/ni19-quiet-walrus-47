#!/usr/bin/env python3
"""Publish entry.png to the make.fun output directory.

The renderer produces entry.png at the repository root. This script validates
the PNG thoroughly - signature, every chunk CRC, IHDR/IEND presence, byte size
and pixel dimensions - and only then copies it to $MAKEFUN_OUTPUT_DIR
(default /output).

Usage:
    python3 main.py            # validate and copy
    python3 main.py --check    # validate only, print size
"""

import argparse
import os
import pathlib
import shutil
import struct
import sys
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIM = 1024
HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def validate(path):
    """Validate the PNG at *path*; return (width, height, size)."""
    if not path.exists():
        raise ValueError("entry.png not found at {}. Run build/render.sh first.".format(path))

    data = path.read_bytes()
    size = len(data)

    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(
            "bad PNG signature: expected b'\\x89PNG\\r\\n\\x1a\\n', got {!r}".format(
                data[:8]
            )
        )

    # Walk every chunk, checking each CRC.
    offset = len(PNG_SIGNATURE)
    chunks = []
    width = height = None

    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError(
                "truncated chunk header at offset {} ({} of {} bytes)".format(
                    offset, offset, size
                )
            )
        length, ctype = struct.unpack(">I4s", data[offset:offset + 8])
        body_start = offset + 8
        body_end = body_start + length
        crc_end = body_end + 4
        if crc_end > len(data):
            raise ValueError(
                "truncated chunk {!r} at offset {}: declared length {} overruns "
                "file of {} bytes".format(ctype, offset, length, size)
            )
        body = data[body_start:body_end]
        (stored_crc,) = struct.unpack(">I", data[body_end:crc_end])
        computed_crc = zlib.crc32(ctype + body) & 0xFFFFFFFF
        if stored_crc != computed_crc:
            raise ValueError(
                "CRC mismatch in chunk {!r} at offset {}: stored {:#010x}, "
                "computed {:#010x}".format(ctype, offset, stored_crc, computed_crc)
            )
        chunks.append(ctype)
        if ctype == b"IHDR":
            if length != 13:
                raise ValueError(
                    "IHDR chunk has wrong length {} (expected 13)".format(length)
                )
            width, height = struct.unpack(">II", body[:8])
        offset = crc_end

    if offset != len(data):
        raise ValueError(
            "chunk walk ended at {} but file is {} bytes".format(offset, size)
        )

    if b"IHDR" not in chunks:
        raise ValueError("missing IHDR chunk")
    if chunks[0] != b"IHDR":
        raise ValueError("first chunk is {!r}, must be IHDR".format(chunks[0]))
    if b"IEND" not in chunks:
        raise ValueError("missing IEND chunk")
    if chunks[-1] != b"IEND":
        raise ValueError("last chunk is {!r}, must be IEND".format(chunks[-1]))
    if width is None or height is None:
        raise ValueError("could not read dimensions from IHDR")

    if size > MAX_BYTES:
        raise ValueError(
            "entry.png is {} bytes, over the {} byte limit".format(size, MAX_BYTES)
        )
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(
            "entry.png is {}x{}, over the {}x{} limit".format(
                width, height, MAX_DIM, MAX_DIM
            )
        )

    return width, height, size


def main(argv=None):
    parser = argparse.ArgumentParser(description="Publish entry.png.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate only, do not copy",
    )
    args = parser.parse_args(argv)

    try:
        width, height, size = validate(SOURCE)
    except ValueError as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 1

    if args.check:
        print("ok {} bytes {}x{} (check only)".format(size, width, height))
        return 0

    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)

    print("wrote {} - {} bytes, {}x{}".format(dest, size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
