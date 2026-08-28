import requests
from typing import Dict, Any, Optional
from app.ai.adapters.base import BaseAIAdapter


class AnthropicAdapter(BaseAIAdapter):
    """Adapter for Anthropic Claude API."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = 'claude-3-5-sonnet-20240620'):
        super().__init__(api_key, model_name)
        self.endpoint = 'https://api.anthropic.com/v1/messages'

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("Anthropic API Key is missing.")

        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model_name,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'messages': [{'role': 'user', 'content': prompt}]
        }
        if system_prompt:
            payload['system'] = system_prompt

        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        content = data['content'][0]['text']
        usage = data.get('usage', {})

        return {
            'content': content,
            'model': self.model_name,
            'provider': 'anthropic',
            'prompt_tokens': usage.get('input_tokens', 0),
            'completion_tokens': usage.get('output_tokens', 0),
            'success': True
        }
