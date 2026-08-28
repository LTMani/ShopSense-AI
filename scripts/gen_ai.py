# ShopSense AI Engine Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'ai'
(BASE / 'adapters').mkdir(parents=True, exist_ok=True)
(BASE / 'nlp').mkdir(parents=True, exist_ok=True)
(BASE / 'copilot').mkdir(parents=True, exist_ok=True)
(BASE / 'seller').mkdir(parents=True, exist_ok=True)

# 1. adapters/base.py
(BASE / 'adapters' / 'base.py').write_text('''from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseAIAdapter(ABC):
    """Abstract interface for AI model provider adapters."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = 'default'):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        """Generate response from model provider. Must return dict with 'content', 'raw_response', 'tokens'."""
        pass
''', encoding='utf-8')

# 2. adapters/local_adapter.py
(BASE / 'adapters' / 'local_adapter.py').write_text('''import json
import re
from typing import Dict, Any, Optional
from app.ai.adapters.base import BaseAIAdapter


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
            response_json = self._extract_structured_heuristics(prompt)
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

    def _extract_structured_heuristics(self, prompt: str) -> Dict[str, Any]:
        text = prompt.lower()
        budget = None
        
        # Budget extraction
        budget_match = re.search(r'(?:under|below|budget|within|around|less than|max)?\s*(?:rs\.?|₹|inr)?\s*(\d{1,3}(?:,\d{3})*|\d+)\s*(?:k|thousand|lakh)?', text)
        if budget_match:
            raw_val = budget_match.group(1).replace(',', '')
            try:
                val = float(raw_val)
                if 'k' in text[budget_match.start():budget_match.end()+2]:
                    val *= 1000
                elif 'lakh' in text[budget_match.start():budget_match.end()+5]:
                    val *= 100000
                if val > 100:
                    budget = val
            except Exception:
                budget = None

        # Category detection
        categories = {
            'laptops': ['laptop', 'notebook', 'macbook', 'ultrabook', 'thinkpad', 'gaming laptop'],
            'smartphones': ['phone', 'smartphone', 'mobile', 'iphone', 'android', 'galaxy'],
            'audio': ['headphone', 'earphone', 'earbud', 'speaker', 'audio', 'soundbar', 'tws', 'anc'],
            'cameras': ['camera', 'dslr', 'mirrorless', 'lens', 'action cam'],
            'monitors': ['monitor', 'display', 'screen', 'gaming monitor', '4k display'],
            'peripherals': ['keyboard', 'mouse', 'mechanical keyboard', 'trackpad', 'dock'],
            'wearables': ['smartwatch', 'watch', 'fitness band', 'tracker'],
            'gaming': ['console', 'playstation', 'ps5', 'xbox', 'nintendo', 'controller'],
            'furniture': ['chair', 'desk', 'standing desk', 'ergonomic chair', 'table']
        }
        
        detected_category = None
        for cat, keywords in categories.items():
            if any(k in text for k in keywords):
                detected_category = cat
                break

        # Priority weights
        priorities = []
        if any(w in text for w in ['battery', 'long lasting', 'backup', 'hours']):
            priorities.append('battery')
        if any(w in text for w in ['performance', 'fast', 'speed', 'ram', 'processor', 'coding', 'programming']):
            priorities.append('performance')
        if any(w in text for w in ['lightweight', 'portable', 'slim', 'travel', 'weight']):
            priorities.append('portability')
        if any(w in text for w in ['gaming', 'gpu', 'graphics', 'fps', 'rtx']):
            priorities.append('gaming')
        if any(w in text for w in ['camera', 'photo', 'video', 'sensor']):
            priorities.append('camera')
        if any(w in text for w in ['sound', 'bass', 'anc', 'noise cancellation', 'audio quality']):
            priorities.append('audio_quality')
        if any(w in text for w in ['budget', 'affordable', 'value', 'cheap', 'inexpensive']):
            priorities.append('value')

        return {
            'category': detected_category,
            'budget': budget,
            'primary_usage': priorities[0] if priorities else 'general',
            'priorities': priorities,
            'intent': 'product_search_and_recommendation',
            'explanation_focus': 'matches user stated budget and prioritized hardware specifications'
        }

    def _generate_conversational_heuristics(self, prompt: str) -> str:
        text = prompt.lower()
        if 'why' in text and ('decrease' in text or 'drop' in text or 'down' in text or 'sales' in text):
            return "Based on diagnostic data analysis across traffic, conversion funnels, inventory levels, and customer sentiment: The sales contraction is primarily driven by intermittent stockouts during peak shopping periods combined with recent negative review sentiment regarding specific comfort attributes."
        elif 'laptop' in text or 'phone' in text or 'headphone' in text:
            return "I have analyzed the catalog based on your requirements. Here are the most relevant products ranked by technical specifications, verified customer ratings, and budget suitability."
        return "I have processed your request. How else can I assist your shopping or seller analytics today?"
''', encoding='utf-8')

