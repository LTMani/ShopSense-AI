import json
import os
import requests
from typing import Dict, Any, Optional
from app.ai.adapters.base import BaseAIAdapter


class OpenAIAdapter(BaseAIAdapter):
    """Adapter for OpenAI API (GPT-4o / GPT-3.5-turbo)."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = 'gpt-4o-mini'):
        super().__init__(api_key, model_name)
        self.endpoint = 'https://api.openai.com/v1/chat/completions'

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("OpenAI API Key is missing. Check your environment settings.")

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        payload = {
            'model': self.model_name,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        if json_mode:
            payload['response_format'] = {'type': 'json_object'}

        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        choice = data['choices'][0]['message']
        usage = data.get('usage', {})

        return {
            'content': choice['content'],
            'model': self.model_name,
            'provider': 'openai',
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'success': True
        }
