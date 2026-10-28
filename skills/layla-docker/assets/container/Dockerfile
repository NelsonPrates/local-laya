FROM python:3.12-slim-bookworm

ARG LAYLA_REV
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CMAKE_BUILD_PARALLEL_LEVEL=2 \
    CMAKE_ARGS="-DGGML_CUDA=OFF -DGGML_NATIVE=OFF" \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates build-essential cmake libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Não executar instaladores remotos; obter e verificar a revisão selecionada.
RUN test -n "$LAYLA_REV" \
    && git init /opt/layla \
    && cd /opt/layla \
    && git remote add origin https://github.com/PapaKoftes/Layla.git \
    && git fetch --depth 1 origin "$LAYLA_REV" \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "$LAYLA_REV" \
    && rm -rf .git

# O índice CPU evita baixar bibliotecas CUDA numa instalação sem GPU.
# `core` traz o chromadb: sem ele a memória e o índice do workspace caem num
# fallback sem busca vetorial e /health informa chroma_ok=false.
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir '/opt/layla[core,cpu,llm]'

WORKDIR /opt/layla/agent
# O chromadb envia telemetria anônima por padrão; a instância só fala com o loopback.
ENV HOME=/data LAYLA_DATA_DIR=/data ANONYMIZED_TELEMETRY=False
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-proxy-headers"]