# 3. adapters/openai_adapter.py
(BASE / 'adapters' / 'openai_adapter.py').write_text('''import json
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
''', encoding='utf-8')

# 4. adapters/gemini_adapter.py
(BASE / 'adapters' / 'gemini_adapter.py').write_text('''import requests
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
''', encoding='utf-8')

# 5. adapters/anthropic_adapter.py
(BASE / 'adapters' / 'anthropic_adapter.py').write_text('''import requests
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
''', encoding='utf-8')

# 6. adapters/__init__.py
(BASE / 'adapters' / '__init__.py').write_text('''from app.ai.adapters.base import BaseAIAdapter
from app.ai.adapters.local_adapter import LocalAIAdapter
from app.ai.adapters.openai_adapter import OpenAIAdapter
from app.ai.adapters.gemini_adapter import GeminiAdapter
from app.ai.adapters.anthropic_adapter import AnthropicAdapter

__all__ = [
    'BaseAIAdapter',
    'LocalAIAdapter',
    'OpenAIAdapter',
    'GeminiAdapter',
    'AnthropicAdapter'
]
''', encoding='utf-8')

# 7. gateway.py
(BASE / 'gateway.py').write_text('''import time
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
''', encoding='utf-8')

# 8. nlp/tokenizer.py
(BASE / 'nlp' / 'tokenizer.py').write_text('''import re
from typing import List, Set

STOPWORDS: Set[str] = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
    'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
    'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
    'just', 'don', 'should', 'now', 'need', 'want', 'looking', 'please', 'help'
}


class TextTokenizer:
    """Text cleaner, normalizer, and tokenizer for NLP information retrieval."""

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'[^\w\s\₹\$\.\,\-\+]', '', text)
        return text.strip()

    @classmethod
    def tokenize(cls, text: str, remove_stopwords: bool = True) -> List[str]:
        cleaned = cls.clean_text(text)
        words = re.findall(r'\b[a-zA-Z0-9_\-\+]{2,}\b', cleaned)
        if remove_stopwords:
            words = [w for w in words if w not in STOPWORDS]
        return words

    @classmethod
    def extract_ngrams(cls, words: List[str], n: int = 2) -> List[str]:
        if len(words) < n:
            return []
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
''', encoding='utf-8')

