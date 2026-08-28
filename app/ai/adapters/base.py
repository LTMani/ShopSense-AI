from abc import ABC, abstractmethod
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
