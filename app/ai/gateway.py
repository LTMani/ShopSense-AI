import time
import logging
from typing import Dict, Any, Optional
from flask import current_app
from app.ai.adapters import LocalAIAdapter, OpenAIAdapter, GeminiAdapter, AnthropicAdapter, BaseAIAdapter

logger = logging.getLogger(__name__)


class AIGateway:
    """Unified AI Gateway with automatic provider routing, graceful fallback, and telemetry."""

    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.provider = provider or 'local'
        self.api_key = api_key
        self.model_name = model_name
        self.local_adapter = LocalAIAdapter()
        self._active_adapter = self._init_adapter()

    def _init_adapter(self) -> BaseAIAdapter:
        try:
            if self.provider == 'openai' and self.api_key:
                return OpenAIAdapter(api_key=self.api_key, model_name=self.model_name or 'gpt-4o-mini')
            elif self.provider == 'gemini' and self.api_key:
                return GeminiAdapter(api_key=self.api_key, model_name=self.model_name or 'gemini-1.5-flash')
            elif self.provider == 'anthropic' and self.api_key:
                return AnthropicAdapter(api_key=self.api_key, model_name=self.model_name or 'claude-3-5-sonnet-20240620')
        except Exception as e:
            logger.warning(f"Failed to initialize external AI provider {self.provider}: {e}. Falling back to Local AI.")
        return self.local_adapter

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        start_time = time.time()
        try:
            result = self._active_adapter.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode
            )
            result['latency_ms'] = int((time.time() - start_time) * 1000)
            return result
        except Exception as err:
            logger.error(f"AI Provider error ({self.provider}): {err}. Invoking local fallback engine.")
            result = self.local_adapter.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode
            )
            result['fallback'] = True
            result['latency_ms'] = int((time.time() - start_time) * 1000)
            return result


def get_ai_gateway() -> AIGateway:
    """Factory helper to obtain AI Gateway configured with application environment variables."""
    provider = current_app.config.get('AI_PROVIDER', 'local') if current_app else 'local'
    api_key = current_app.config.get('AI_API_KEY', '') if current_app else ''
    model_name = current_app.config.get('AI_MODEL', 'local-hybrid-v1') if current_app else 'local-hybrid-v1'
    return AIGateway(provider=provider, api_key=api_key, model_name=model_name)
