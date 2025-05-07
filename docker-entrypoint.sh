#!/usr/bin/env bash
set -eux
mcp-proxy --pass-environment --sse-host=${MCP_PROXY_SSE_HOST} --sse-port=${MCP_PROXY_SSE_PORT} -- mcp-memory
