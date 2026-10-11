#!/usr/bin/env python3
"""Confere a integridade da cópia local do Superpowers contra seu lock."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1] / "vendor/superpowers"
lock = json.loads((root / "source.lock.json").read_text(encoding="utf-8"))
actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and p.name != "source.lock.json" and "__pycache__" not in p.parts}
if actual != lock["sha256"]:
    print("Superpowers foi alterado ou está incompleto; conferir origem e atualizar o lock conscientemente.", file=sys.stderr)
    sys.exit(1)
executable = [p.relative_to(root).as_posix() for p in sorted(root.rglob("*")) if p.is_file() and p.stat().st_mode & 0o111]
if executable != lock.get("executable", []):
    print("Permissões executáveis do Superpowers divergem do lock.", file=sys.stderr)
    sys.exit(1)
print(f"Superpowers íntegro: {lock['revision']} ({len(actual)} arquivos)")