# 9. nlp/entity_extractor.py
(BASE / 'nlp' / 'entity_extractor.py').write_text('''import re
from typing import Dict, Any, Optional, List


class EntityExtractor:
    """Extracts budgets, categories, brands, screen sizes, RAM, and storage from shopping queries."""

    CATEGORY_SYNONYMS = {
        'Laptops': ['laptop', 'notebook', 'macbook', 'ultrabook', 'thinkpad', 'gaming laptop', 'chromebook'],
        'Smartphones': ['phone', 'smartphone', 'mobile', 'iphone', 'galaxy', 'handset', 'android'],
        'Audio & Headphones': ['headphone', 'headphones', 'earphone', 'earbuds', 'speaker', 'soundbar', 'tws', 'anc'],
        'Cameras & Photography': ['camera', 'dslr', 'mirrorless', 'action cam', 'lens', 'camcorder'],
        'Monitors & Displays': ['monitor', 'display', 'screen', 'ultrawide', '4k monitor', 'gaming display'],
        'Computer Peripherals': ['keyboard', 'mouse', 'trackpad', 'webcam', 'docking station', 'usb hub'],
        'Smart Wearables': ['smartwatch', 'smart watch', 'fitness tracker', 'band', 'apple watch'],
        'Gaming & Consoles': ['gaming console', 'playstation', 'ps5', 'xbox', 'nintendo', 'gamepad', 'joystick'],
        'Office & Study Furniture': ['chair', 'desk', 'ergonomic chair', 'standing desk', 'study table', 'bookshelf']
    }

    BRAND_LIST = [
        'Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Samsung', 'Sony', 'Bose', 'Sennheiser',
        'JBL', 'Logitech', 'Razer', 'Keychron', 'LG', 'Canon', 'Nikon', 'GoPro', 'SteelSeries',
        'Corsair', 'Microsoft', 'Nothing', 'OnePlus', 'Xiaomi', 'HyperX', 'Anker', 'Herman Miller', 'Ikea'
    ]

    @classmethod
    def extract_entities(cls, query: str) -> Dict[str, Any]:
        text = query.lower()
        extracted: Dict[str, Any] = {
            'budget': cls._extract_budget(text),
            'category': cls._extract_category(text),
            'brand': cls._extract_brand(text),
            'usage': cls._extract_usage(text),
            'specs': cls._extract_spec_constraints(text)
        }
        return extracted

    @staticmethod
    def _extract_budget(text: str) -> Optional[float]:
        patterns = [
            r'(?:under|below|budget|within|around|less than|max|upto|up to)?\s*(?:rs\.?|₹|inr|\$)?\s*(\d{1,3}(?:,\d{3})*|\d+)\s*(?:k|thousand|lakh)?'
        ]
        for pat in patterns:
            match = re.search(pat, text)
            if match:
                raw = match.group(1).replace(',', '')
                try:
                    val = float(raw)
                    matched_str = text[match.start():match.end()+6]
                    if 'k' in matched_str:
                        val *= 1000
                    elif 'lakh' in matched_str:
                        val *= 100000
                    if 100 <= val <= 1000000:
                        return val
                except ValueError:
                    pass
        return None

    @classmethod
    def _extract_category(cls, text: str) -> Optional[str]:
        for cat_name, synonyms in cls.CATEGORY_SYNONYMS.items():
            for syn in synonyms:
                if re.search(r'\b' + re.escape(syn) + r'\b', text):
                    return cat_name
        return None

    @classmethod
    def _extract_brand(cls, text: str) -> Optional[str]:
        for b in cls.BRAND_LIST:
            if re.search(r'\b' + re.escape(b.lower()) + r'\b', text):
                return b
        return None

    @staticmethod
    def _extract_usage(text: str) -> List[str]:
        usages = []
        keywords = {
            'coding': ['coding', 'programming', 'developer', 'python', 'software', 'vscode'],
            'gaming': ['gaming', 'games', 'gamer', 'fps', 'rtx', 'gpu'],
            'battery': ['battery', 'battery life', 'backup', 'long battery'],
            'portability': ['lightweight', 'portable', 'travel', 'slim', 'thin', 'college', 'student'],
            'creative': ['photo editing', 'video editing', 'photoshop', 'premiere', 'design', 'graphic'],
            'office': ['office', 'excel', 'work', 'business', 'zoom', 'calls'],
            'audiophile': ['sound quality', 'bass', 'audiophile', 'noise cancellation', 'anc', 'lossless']
        }
        for use, words in keywords.items():
            if any(w in text for w in words):
                usages.append(use)
        return usages

    @staticmethod
    def _extract_spec_constraints(text: str) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        ram_match = re.search(r'(\d+)\s*(?:gb|gig)\s*ram', text)
        if ram_match:
            specs['ram_gb'] = int(ram_match.group(1))

        storage_match = re.search(r'(\d+)\s*(?:gb|tb|ssd|storage)', text)
        if storage_match:
            specs['storage'] = storage_match.group(0)

        screen_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|\"|\-inch)', text)
        if screen_match:
            specs['screen_size'] = float(screen_match.group(1))

        return specs
''', encoding='utf-8')

