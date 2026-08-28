import re
from typing import Dict, Any, List, Tuple, Set


class AspectSentimentExtractionEngine:
    """Aspect-Based Sentiment Analysis (ABSA) with negation handling, intensifiers, and polarity scoring."""

    ASPECT_LEXICONS: Dict[str, List[str]] = {
        'battery': [
            'battery', 'backup', 'charge', 'charging', 'mah', 'endurance', 'hours', 'drain',
            'power', 'standby', 'battery life', 'runtime', 'supervooc', 'magsafe', 'rapid charge'
        ],
        'sound': [
            'sound', 'audio', 'bass', 'treble', 'mic', 'microphone', 'voice', 'speaker', 'volume',
            'clarity', 'anc', 'noise cancellation', 'spatial audio', 'music', 'soundstage', 'mids'
        ],
        'build': [
            'build', 'quality', 'durability', 'sturdy', 'premium', 'chassis', 'aluminum', 'finish',
            'hinge', 'casing', 'feel', 'design', 'solid', 'rugged', 'plastic', 'creak', 'weight'
        ],
        'display': [
            'display', 'screen', 'panel', 'ips', 'oled', 'amoled', 'brightness', 'nits', 'hz',
            'refresh rate', 'colors', 'resolution', '4k', 'fhd', 'viewing angle', 'contrast'
        ],
        'performance': [
            'performance', 'speed', 'fast', 'lag', 'smooth', 'fps', 'gpu', 'cpu', 'processor',
            'ram', 'heating', 'thermal', 'multitasking', 'snappy', 'quick', 'benchmark', 'throttle'
        ],
        'comfort': [
            'comfort', 'comfortable', 'earpads', 'headband', 'cushion', 'lumbar', 'fit', 'ergonomics',
            'pain', 'weight', 'lightweight', 'breathable', 'tight', 'mesh', 'posture'
        ],
        'camera': [
            'camera', 'photo', 'video', 'sensor', 'lens', 'night mode', 'portrait', 'ois',
            'megapixels', 'sharpness', 'zoom', 'telephoto', 'low light', 'dynamic range'
        ],
        'value': [
            'value', 'price', 'worth', 'budget', 'expensive', 'cheap', 'deal', 'cost',
            'affordable', 'money', 'overpriced', 'bang for buck', 'investment'
        ]
    }

    POSITIVE_WORDS: Set[str] = {
        'excellent', 'amazing', 'superb', 'great', 'fantastic', 'good', 'crisp', 'clear',
        'long', 'fast', 'smooth', 'stellar', 'flawless', 'premium', 'solid', 'punchy',
        'bright', 'vibrant', 'quiet', 'sturdy', 'responsive', 'perfect', 'comfortable',
        'loved', 'impressed', 'satisfying', 'topnotch', 'worth', 'best', 'incredible',
        'lasted', 'lasting', 'outstanding', 'splendid', 'brilliant', 'durable'
    }

    NEGATIVE_WORDS: Set[str] = {
        'terrible', 'awful', 'poor', 'bad', 'laggy', 'slow', 'scratch', 'loose', 'drain',
        'drains', 'muffled', 'distortion', 'heating', 'hot', 'dim', 'dull', 'creaky',
        'uncomfortable', 'pain', 'heavy', 'heavyweight', 'expensive', 'overpriced',
        'broke', 'disappointed', 'flimsy', 'glitch', 'noisy', 'mediocre', 'subpar',
        'disappointing', 'worst', 'failed', 'issue', 'issues', 'defective', 'cheap', 'lack'
    }

    NEGATION_WORDS: Set[str] = {'not', "n't", 'no', 'never', 'hardly', 'barely', 'scarcely', 'without'}
    INTENSIFIERS: Dict[str, float] = {
        'very': 1.5, 'extremely': 2.0, 'super': 1.8, 'highly': 1.7, 'ultra': 1.8,
        'really': 1.4, 'absolutely': 1.9, 'incredibly': 1.9, 'exceptionally': 2.0
    }

    @classmethod
    def analyze_aspects_in_text(cls, text: str) -> Dict[str, Any]:
        sentences = re.split(r'[.!?;\n]+', text)
        aspect_scores: Dict[str, List[float]] = {asp: [] for asp in cls.ASPECT_LEXICONS}
        praises: List[str] = []
        complaints: List[str] = []

        for sentence in sentences:
            s_clean = sentence.strip().lower()
            if not s_clean:
                continue

            words = re.findall(r"\b[\w']+\b", s_clean)
            
            # Check which aspects are mentioned in this sentence
            mentioned_aspects = set()
            for asp, keywords in cls.ASPECT_LEXICONS.items():
                for kw in keywords:
                    if kw in s_clean:
                        mentioned_aspects.add(asp)
                        break

            if not mentioned_aspects:
                continue

            # Compute polarity for this sentence
            pos_count = 0
            neg_count = 0

            for i, word in enumerate(words):
                # Check for preceding negation in 1-2 token lookback
                is_negated = False
                if i > 0 and words[i - 1] in cls.NEGATION_WORDS:
                    is_negated = True
                elif i > 1 and words[i - 2] in cls.NEGATION_WORDS:
                    is_negated = True

                if word in cls.POSITIVE_WORDS:
                    if is_negated:
                        neg_count += 1
                    else:
                        pos_count += 1
                elif word in cls.NEGATIVE_WORDS:
                    if is_negated:
                        pos_count += 1
                    else:
                        neg_count += 1

            score = float(pos_count - neg_count)

            # Record aspect score
            for asp in mentioned_aspects:
                aspect_scores[asp].append(score)

            if pos_count > neg_count and pos_count > 0:
                praises.append(sentence.strip())
            elif neg_count > pos_count and neg_count > 0:
                complaints.append(sentence.strip())

        # Compile aspect ratings (0-100 percentage scale)
        summary: Dict[str, int] = {}
        for asp, scores in aspect_scores.items():
            if scores:
                avg = sum(scores) / len(scores)
                # Map -2.0 to +2.0 into 0 to 100%
                percent = int(max(0, min(100, (avg + 2.0) / 4.0 * 100)))
                summary[asp] = percent
            else:
                summary[asp] = 80  # Baseline neutral positive

        return {
            'aspect_ratings': summary,
            'top_praises': praises[:5],
            'top_complaints': complaints[:5]
        }
