import importlib
import sys
import types


def _package(monkeypatch, name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = []
    monkeypatch.setitem(sys.modules, name, module)
    return module


def _module(monkeypatch, name: str, **attrs: object) -> types.ModuleType:
    module = types.ModuleType(name)
    for attr_name, value in attrs.items():
        setattr(module, attr_name, value)
    monkeypatch.setitem(sys.modules, name, module)
    parent_name, _, child_name = name.rpartition(".")
    if parent_name and parent_name in sys.modules:
        setattr(sys.modules[parent_name], child_name, module)
    return module


def _type(name: str) -> type:
    return type(name, (), {})


def install_weav_core_stubs(monkeypatch):
    for package_name in [
        "weav_core",
        "weav_core.runtime",
        "weav_core.llm",
        "weav_core.rag",
        "weav_core.tools",
    ]:
        _package(monkeypatch, package_name)

    _module(monkeypatch, "weav_core.runtime.agent", Agent=_type("Agent"))
    _module(monkeypatch, "weav_core.runtime.agent_profile", AgentProfile=_type("AgentProfile"))
    _module(
        monkeypatch,
        "weav_core.agent_loop",
        AgentLoop=_type("AgentLoop"),
        AgentLoopRunner=_type("AgentLoopRunner"),
        AgentLoopStep=_type("AgentLoopStep"),
    )
    _module(
        monkeypatch,
        "weav_core.llm.base",
        CompletionConfig=_type("CompletionConfig"),
        LLMBase=_type("LLMBase"),
        ModelInfo=_type("ModelInfo"),
    )
    _module(monkeypatch, "weav_core.llm.router", LLMRouter=_type("LLMRouter"))
    _module(
        monkeypatch,
        "weav_core.llm.usage",
        add_usage=lambda *args, **kwargs: None,
        get_and_reset=lambda: None,
        usage_context=lambda: None,
    )
    _module(monkeypatch, "weav_core.rag.pipeline", RAGPipeline=_type("RAGPipeline"))
    _module(
        monkeypatch,
        "weav_core.tools.base",
        ToolContext=_type("ToolContext"),
        ToolInput=_type("ToolInput"),
        ToolOutput=_type("ToolOutput"),
        ToolSpec=_type("ToolSpec"),
    )
    _module(monkeypatch, "weav_core.tools.registry", ToolRegistry=_type("ToolRegistry"))


def test_root_exports_public_api(monkeypatch):
    install_weav_core_stubs(monkeypatch)

    package = importlib.import_module("weav_ai_core")

    assert "LLMRouter" in package.__all__
    assert "ToolRegistry" in package.__all__
    assert package.Agent.__name__ == "Agent"
    assert package.RAGPipeline.__name__ == "RAGPipeline"


def test_subpackage_exports_are_stable(monkeypatch):
    install_weav_core_stubs(monkeypatch)

    llm = importlib.import_module("weav_ai_core.llm")
    tools = importlib.import_module("weav_ai_core.tools")
    agent = importlib.import_module("weav_ai_core.agent")
    rag = importlib.import_module("weav_ai_core.rag")

    assert "usage_context" in llm.__all__
    assert "ToolSpec" in tools.__all__
    assert agent.AgentProfile.__name__ == "AgentProfile"
    assert rag.RAGPipeline.__name__ == "RAGPipeline"
