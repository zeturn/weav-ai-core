# weav-ai-core

Reusable AI capability package for WeavInt.

`weav-ai-core` is the stable import surface for shared AI primitives used by the WeavInt server and related packages. It currently re-exports the existing `weav_core` modules so downstream code can migrate incrementally without breaking the server.

## Scope

This package exposes:

- LLM protocols, configs, router, and usage helpers
- Agent and `AgentProfile`
- Agent loop contracts and runner types
- RAG pipeline components
- Tool registry and tool contracts

## Package Relationship

The AI packages are intended to be consumed in this order:

1. `weav-ai-core` provides shared primitives and compatibility imports.
2. `weav-ai-providers` exposes provider construction and model discovery.
3. `weav-ai-runtime` assembles credentials, model catalog, routing, and usage contracts.
4. `weav-server-ai-adapter` connects the reusable runtime to `weav_server` infrastructure.

## Installation

```bash
python -m pip install git+https://github.com/zeturn/weav-ai-core.git@main
```

For local development:

```bash
python -m pip install -e ".[dev]" --no-deps
```

`--no-deps` is useful for validating the package shell without requiring the upstream migration dependency to be installed locally.

## Usage

```python
from weav_ai_core import LLMRouter, ToolRegistry
from weav_ai_core.agent import Agent, AgentProfile
```

The public API is intentionally small. Add new exports only when they are stable enough for downstream packages to depend on.

## Development

Run the local quality checks:

```bash
python -m pytest
python -m build --wheel
```

## Release Notes

This package is currently in migration bootstrap status. Before cutting a production release, pin downstream dependencies to a tag or published package version instead of tracking `main`.