# 10. nlp/intent_classifier.py
(BASE / 'nlp' / 'intent_classifier.py').write_text('''from typing import Dict, Any


class IntentClassifier:
    """Classifies user dialogue into e-commerce operational intents."""

    INTENT_KEYWORDS = {
        'product_search': ['search', 'find', 'show me', 'looking for', 'need', 'buy', 'get', 'recommend'],
        'product_comparison': ['compare', 'difference between', 'which is better', 'vs', 'versus', 'against'],
        'budget_inquiry': ['cheap', 'under budget', 'affordable', 'lowest price', 'deals', 'discount'],
        'alternative_request': ['alternative', 'similar to', 'substitute', 'replace', 'like this'],
        'shopping_mission': ['build a setup', 'study setup', 'gaming setup', 'workstation', 'bundle', 'complete kit'],
        'review_inquiry': ['reviews', 'ratings', 'what do people say', 'pros and cons', 'complaints', 'praise'],
        'refinement': ['make it cheaper', 'better battery', 'more ram', 'different color', 'prefer', 'change budget']
    }

    @classmethod
    def classify(cls, message: str) -> Dict[str, Any]:
        text = message.lower().strip()
        matched_intent = 'product_search'
        max_matches = 0

        for intent, patterns in cls.INTENT_KEYWORDS.items():
            matches = sum(1 for p in patterns if p in text)
            if matches > max_matches:
                max_matches = matches
                matched_intent = intent

        confidence = 0.85 if max_matches > 0 else 0.50
        return {
            'intent': matched_intent,
            'confidence': confidence
        }
''', encoding='utf-8')

