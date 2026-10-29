# Operation of the generated installation

## Dependencies and first use

- Python 3.10+ and Bash on the host. Linux is the main target. On Windows, use WSL2 with the Docker Desktop integration. On macOS, use Docker Desktop and Python 3.
- [Docker Engine](https://docs.docker.com/engine/install/) or [Docker Desktop](https://docs.docker.com/desktop/) with [Compose v2](https://docs.docker.com/compose/install/).
- Git and compilers are in the image. The generated runtime does not need them on the host.
- The CPU image includes the memory and inference dependencies. Reserve several GB of disk space and time for the build. The necessary memory depends on the GGUF model. `8g` is an initial limit. It does not guarantee that every model fits.

Generate the installation without `--model` to use the setup flow in `/ui`. The app can download a model and embedding models during setup or first use. Local inference does not mean that the first installation works without internet access.

For an existing GGUF file, `--model` copies the file to `models/` and sets its name. The generator checks the GGUF header. Only a loaded model proves compatibility. You can also copy a GGUF file manually to `models/`, set `model_filename` in `data/runtime_config.json`, and restart.

## Paths and configuration

| Host (generated directory) | Container | Use |
| --- | --- | --- |
| `data/` | `/data` | Database, configuration, cache, and persistent state |
| `models/` | `/data/models` | GGUF models, including downloads from the interface |
| `workspace/` | `/workspace` | Files that you want to give to Layla |

Edit `.env` for `LAYLA_PORT`, `LAYLA_CPUS`, and `LAYLA_MEMORY`. Run `./layla up` to create the container again with these values. Edit `data/runtime_config.json` for `model_filename`, `n_ctx`, `n_threads`, and the language. Then run `./layla restart`. The app keeps the existing configuration and adds missing defaults.

The generated UID and GID match the host user. Do not run `setup.py` with sudo. On Linux with rootless Docker or user namespaces, check the bind mount permissions for the effective container UID. On macOS and Windows, Docker Desktop manages the shared folders.

## API and authorized operations

The network client connects through the Docker bridge. Some upstream routes check for a direct loopback connection. For example, `POST /approve` can return 403 even when you call it from the host localhost. `./layla approve ID` calls `/approve` from inside the container. This is a real approval. Use it only for the specific action that the user authorized.

The Uvicorn command disables proxy header processing. Do not try to simulate localhost with `X-Forwarded-For`. Do not enable `remote_enabled` to avoid restrictions. The upstream also disables writes and execution for `/agent` requests through the bridge. The client of the other skill already sends both flags as `false`.

## Common problems

- Docker does not respond: start the Engine or Desktop. Run `docker info` and check the user's access to the daemon. Do not change groups or permissions automatically only to run a diagnosis.
- Port is busy: change `LAYLA_PORT` in `.env` and run `./layla up`. Update `LAYLA_BASE_URL` for the client on the host.
- Container stops or is slow: run `./layla status` and `docker compose logs --tail 100 layla`. The first build can take a long time. The 600-second limit of `up` applies to startup after the build.
- `model_loaded=false`: check the file name, the mount, the supported format, the logs, and the memory. `./layla ready` returns exit code 1 in this case.
- Out of memory: use a smaller GGUF model, decrease `n_ctx` or `n_batch`, or increase the available memory and `LAYLA_MEMORY`.
- The app cannot find a host path: copy the file to `workspace/` and use `/workspace/file` in the conversation.
- The build fails on a dependency: keep the error. Check the architecture support and the upstream versions. Do not report the installation as complete.
- `exec ... operation not permitted` before the app starts: on some hosts, Docker cannot run images with `no-new-privileges`. The template does not enable this option. Check local overrides before you change the daemon or the host.

## Stop, back up, and update

`./layla down` removes the container and the network. It keeps the directories. For a consistent backup, stop the container. Then archive `data/`, `models/`, `workspace/`, `.env`, `compose.yaml`, and `Dockerfile`. A copy of the database while the app writes to it is not guaranteed to be consistent. Make sure that you can read the backup before you remove an installation.

To update:

1. Make a backup.
2. Find the necessary revision in the upstream repository.
3. Replace `LAYLA_REV` in `.env` with its full 40-character SHA.
4. Run `./layla up`.
5. Check `/openapi.json`, `/health`, and one conversation.

If a regression occurs, restore the revision and the data from a compatible backup. An older image does not undo database migrations.

## Checked sources

Base revision: `336ee4a362945b2badf8f48fcd5820cb132a7759`.

- [Upstream Dockerfile](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/Dockerfile)
- [CPU and LLM extras](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/pyproject.toml)
- [Configuration and persistent paths](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/runtime_safety.py)
- [Layla license](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/LICENSE): non-commercial use. Read the terms before commercial use.
