#!/usr/bin/env python3
"""Gera uma instalação independente, preservando configurações e dados existentes."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys

UPSTREAM_REV = "336ee4a362945b2badf8f48fcd5820cb132a7759"
ASSETS = Path(__file__).resolve().parents[1] / "assets" / "container"


def port_number(value):
    port = int(value)
    if not 1024 <= port <= 65535:
        raise argparse.ArgumentTypeError("Use uma porta entre 1024 e 65535.")
    return port


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.home() / "local-layla-runtime")
    parser.add_argument("--model", type=Path, help="GGUF existente a copiar para models/; opcional")
    parser.add_argument("--port", type=port_number, default=8000)
    parser.add_argument("--revision", default=UPSTREAM_REV, help="SHA completo do upstream")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("--revision precisa ser um SHA de 40 caracteres hexadecimais minúsculos")
    model = args.model.expanduser().resolve() if args.model else None
    if model:
        if not model.is_file() or model.suffix.lower() != ".gguf":
            parser.error("--model precisa apontar para um arquivo .gguf existente")
        with model.open("rb") as stream:
            if stream.read(4) != b"GGUF":
                parser.error("O arquivo não tem o cabeçalho GGUF.")
    root = args.output.expanduser().resolve()
    # Pré-validar conflitos antes de escrever; nunca sobrescrever uma instalação.
    generated = ["Dockerfile", ".dockerignore", "compose.yaml", "layla", ".env", "data/runtime_config.json"]
    conflicts = [str(root / name) for name in generated if (root / name).exists() or (root / name).is_symlink()]
    if conflicts:
        parser.error("Instalação já configurada. Edite os arquivos existentes ou use outro --output: " + ", ".join(conflicts))
    if model and ((root / "models" / model.name).exists() or (root / "models" / model.name).is_symlink()) and (root / "models" / model.name).resolve() != model:
        parser.error("Já existe um modelo com esse nome no destino; nenhum arquivo foi alterado.")
    for directory in ("data", "models", "workspace"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    for name in ("Dockerfile", ".dockerignore", "compose.yaml", "layla"):
        shutil.copyfile(ASSETS / name, root / name)
    (root / "layla").chmod(0o755)
    config = {
        "model_filename": model.name if model else "your-model.gguf",
        "models_dir": "/data/models",
        "sandbox_root": "/workspace",
        "n_gpu_layers": 0,
        "n_ctx": 4096,
        "n_batch": 256,
        # Sem travar, o auto-tune grava performance_mode=low em CPU, que corta
        # n_ctx para 2048 e trunca os pedidos sem avisar; 600 s não bastam a um 7B em CPU.
        "performance_mode": "mid",
        "completion_max_tokens": 512,
        "max_runtime_seconds": 900,
        "auto_tune_locked_keys": ["n_ctx", "completion_max_tokens", "performance_mode", "max_runtime_seconds"],
        "max_resident_models": 1,
        "response_language": "Portuguese",
        "remote_enabled": False,
        "scheduler_study_enabled": False,
        "system_tray_enabled": False,
    }
    (root / "data/runtime_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "data/runtime_config.json").chmod(0o600)
    if model and (root / "models" / model.name).resolve() != model:
        print("Copiando modelo GGUF (pode levar alguns minutos)…", flush=True)
        shutil.copy2(model, root / "models" / model.name)
    env = f"LAYLA_REV={args.revision}\nLAYLA_PORT={args.port}\nLOCAL_UID={getattr(os, 'getuid', lambda: 1000)()}\nLOCAL_GID={getattr(os, 'getgid', lambda: 1000)()}\nLAYLA_CPUS=4\nLAYLA_MEMORY=8g\n"
    (root / ".env").write_text(env, encoding="utf-8")
    (root / ".env").chmod(0o600)
    print(f"Instalação gerada em {root}")
    print(f"Execute: cd {str(root)!r} && ./layla up")
    print(f"Interface: http://127.0.0.1:{args.port}/ui")
    if not model:
        print("Nenhum modelo configurado: selecione/baixe um GGUF na interface antes de conversar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
