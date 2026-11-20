#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261120 v2 submission.

Copies the pre-rendered entry.png (built by build_image.py in this
same directory) into $MAKEFUN_OUTPUT_DIR/entry.png, then verifies the
copy byte-for-byte. No network, no image generation at run time: the
program is deterministic because the PNG is fixed and checked by hash.

Expected layout:
    <repo root>/
        main.py        (this file)
        entry.png      (1024x1024, built by build_image.py)
"""
import hashlib
import os
import shutil
import sys

# The PNG this program ships. Filled in at build time by build_image.py
# (kept in sync by the build script's own self-check).
EXPECTED_SHA256 = "2ae9a5dd74c626c8f33a0cc18318d85a9c9190a1198e611dd3708fd3d945592d"
EXPECTED_BYTES = 209983

SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message):
    print("main.py: ERROR: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")

    if not os.path.isfile(source):
        return fail("source image missing: " + source)

    size = os.path.getsize(source)
    if size != EXPECTED_BYTES:
        return fail("source size %d != expected %d" % (size, EXPECTED_BYTES))

    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        return fail("source is not a PNG file")

    digest = sha256_of(source)
    if digest != EXPECTED_SHA256:
        return fail("source sha256 %s != expected %s" % (digest, EXPECTED_SHA256))

    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(source, target)

    # Verify the copy, not just the source.
    if os.path.getsize(target) != EXPECTED_BYTES:
        return fail("copied size mismatch")
    if sha256_of(target) != EXPECTED_SHA256:
        return fail("copied sha256 mismatch")

    print("main.py: wrote %s (%d bytes, sha256 %s)"
          % (target, EXPECTED_BYTES, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
