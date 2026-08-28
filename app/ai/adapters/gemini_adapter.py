import requests
from typing import Dict, Any, Optional
from app.ai.adapters.base import BaseAIAdapter


class GeminiAdapter(BaseAIAdapter):
    """Adapter for Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = 'gemini-1.5-flash'):
        super().__init__(api_key, model_name)

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("Gemini API Key is missing.")

        url = f'https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}'
        contents = []
        if system_prompt:
            contents.append({'role': 'user', 'parts': [{'text': f'System Instructions: {system_prompt}'}]})
        contents.append({'role': 'user', 'parts': [{'text': prompt}]})

        payload = {
            'contents': contents,
            'generationConfig': {
                'temperature': temperature,
                'maxOutputTokens': max_tokens
            }
        }
        if json_mode:
            payload['generationConfig']['responseMimeType'] = 'application/json'

        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        candidate = data['candidates'][0]['content']['parts'][0]['text']
        usage = data.get('usageMetadata', {})

        return {
            'content': candidate,
            'model': self.model_name,
            'provider': 'gemini',
            'prompt_tokens': usage.get('promptTokenCount', 0),
            'completion_tokens': usage.get('candidatesTokenCount', 0),
            'success': True
        }
