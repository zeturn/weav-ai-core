# weav-ai-core

Reusable AI capability package for WeavInt.

`weav-ai-core` is the stable import surface for shared AI primitives used by the WeavInt server and related packages. It currently re-exports the existing `weav_core` modules so downstream code can migrate incrementally without breaking the server.

## When to Use This Package

Use `weav-ai-core` when you need one of the reusable AI primitives without depending directly on the larger server application:

- LLM protocol and routing types
- agent and agent profile types
- agent loop contracts
- RAG pipeline entry points
- tool registry and tool contract types

Do not use this package for provider-specific API key lookup, tenant-aware runtime assembly, database access, or server usage accounting. Those responsibilities live in the downstream packages described below.

## Package Relationship

The AI packages are intended to be consumed in this order:

1. `weav-ai-core` provides shared primitives and compatibility imports.
2. `weav-ai-providers` exposes provider construction and model discovery.
3. `weav-ai-runtime` assembles credentials, model catalog, routing, and usage contracts.
4. `weav-server-ai-adapter` connects the reusable runtime to `weav_server` infrastructure.

`weav-ai-core` should stay at the bottom of this stack. It should not import runtime, provider, database, or product-specific server modules.

## Public API Overview

The root package exports the stable symbols most callers need:

```python
from weav_ai_core import (
    Agent,
    AgentProfile,
    AgentLoop,
    AgentLoopRunner,
    CompletionConfig,
    LLMBase,
    LLMRouter,
    ModelInfo,
    RAGPipeline,
    ToolContext,
    ToolInput,
    ToolOutput,
    ToolRegistry,
    ToolSpec,
)
```

Subpackages provide narrower imports when a caller wants an explicit domain boundary:

```python
from weav_ai_core.agent import Agent, AgentProfile
from weav_ai_core.agent_loop import AgentLoopRunner
from weav_ai_core.llm import LLMRouter, CompletionConfig, usage_context
from weav_ai_core.rag import RAGPipeline
from weav_ai_core.tools import ToolRegistry, ToolSpec
```

See [docs/api-reference.md](docs/api-reference.md) for details.

## Architecture

This package is intentionally a compatibility and stabilization layer. It currently re-exports types from `weav_core`, which is pulled from the migration source repository through `pyproject.toml`.

That means the package has two jobs:

- give downstream packages a small stable import target
- make future extraction from `weav_core` possible without forcing downstream import churn

See [docs/architecture.md](docs/architecture.md) for package boundaries and migration guidance.

## Installation

Install from the current main branch:

```bash
python -m pip install git+https://github.com/zeturn/weav-ai-core.git@main
```

For local development:

```bash
python -m pip install -e ".[dev]"
```

For package-shell validation without installing migration-time upstream dependencies:

```bash
python -m pip install -e . --no-deps
```

## Quick Start

```python
from weav_ai_core.llm import LLMRouter
from weav_ai_core.tools import ToolRegistry

router = LLMRouter()
tools = ToolRegistry()
```

Provider registration is handled by `weav-ai-runtime` and `weav-ai-providers`; this package only exposes the shared primitive types.

## Development

Run the local quality checks:

```bash
python -m pytest
python -m build --wheel
```

The test suite includes public API smoke tests that mock the migration dependency. These tests protect the exported import surface without requiring the full server stack.

## Release Notes

This package is currently in migration bootstrap status. Before cutting a production release, pin downstream dependencies to a tag or published package version instead of tracking `main`.

Recommended release order:

1. tag and release `weav-ai-core`
2. update `weav-ai-providers` to depend on that tag or package version
3. release downstream packages in dependency order

## Governance

- Security reporting: see [SECURITY.md](SECURITY.md)
- Contribution workflow: see [CONTRIBUTING.md](CONTRIBUTING.md)
- License: Apache-2.0, see [LICENSE](LICENSE)
