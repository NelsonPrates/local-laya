#!/usr/bin/env python3
"""Check the skill metadata and essential resources without dependencies."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for name in ("layla-docker", "layla-local", "project-research", "project-qa"):
    folder = root / "skills" / name
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{name}: missing frontmatter"
    metadata = text.split("---", 2)[1]
    assert re.search(rf"^name: {re.escape(name)}$", metadata, re.M), f"{name}: invalid name"
    assert re.search(r"^description: .+", metadata, re.M), f"{name}: missing description"
    assert (folder / "agents/openai.yaml").is_file(), f"{name}: missing interface metadata"
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in link:
            assert (folder / link).is_file(), f"{name}: broken reference: {link}"
    print(f"{name}: OK")
