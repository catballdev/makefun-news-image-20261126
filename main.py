#!/usr/bin/env python3
"""
Copy the competition entry image to the output directory.

This program is the v1 entry for the make.fun "news-image-20261126" competition.
It reads the pre-rendered entry.png (a newspaper front page summarising
26 November 2026 world news) from the repository root and writes an exact
byte-for-byte copy to the directory specified by the MAKEFUN_OUTPUT_DIR
environment variable (defaulting to /output). The operation is deterministic:
running it multiple times produces identically-hashed output files.
"""

import os
import shutil
import sys


def main() -> int:
    """
    Copy entry.png to the output directory.

    Returns:
        0 on success, non-zero on error.
    """
    # Source image lives next to this script in the repo root
    src = os.path.join(os.path.dirname(__file__), "entry.png")

    # Output directory: honour MAKEFUN_OUTPUT_DIR, fallback to /output
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    dst = os.path.join(out_dir, "entry.png")

    # shutil.copyfile copies only the file contents (bytes), no metadata,
    # guaranteeing byte-identical output on every run.
    shutil.copyfile(src, dst)

    return 0


if __name__ == "__main__":
    sys.exit(main())