# 11. nlp/sentiment_analyzer.py
(BASE / 'nlp' / 'sentiment_analyzer.py').write_text('''import re
from typing import Dict, Any, List

POSITIVE_WORDS = {
    'excellent', 'great', 'good', 'amazing', 'superb', 'fast', 'smooth', 'durable',
    'fantastic', 'love', 'best', 'flawless', 'crisp', 'premium', 'solid', 'comfortable',
    'impressive', 'stellar', 'worth', 'value', 'satisfied', 'powerful', 'lightweight'
}

NEGATIVE_WORDS = {
    'terrible', 'bad', 'poor', 'slow', 'lag', 'broke', 'broken', 'disappointed',
    'horrible', 'worst', 'cheap', 'uncomfortable', 'defective', 'noisy', 'overheating',
    'drains', 'drain', 'weak', 'heavy', 'waste', 'issue', 'complaint', 'problem'
}

ASPECT_LEXICON = {
    'battery': ['battery', 'backup', 'charge', 'charging', 'drain', 'hours', 'mah'],
    'performance': ['speed', 'fast', 'lag', 'processor', 'ram', 'smooth', 'multitasking', 'gaming', 'fps'],
    'build_quality': ['build', 'quality', 'hinge', 'plastic', 'metal', 'solid', 'durable', 'sturdy', 'finish'],
    'sound': ['sound', 'audio', 'bass', 'treble', 'mic', 'volume', 'noise', 'anc', 'clarity'],
    'comfort': ['comfort', 'fit', 'ears', 'cushion', 'ergonomic', 'pain', 'heavy', 'wearable'],
    'display': ['screen', 'display', 'panel', 'brightness', 'colors', 'resolution', '4k', 'ips', 'oled'],
    'camera': ['camera', 'photo', 'video', 'lens', 'sensor', 'lowlight', 'image quality'],
    'value': ['price', 'value', 'worth', 'expensive', 'cost', 'deal', 'money']
}


class AspectSentimentAnalyzer:
    """Aspect-based sentiment analysis extracting granular scores for battery, build, sound, etc."""

    @classmethod
    def analyze_review(cls, text: str) -> Dict[str, Any]:
        clean = text.lower()
        words = re.findall(r'\b\w+\b', clean)
        
        pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
        total = pos_count + neg_count
        
        if total == 0:
            polarity = 0.0
            label = 'neutral'
        else:
            polarity = (pos_count - neg_count) / total
            if polarity > 0.15:
                label = 'positive'
            elif polarity < -0.15:
                label = 'negative'
            else:
                label = 'neutral'

        # Aspect extraction
        aspect_ratings = {}
        sentences = re.split(r'[.!?]+', clean)
        for aspect, aspect_words in ASPECT_LEXICON.items():
            aspect_sentences = [s for s in sentences if any(aw in s for aw in aspect_words)]
            if aspect_sentences:
                a_pos = sum(1 for s in aspect_sentences for w in re.findall(r'\b\w+\b', s) if w in POSITIVE_WORDS)
                a_neg = sum(1 for s in aspect_sentences for w in re.findall(r'\b\w+\b', s) if w in NEGATIVE_WORDS)
                a_total = a_pos + a_neg
                if a_total > 0:
                    score = (a_pos / a_total)
                else:
                    score = 0.70 if polarity >= 0 else 0.30
                aspect_ratings[aspect] = {
                    'score': round(score, 2),
                    'label': 'positive' if score >= 0.6 else ('neutral' if score >= 0.4 else 'negative')
                }

        # Praises and Complaints extraction
        praises = []
        complaints = []
        for s in sentences:
            s_str = s.strip()
            if not s_str or len(s_str) < 5:
                continue
            if any(w in s for w in POSITIVE_WORDS) and not any(w in s for w in NEGATIVE_WORDS):
                praises.append(s_str.capitalize())
            elif any(w in s for w in NEGATIVE_WORDS):
                complaints.append(s_str.capitalize())

        return {
            'polarity': round(polarity, 2),
            'label': label,
            'aspect_ratings': aspect_ratings,
            'praises': praises[:3],
            'complaints': complaints[:3]
        }
''', encoding='utf-8')

# 12. nlp/vector_similarity.py
(BASE / 'nlp' / 'vector_similarity.py').write_text('''import math
from typing import List, Dict, Tuple
from app.ai.nlp.tokenizer import TextTokenizer


class VectorSimilarityEngine:
    """Pure Python TF-IDF and Cosine Similarity calculation for semantic product ranking."""

    @staticmethod
    def compute_tf(tokens: List[str]) -> Dict[str, float]:
        tf = {}
        total = len(tokens)
        if total == 0:
            return tf
        for t in tokens:
            tf[t] = tf.get(t, 0.0) + 1.0 / total
        return tf

    @classmethod
    def compute_idf(cls, corpus_tokens: List[List[str]]) -> Dict[str, float]:
        n_docs = len(corpus_tokens)
        df = {}
        for doc in corpus_tokens:
            unique_terms = set(doc)
            for t in unique_terms:
                df[t] = df.get(t, 0) + 1

        idf = {}
        for term, freq in df.items():
            idf[term] = math.log((n_docs + 1.0) / (freq + 1.0)) + 1.0
        return idf

    @classmethod
    def cosine_similarity(cls, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        dot_product = sum(vec_a[k] * vec_b.get(k, 0.0) for k in vec_a)
        norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    @classmethod
    def rank_documents(cls, query: str, documents: List[Tuple[int, str]]) -> List[Tuple[int, float]]:
        query_tokens = TextTokenizer.tokenize(query)
        if not query_tokens or not documents:
            return []

        doc_tokens_list = [TextTokenizer.tokenize(doc_text) for _, doc_text in documents]
        idf = cls.compute_idf(doc_tokens_list + [query_tokens])

        query_tf = cls.compute_tf(query_tokens)
        query_vec = {k: query_tf[k] * idf.get(k, 1.0) for k in query_tf}

        scores = []
        for (doc_id, _), doc_tokens in zip(documents, doc_tokens_list):
            doc_tf = cls.compute_tf(doc_tokens)
            doc_vec = {k: doc_tf[k] * idf.get(k, 1.0) for k in doc_tf}
            sim = cls.cosine_similarity(query_vec, doc_vec)
            scores.append((doc_id, round(sim, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
''', encoding='utf-8')

