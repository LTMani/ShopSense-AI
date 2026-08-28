import re
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
