#!/usr/bin/env python3
"""Validação sem dependências dos metadados e recursos essenciais das skills."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for name in ("layla-docker", "layla-local", "project-research", "project-qa"):
    folder = root / "skills" / name
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{name}: frontmatter ausente"
    metadata = text.split("---", 2)[1]
    assert re.search(rf"^name: {re.escape(name)}$", metadata, re.M), f"{name}: nome inválido"
    assert re.search(r"^description: .+", metadata, re.M), f"{name}: descrição ausente"
    assert (folder / "agents/openai.yaml").is_file(), f"{name}: metadados de interface ausentes"
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in link:
            assert (folder / link).is_file(), f"{name}: referência quebrada: {link}"
    print(f"{name}: OK")
