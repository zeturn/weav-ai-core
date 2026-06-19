# weav-ai-core

Reusable AI capability package for WeavInt.

This package is the stable import surface for AI primitives:

- LLM protocols, configs, router, and usage helpers
- Agent and AgentProfile
- AgentLoopRunner and loop models
- RAG pipeline components
- Tool registry and tool contracts

The current implementation re-exports the existing `weav_core` modules so downstream code can migrate incrementally without breaking the server.

