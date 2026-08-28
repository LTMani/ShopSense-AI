from typing import Dict, Any


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
