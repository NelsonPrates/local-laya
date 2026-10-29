---
name: layla-docker
description: Create scripts for PapaKoftes/Layla in Docker Compose and guide its local installation, configuration, and operation with a GGUF model and persistent data. Use it to prepare or diagnose the container. To talk to a running instance, use layla-local.
---

# Layla in Docker

Use the included generator to make an independent installation. Explain its commands to the user. The target project is [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla). Do not confuse it with Layla-Server, the mobile app, or Ollama.

1. Check for Python 3.10+, a running Docker Engine or Docker Desktop, and Compose v2 (`docker info`, `docker compose version`). If one is missing, read the official instructions for the user's system. Do not install packages for a different system.
2. Select an installation directory. Use a GGUF model that the user supplies. Alternatively, prepare only the interface so that the user can select or download a model later. Do not invent model URLs. Do not download many GB unless the request includes it.
3. Run this command from this skill folder:

   ```bash
   python3 scripts/setup.py --output ~/local-layla-runtime --model /path/to/model.gguf
   ```

   `--model` is optional. Use `--port 8001` if port 8000 is busy. The generator copies the GGUF file. It refuses to overwrite an existing installation. Do not delete data to avoid this refusal.
4. In the generated directory, run `./layla config`. If the user asked for the installation, run `./layla up`. The first CPU build can take several minutes and download large dependencies. Tell the user about the progress and the errors that you see.
5. Run `./layla health`, open `http://127.0.0.1:PORT/ui`, and run `./layla ready`. Report inference as ready only when `model_loaded` is true and the model answers a simple message. An API that responds and a healthy container do not prove inference.

Read [references/operations.md](references/operations.md) for the model, limits, updates, backup, and Docker problems. The files in `assets/container/` are editable templates. Adapt them when the user asks for different scripts. Keep the volumes and paths consistent.

The defaults are CPU only, `n_gpu_layers=0`, a port published only on `127.0.0.1`, data in `/data`, models in `/data/models`, and the workspace in `/workspace`. Do not mount the full home folder or the Docker socket. Do not describe this CPU image as CUDA acceleration. A GPU needs a different image and its own tests.

Keep the upstream SHA explicit and checked. Do not use `latest` as a stable revision. A new revision needs new checks of Docker, schemas, and readiness. The build still resolves the Python dependencies and the base image. The SHA alone does not make the build reproducible byte for byte.
