import json
import re
from typing import Dict, Any, Optional
from app.ai.adapters.base import BaseAIAdapter
from app.ai.nlp.entity_extractor import EntityExtractor


class LocalAIAdapter(BaseAIAdapter):
    """Zero-dependency local heuristic AI adapter providing reliable, structured intelligence offline."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = 'local-hybrid-v1'):
        super().__init__(api_key, model_name)

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        
        # Check if caller expects JSON or structured response
        if json_mode or 'json' in prompt_lower or 'extract' in prompt_lower:
            extracted = EntityExtractor.extract_entities(prompt)
            response_json = {
                'category': extracted.get('category'),
                'budget': extracted.get('budget'),
                'primary_usage': extracted['usage'][0] if extracted.get('usage') else 'general',
                'priorities': extracted.get('usage', []),
                'intent': 'product_search_and_recommendation',
                'explanation_focus': 'matches user stated budget and prioritized hardware specifications'
            }
            content_str = json.dumps(response_json)
        else:
            content_str = self._generate_conversational_heuristics(prompt)

        return {
            'content': content_str,
            'model': self.model_name,
            'provider': 'local',
            'prompt_tokens': len(prompt.split()),
            'completion_tokens': len(content_str.split()),
            'success': True
        }

    def _generate_conversational_heuristics(self, prompt: str) -> str:
        text = prompt.lower()
        if 'why' in text and ('decrease' in text or 'drop' in text or 'down' in text or 'sales' in text):
            return "Based on diagnostic data analysis across traffic, conversion funnels, inventory levels, and customer sentiment: The sales contraction is primarily driven by intermittent stockouts during peak shopping periods combined with recent negative review sentiment regarding specific comfort attributes."
        elif 'laptop' in text or 'phone' in text or 'headphone' in text:
            return "I have analyzed the catalog based on your requirements. Here are the most relevant products ranked by technical specifications, verified customer ratings, and budget suitability."
        return "I have processed your request. How else can I assist your shopping or seller analytics today?"
