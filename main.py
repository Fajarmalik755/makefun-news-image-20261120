#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261120 v3 entry.

Copies the pre-rendered entry.png (which sits next to this file) into the
output directory the harness provides, then verifies the copy. Stdlib only.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "b50b0750485c5f6591a4eb14ca5cd8230082c18ff106fe7eae742f403a064650"
EXPECTED_BYTES = 208862
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message):
    print("main.py: ERROR: %s" % message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py: %s" % src)

    with open(src, "rb") as fh:
        magic = fh.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        return fail("entry.png is not a PNG file")

    size = os.path.getsize(src)
    if size != EXPECTED_BYTES:
        return fail("entry.png size %d != expected %d" % (size, EXPECTED_BYTES))
    if sha256_of(src) != EXPECTED_SHA256:
        return fail("entry.png sha256 mismatch")

    os.makedirs(out_dir, exist_ok=True)
    if not os.path.isdir(out_dir):
        return fail("MAKEFUN_OUTPUT_DIR is not a directory: %s" % out_dir)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)

    if os.path.getsize(dst) != EXPECTED_BYTES:
        return fail("copied entry.png size mismatch")
    if sha256_of(dst) != EXPECTED_SHA256:
        return fail("copied entry.png sha256 mismatch")
    with open(dst, "rb") as fh:
        if fh.read(len(PNG_MAGIC)) != PNG_MAGIC:
            return fail("copied entry.png is not a PNG file")

    print("main.py: wrote %s (%d bytes, sha256 %s)"
          % (dst, EXPECTED_BYTES, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
