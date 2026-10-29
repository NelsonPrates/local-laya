FROM python:3.12-slim-bookworm

ARG LAYLA_REV
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CMAKE_BUILD_PARALLEL_LEVEL=2 \
    CMAKE_ARGS="-DGGML_CUDA=OFF -DGGML_NATIVE=OFF" \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates build-essential cmake libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Do not run remote installers. Get the selected revision and check it.
RUN test -n "$LAYLA_REV" \
    && git init /opt/layla \
    && cd /opt/layla \
    && git remote add origin https://github.com/PapaKoftes/Layla.git \
    && git fetch --depth 1 origin "$LAYLA_REV" \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "$LAYLA_REV" \
    && rm -rf .git

# The CPU index prevents CUDA library downloads in an installation without a GPU.
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir '/opt/layla[cpu,llm]'

WORKDIR /opt/layla/agent
ENV HOME=/data LAYLA_DATA_DIR=/data
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-proxy-headers"]
