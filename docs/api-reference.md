# API Reference

This document describes the public imports exposed by `weav-ai-core`. The package currently re-exports stable primitives from `weav_core`.

## Root Package

```python
from weav_ai_core import Agent, LLMRouter, ToolRegistry
```

The root package is convenient for application or runtime assembly code that needs multiple AI primitive domains.

### Exported Symbols

| Symbol | Purpose |
| --- | --- |
| `Agent` | Agent runtime type. |
| `AgentProfile` | Agent configuration/profile type. |
| `AgentLoop` | Agent loop contract or implementation entry point. |
| `AgentLoopRunner` | Runner for executing agent loop steps. |
| `AgentLoopStep` | Step model used by the agent loop. |
| `CompletionConfig` | LLM completion configuration type. |
| `LLMBase` | Base protocol or class for LLM providers. |
| `LLMRouter` | Router for registering and selecting LLM providers. |
| `ModelInfo` | Model metadata type. |
| `RAGPipeline` | RAG pipeline entry point. |
| `ToolContext` | Runtime context passed to tools. |
| `ToolInput` | Tool input contract. |
| `ToolOutput` | Tool output contract. |
| `ToolRegistry` | Registry for tool definitions. |
| `ToolSpec` | Tool specification contract. |

## Agent Imports

```python
from weav_ai_core.agent import Agent, AgentProfile
```

Use this import path when a caller only needs agent domain types.

## Agent Loop Imports

```python
from weav_ai_core.agent_loop import AgentLoop, AgentLoopRunner, AgentLoopStep
```

Use this import path for code that executes or inspects agent loop behavior.

## LLM Imports

```python
from weav_ai_core.llm import (
    CompletionConfig,
    LLMBase,
    LLMRouter,
    ModelInfo,
    add_usage,
    get_and_reset,
    usage_context,
)
```

`LLMRouter` is commonly used by `weav-ai-runtime` after credentials and providers are resolved.

Example:

```python
from weav_ai_core.llm import LLMRouter

router = LLMRouter()
# Runtime packages register provider instances on the router.
```

Usage helper exports are available for code that needs to track or reset LLM usage accounting state.

## RAG Imports

```python
from weav_ai_core.rag import RAGPipeline
```

Use this import path for retrieval-augmented generation pipeline integration.

## Tool Imports

```python
from weav_ai_core.tools import ToolContext, ToolInput, ToolOutput, ToolRegistry, ToolSpec
```

Example:

```python
from weav_ai_core.tools import ToolRegistry

tools = ToolRegistry()
```

## Compatibility Notes

Because this package currently re-exports `weav_core`, behavior is defined by the upstream implementation. This package owns the import path and public API boundary; it does not yet own every implementation detail.

## Public API Rules

- New public exports must be added to `__all__`.
- New public exports must be documented here.
- New public exports should have import smoke tests.
- Downstream packages should prefer `weav_ai_core` imports over direct `weav_core` imports.
