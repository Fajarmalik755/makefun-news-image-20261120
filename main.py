# A news-image entry (Python 3.13, standard library only): the image is the
# entry.png beside this file, and the program copies it to /output/entry.png.
# Deterministic: a plain file copy, so repeated runs write identical bytes.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
dst = os.path.join(out_dir, "entry.png")
shutil.copyfile(src, dst)

# Self-check: the copy must be byte-identical to the source. If the write
# were truncated or corrupted, fail loudly instead of handing the grader a
# broken image. Size + sha256, deterministic, stdlib-only.
def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

if os.path.getsize(src) != os.path.getsize(dst) or _sha256(src) != _sha256(dst):
    raise SystemExit("entry.png copy failed verification: output differs from source")
