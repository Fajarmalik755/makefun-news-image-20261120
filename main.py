"""Hand over the finished front page.

The picture itself was already drawn by the generator and sits beside
this file as entry.png. This program only delivers it: it copies that
file to the folder the grader reads from, then proves the copy is exact
by comparing size and sha256. It never draws, downloads, or changes
anything, so running it twice always produces the same bytes.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

BLOCK = 1 << 16
PICTURE = "entry.png"
FALLBACK_DIR = "/output"


def picture_next_to_this_file() -> Path:
    return Path(__file__).resolve().parent / PICTURE


def where_the_copy_goes() -> Path:
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    return Path(folder) / PICTURE


def fingerprint(path: Path) -> tuple[int, str]:
    summer = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            piece = stream.read(BLOCK)
            if not piece:
                break
            size += len(piece)
            summer.update(piece)
    return size, summer.hexdigest()


def move_picture(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as reader, target.open("wb") as writer:
        while True:
            piece = reader.read(BLOCK)
            if not piece:
                break
            writer.write(piece)


def check_copy(source: Path, target: Path) -> None:
    before = fingerprint(source)
    after = fingerprint(target)
    if before != after:
        raise SystemExit(
            "copy does not match source: source is "
            f"{before[0]} bytes {before[1]}, copy is "
            f"{after[0]} bytes {after[1]}"
        )


def run() -> None:
    origin = picture_next_to_this_file()
    if not origin.is_file():
        raise SystemExit(
            f"cannot deliver the front page: {origin} is missing, "
            "so there is nothing to copy"
        )
    destination = where_the_copy_goes()
    move_picture(origin, destination)
    check_copy(origin, destination)


if __name__ == "__main__":
    run()
