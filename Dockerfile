# syntax=docker/dockerfile:1
### Build stage ###############################################################
FROM ghcr.io/astral-sh/uv:bookworm-slim AS build
RUN uv python install 3.13
RUN uv tool install mcp-proxy

COPY . /usr/local/src/memory
WORKDIR /usr/local/src/memory
RUN uvx hatch build
RUN uv tool install dist/*.whl

### Release stage #############################################################
FROM debian:bookworm-slim AS release
LABEL org.opencontainers.image.title="mcp-remote-memory"
LABEL org.opencontainers.image.description=""
LABEL org.opencontainers.image.authors="Andrey Gubarev"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /root/.local /root/.local

ENV PATH="/root/.local/bin:${PATH}"
ENV MCP_PROXY_SSE_HOST=0.0.0.0
ENV MCP_PROXY_SSE_PORT=8080
ENV ANONYMIZED_TELEMETRY=False
ENV CHROMADB_DATABASE=/data
VOLUME ["/data"]
COPY --chown=root:root --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]
