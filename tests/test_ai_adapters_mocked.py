from unittest.mock import patch, MagicMock
from app.ai.adapters.local_adapter import LocalAIAdapter
from app.ai.adapters.openai_adapter import OpenAIAdapter
from app.ai.adapters.gemini_adapter import GeminiAdapter
from app.ai.adapters.anthropic_adapter import AnthropicAdapter
from app.ai.gateway import AIGateway


def test_local_ai_adapter():
    adapter = LocalAIAdapter()
    res = adapter.generate_response("I want a laptop under 50000 for coding", json_mode=True)
    assert res['success'] is True
    assert res['provider'] == 'local'
    assert 'category' in res['content']


def test_ai_gateway_fallback():
    # Gateway with invalid or unprovided key automatically falls back to local heuristic engine
    gateway = AIGateway(provider='openai', api_key='')
    res = gateway.generate("Recommend a good phone under 30000")
    assert res['success'] is True
    assert len(res['content']) > 0


def test_ai_gateway_local_selection():
    gateway = AIGateway(provider='local')
    res = gateway.generate("Recommend a good phone under 30000")
    assert res['success'] is True
    assert len(res['content']) > 0
