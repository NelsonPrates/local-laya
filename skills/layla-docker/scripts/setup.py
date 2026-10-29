#!/usr/bin/env python3
"""Generate an independent installation. Keep the existing configuration and data."""
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
        raise argparse.ArgumentTypeError("Use a port from 1024 to 65535.")
    return port


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.home() / "local-layla-runtime")
    parser.add_argument("--model", type=Path, help="Optional. An existing GGUF file to copy to models/")
    parser.add_argument("--port", type=port_number, default=8000)
    parser.add_argument("--revision", default=UPSTREAM_REV, help="Full upstream SHA")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("--revision must be a SHA of 40 lowercase hexadecimal characters")
    model = args.model.expanduser().resolve() if args.model else None
    if model:
        if not model.is_file() or model.suffix.lower() != ".gguf":
            parser.error("--model must point to an existing .gguf file")
        with model.open("rb") as stream:
            if stream.read(4) != b"GGUF":
                parser.error("The file does not have the GGUF header.")
    root = args.output.expanduser().resolve()
    # Find conflicts before the first write. Never overwrite an installation.
    generated = ["Dockerfile", ".dockerignore", "compose.yaml", "layla", ".env", "data/runtime_config.json"]
    conflicts = [str(root / name) for name in generated if (root / name).exists() or (root / name).is_symlink()]
    if conflicts:
        parser.error("The installation exists. Edit the existing files or use a different --output: " + ", ".join(conflicts))
    if model and ((root / "models" / model.name).exists() or (root / "models" / model.name).is_symlink()) and (root / "models" / model.name).resolve() != model:
        parser.error("A model with this name exists in the target. No file changed.")
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
        "max_resident_models": 1,
        "response_language": "English",
        "remote_enabled": False,
        "scheduler_study_enabled": False,
        "system_tray_enabled": False,
    }
    (root / "data/runtime_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "data/runtime_config.json").chmod(0o600)
    if model and (root / "models" / model.name).resolve() != model:
        print("Copying the GGUF model. This can take a few minutes…", flush=True)
        shutil.copy2(model, root / "models" / model.name)
    env = f"LAYLA_REV={args.revision}\nLAYLA_PORT={args.port}\nLOCAL_UID={getattr(os, 'getuid', lambda: 1000)()}\nLOCAL_GID={getattr(os, 'getgid', lambda: 1000)()}\nLAYLA_CPUS=4\nLAYLA_MEMORY=8g\n"
    (root / ".env").write_text(env, encoding="utf-8")
    (root / ".env").chmod(0o600)
    print(f"Installation generated in {root}")
    print(f"Run: cd {str(root)!r} && ./layla up")
    print(f"Interface: http://127.0.0.1:{args.port}/ui")
    if not model:
        print("No model is configured. Select or download a GGUF model in the interface before you chat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