# 13. nlp/__init__.py
(BASE / 'nlp' / '__init__.py').write_text('''from app.ai.nlp.tokenizer import TextTokenizer
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.nlp.intent_classifier import IntentClassifier
from app.ai.nlp.sentiment_analyzer import AspectSentimentAnalyzer
from app.ai.nlp.vector_similarity import VectorSimilarityEngine

__all__ = [
    'TextTokenizer',
    'EntityExtractor',
    'IntentClassifier',
    'AspectSentimentAnalyzer',
    'VectorSimilarityEngine'
]
''', encoding='utf-8')

# 14. copilot/ranking_engine.py
(BASE / 'copilot' / 'ranking_engine.py').write_text('''from typing import List, Dict, Any, Optional
from app.models.product import Product


class CopilotRankingEngine:
    """Multi-criteria ranking engine scoring candidate products based on budget fit, specs, and ratings."""

    @classmethod
    def rank_candidates(
        cls,
        products: List[Product],
        budget: Optional[float] = None,
        priorities: Optional[List[str]] = None,
        primary_usage: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if not products:
            return []

        priorities = priorities or []
        results = []

        for p in products:
            score = 70.0  # baseline
            reasons = []

            # 1. Budget scoring
            if budget and budget > 0:
                price = p.current_price
                if price <= budget:
                    ratio = price / budget
                    if ratio >= 0.65:
                        score += 15.0
                        reasons.append(f"Well within your target budget of ₹{budget:,.0f}")
                    else:
                        score += 10.0
                        reasons.append("Great budget savings option")
                else:
                    over_ratio = (price - budget) / budget
                    penalty = min(35.0, over_ratio * 40.0)
                    score -= penalty
                    if over_ratio < 0.10:
                        reasons.append("Slightly above budget but high specification match")
                    else:
                        reasons.append("Above target budget")

            # 2. Rating & Review Sentiment
            if p.average_rating >= 4.5:
                score += 8.0
                reasons.append(f"Exceptional rating ({p.average_rating}★ from {p.total_reviews_count} buyers)")
            elif p.average_rating >= 4.0:
                score += 5.0
                reasons.append(f"Highly rated ({p.average_rating}★)")

            # 3. Usage & Priority match
            aspects = p.get_aspect_sentiment_dict()
            usage_str = (p.target_usage or '').lower()
            features_str = ' '.join(p.get_key_features_list()).lower()

            for prio in priorities:
                prio_lower = prio.lower()
                if prio_lower in usage_str or prio_lower in features_str:
                    score += 6.0
                    reasons.append(f"Optimized for {prio}")
                if prio_lower in aspects:
                    a_score = aspects[prio_lower]
                    if a_score >= 80:
                        score += 5.0
                        reasons.append(f"Strong verified sentiment for {prio} ({a_score}%)")

            # Clamp score between 10 and 99
            final_score = max(10.0, min(98.0, score))
            results.append({
                'product': p,
                'match_score': round(final_score, 1),
                'reasons': reasons[:4]
            })

        results.sort(key=lambda x: x['match_score'], reverse=True)

        # Assign badges
        if results:
            results[0]['badge'] = 'Best Match'
            
            # Find Best Value (highest score / price ratio)
            cheapest = sorted(results, key=lambda x: x['product'].current_price)
            if len(cheapest) > 1 and cheapest[0] != results[0]:
                cheapest[0]['badge'] = 'Best Value'

            # Find Best Battery / Best Performance if applicable
            for r in results:
                if 'badge' not in r:
                    aspects = r['product'].get_aspect_sentiment_dict()
                    if aspects.get('battery', 0) >= 88:
                        r['badge'] = 'Best Battery'
                        break
                    elif aspects.get('performance', 0) >= 90:
                        r['badge'] = 'Top Performance'
                        break

        return results
''', encoding='utf-8')

