# Architecture

`weav-ai-core` is the lowest-level package in the WeavInt AI package split. It gives downstream packages a stable import target for shared AI primitives while the implementation is still being migrated from `weav_core`.

## Design Goals

- Keep reusable AI primitives independent from product-specific infrastructure.
- Provide stable imports for downstream packages during migration.
- Make it possible to move implementations out of `weav_core` over time without changing caller imports.
- Keep the public API small enough to maintain intentionally.

## Dependency Direction

The intended dependency direction is:

```text
weav-ai-core
  -> weav-ai-providers
    -> weav-ai-runtime
      -> weav-server-ai-adapter
```

`weav-ai-core` must not import any downstream package. In particular, it should not import:

- provider-router construction code
- tenant or credential storage implementations
- database models or sessions
- server usage accounting
- product-specific configuration

## Current Implementation Strategy

Most exported symbols are re-exported from the migration dependency `weav_core`:

- `weav_core.runtime.agent`
- `weav_core.runtime.agent_profile`
- `weav_core.agent_loop`
- `weav_core.llm.*`
- `weav_core.rag.pipeline`
- `weav_core.tools.*`

This makes the package a compatibility layer today and a future implementation home later.

## Public Import Boundaries

Prefer domain-specific subpackage imports when a caller only needs one slice:

```python
from weav_ai_core.llm import LLMRouter
from weav_ai_core.tools import ToolRegistry
```

Use root imports when composing across multiple domains:

```python
from weav_ai_core import Agent, LLMRouter, ToolRegistry
```

## Adding New Exports

Before adding a new symbol to `__all__`, check that it is:

- needed by at least one downstream package or documented use case
- stable enough to support as part of the public API
- covered by a smoke test
- documented in `docs/api-reference.md`

Avoid exporting internal helpers, temporary migration utilities, or implementation details from `weav_core`.

## Migration Guidance

When moving an implementation from `weav_core` into this repository:

1. Keep the existing `weav_ai_core` import path stable.
2. Add or update tests before changing the import source.
3. Keep backwards-compatible behavior unless a breaking release is planned.
4. Document behavior changes in README and release notes.
5. Update downstream packages only after the core package is released.

## Testing Strategy

The current tests mock `weav_core` modules and validate the public export surface. This is intentional: it protects the package boundary without requiring the full server stack.

Future tests should add behavior coverage as implementations move into this repository.

## Release Considerations

The package currently uses a direct Git dependency for `weav-core`. Hatchling requires `tool.hatch.metadata.allow-direct-references = true` for this. Before a stable release, prefer one of these paths:

- publish the dependency as a versioned package
- pin the Git dependency to a tag or commit SHA
- migrate the required implementation directly into this repository
