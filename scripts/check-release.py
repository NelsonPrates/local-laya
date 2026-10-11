#!/usr/bin/env python3
"""Confere versão e notas antes da publicação de uma tag."""
from pathlib import Path
import re
import sys


def validate(tag, version, changelog):
    if not re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag):
        raise ValueError("Tag precisa ser vX.Y.Z sem zeros iniciais")
    if tag != "v" + version.strip():
        raise ValueError("Tag diverge de VERSION")
    if not re.search(r"^## " + re.escape(version.strip()) + r"\s*$", changelog, re.M):
        raise ValueError("CHANGELOG.md não contém a versão da tag")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    try:
        validate(sys.argv[1], (root / "VERSION").read_text(), (root / "CHANGELOG.md").read_text())
    except (IndexError, ValueError, OSError) as error:
        sys.exit(str(error))
    print("Tag, versão e notas coerentes")