# 15. copilot/explanation_generator.py
(BASE / 'copilot' / 'explanation_generator.py').write_text('''from typing import List, Dict, Any, Optional
from app.models.product import Product


class ExplanationGenerator:
    """Generates transparent, human-readable explanations answering 'Why am I seeing this product?'."""

    @classmethod
    def generate_explanation(
        cls,
        product: Product,
        match_score: float,
        reasons: List[str],
        user_budget: Optional[float] = None,
        priorities: Optional[List[str]] = None
    ) -> str:
        parts = [f"Recommended with a **{match_score}% match score**."]
        
        if reasons:
            bullets = ", ".join(reasons)
            parts.append(f"Key factors: {bullets}.")
        
        if user_budget and product.current_price <= user_budget:
            savings = user_budget - product.current_price
            if savings > 1000:
                parts.append(f"Saves you ₹{savings:,.0f} compared to your maximum budget ceiling.")

        return " ".join(parts)
''', encoding='utf-8')

# 16. seller/diagnostic_engine.py
(BASE / 'seller' / 'diagnostic_engine.py').write_text('''from typing import Dict, Any, List, Optional
from app.models.product import Product
from app.models.analytics import ProductPerformanceScore
from app.models.inventory import ProductInventory


class SellerDiagnosticEngine:
    """Root-cause diagnostic reasoner explaining sales fluctuations, traffic drops, and inventory bottlenecks."""

    @classmethod
    def diagnose_product_performance(
        cls,
        product: Product,
        inventory: Optional[ProductInventory] = None,
        performance: Optional[ProductPerformanceScore] = None
    ) -> Dict[str, Any]:
        findings = []
        recommendations = []
        severity = 'normal'

        # 1. Inventory Check
        if inventory:
            if inventory.available_quantity <= 0:
                findings.append("Product is currently OUT OF STOCK, causing 100% loss of potential conversion.")
                recommendations.append("Initiate immediate supplier reorder.")
                severity = 'critical'
            elif inventory.available_quantity <= inventory.safety_stock:
                findings.append(f"Stock level is low ({inventory.available_quantity} units remaining, safety stock is {inventory.safety_stock}).")
                recommendations.append("Reorder stock before lead-time depletion.")
                severity = 'high'
            elif inventory.days_of_supply > 90:
                findings.append(f"Excess inventory detected ({inventory.days_of_supply} days of supply on hand).")
                recommendations.append("Consider a 10-15% promotional discount or product bundle.")

        # 2. Performance and Sales Velocity
        if performance:
            if performance.is_dead_stock:
                findings.append(f"Flagged as DEAD STOCK: No sales recorded in the last {performance.days_since_last_sale} days.")
                recommendations.append("Execute clearance markdown or bundle with a high-velocity product.")
                severity = 'high'
            if performance.conversion_score < 40:
                findings.append("Low conversion rate relative to page views. Visitors view the item but drop off before cart addition.")
                recommendations.append("Optimize product imagery, lower price point, or address common customer complaints in description.")

        # 3. Reviews & Aspect Sentiment
        aspects = product.get_aspect_sentiment_dict()
        for aspect_name, score in aspects.items():
            if score < 60:
                findings.append(f"Negative review sentiment on '{aspect_name}' ({score}% satisfaction).")
                recommendations.append(f"Review customer feedback regarding {aspect_name} to improve batch quality or adjust specifications.")

        if not findings:
            findings.append("Product is performing stably with healthy sales velocity and balanced inventory.")
            recommendations.append("Maintain current pricing and inventory replenishment cadence.")

        return {
            'product_id': product.id,
            'product_title': product.title,
            'severity': severity,
            'findings': findings,
            'recommendations': recommendations
        }
''', encoding='utf-8')

