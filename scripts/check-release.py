#!/usr/bin/env python3
"""Check the version and the notes before a tag is published."""
from pathlib import Path
import re
import sys


def validate(tag, version, changelog):
    if not re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag):
        raise ValueError("The tag must be vX.Y.Z without leading zeros")
    if tag != "v" + version.strip():
        raise ValueError("The tag does not match VERSION")
    if not re.search(r"^## " + re.escape(version.strip()) + r"\s*$", changelog, re.M):
        raise ValueError("CHANGELOG.md does not contain the tag version")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    try:
        validate(sys.argv[1], (root / "VERSION").read_text(), (root / "CHANGELOG.md").read_text())
    except (IndexError, ValueError, OSError) as error:
        sys.exit(str(error))
    print("Tag, version, and notes agree")
