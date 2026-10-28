#!/usr/bin/env python3
"""Instala cópias independentes das skills próprias, sem sobrescrever destinos."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents" / "skills")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "skills"
    target = args.target.expanduser().resolve()
    names = ("layla-docker", "layla-local", "layla-tuning", "layla-benchmark", "project-research", "project-qa")
    conflicts = [str(target / name) for name in names if (target / name).exists() or (target / name).is_symlink()]
    if conflicts:
        parser.error("Destino já existe; nenhum arquivo foi alterado: " + ", ".join(conflicts))
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(source / name, target / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"Skill instalada: {target / name}")


if __name__ == "__main__":
    main()