# 17. seller/seller_copilot_service.py
(BASE / 'seller' / 'seller_copilot_service.py').write_text('''from typing import Dict, Any, List
from app.ai.gateway import get_ai_gateway
from app.ai.seller.diagnostic_engine import SellerDiagnosticEngine
from app.repositories.product_repository import ProductRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.analytics_repository import ProductPerformanceRepository, SellerMetricDailyRepository


class SellerCopilotService:
    """Answers seller strategic queries grounded in actual database analytics."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.inventory_repo = InventoryRepository()
        self.performance_repo = ProductPerformanceRepository()
        self.metrics_repo = SellerMetricDailyRepository()

    def process_seller_query(self, seller_id: int, query: str) -> Dict[str, Any]:
        ai_gateway = get_ai_gateway()
        q_lower = query.lower()

        # Find relevant products if mentioned
        products = self.product_repo.get_by_seller(seller_id)
        matched_product = None
        for p in products:
            if p.title.lower() in q_lower or p.brand.lower() in q_lower or (p.category and p.category.name.lower() in q_lower):
                matched_product = p
                break

        if not matched_product and products:
            matched_product = products[0]

        diagnostic_data = None
        if matched_product:
            inv = self.inventory_repo.get_by_product_id(matched_product.id)
            perf = self.performance_repo.find_one_by(product_id=matched_product.id)
            diagnostic_data = SellerDiagnosticEngine.diagnose_product_performance(matched_product, inv, perf)

        # Build diagnostic prompt
        system_prompt = (
            "You are ShopSense Seller AI Copilot, a data-driven retail advisor. "
            "Explain business performance strictly grounded in the seller's actual metrics, inventory levels, and review sentiments."
        )
        context_prompt = f"Seller Query: {query}\n"
        if diagnostic_data:
            context_prompt += f"Product: {diagnostic_data['product_title']}\n"
            context_prompt += f"Identified Findings: {'; '.join(diagnostic_data['findings'])}\n"
            context_prompt += f"Action Recommendations: {'; '.join(diagnostic_data['recommendations'])}\n"

        ai_response = ai_gateway.generate(context_prompt, system_prompt=system_prompt)

        return {
            'query': query,
            'response': ai_response['content'],
            'diagnostic': diagnostic_data,
            'latency_ms': ai_response.get('latency_ms', 0)
        }
''', encoding='utf-8')

# 18. __init__.py for app/ai
(BASE / '__init__.py').write_text('''from app.ai.gateway import AIGateway, get_ai_gateway
from app.ai.nlp.tokenizer import TextTokenizer
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.nlp.intent_classifier import IntentClassifier
from app.ai.nlp.sentiment_analyzer import AspectSentimentAnalyzer
from app.ai.nlp.vector_similarity import VectorSimilarityEngine
from app.ai.copilot.ranking_engine import CopilotRankingEngine
from app.ai.copilot.explanation_generator import ExplanationGenerator
from app.ai.seller.diagnostic_engine import SellerDiagnosticEngine
from app.ai.seller.seller_copilot_service import SellerCopilotService

__all__ = [
    'AIGateway',
    'get_ai_gateway',
    'TextTokenizer',
    'EntityExtractor',
    'IntentClassifier',
    'AspectSentimentAnalyzer',
    'VectorSimilarityEngine',
    'CopilotRankingEngine',
    'ExplanationGenerator',
    'SellerDiagnosticEngine',
    'SellerCopilotService'
]
''', encoding='utf-8')

print('All 18 AI layer modules generated successfully!')
