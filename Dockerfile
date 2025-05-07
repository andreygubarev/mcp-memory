# syntax=docker/dockerfile:1
### Build stage ###############################################################
FROM ghcr.io/astral-sh/uv:bookworm-slim AS build
RUN uv python install 3.13

COPY . /usr/local/src/memory
WORKDIR /usr/local/src/memory
RUN uvx hatch build
RUN uv tool install dist/*.whl

### Release stage #############################################################
FROM debian:bookworm-slim AS release
LABEL org.opencontainers.image.title="mcp-remote-memory"
LABEL org.opencontainers.image.description=""
LABEL org.opencontainers.image.authors="Andrey Gubarev"

COPY --from=build /root/.local /root/.local
COPY chroma /root/.cache/chroma

ENV PATH="/root/.local/bin:${PATH}"
ENV MCP_PROXY_SSE_HOST=0.0.0.0
ENV MCP_PROXY_SSE_PORT=8000
ENV ANONYMIZED_TELEMETRY=False
ENV CHROMADB_DATABASE=/data
VOLUME ["/data"]
EXPOSE 8000
CMD ["mcp-memory"]
