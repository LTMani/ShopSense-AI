import re
from typing import Dict, Any, Optional, List


class EntityExtractor:
    """Extracts budgets, categories, brands, screen sizes, RAM, and storage from shopping queries."""

    CATEGORY_SYNONYMS = {
        'Laptops & Computers': ['laptop', 'notebook', 'macbook', 'ultrabook', 'thinkpad', 'gaming laptop', 'chromebook'],
        'Smartphones & Tablets': ['phone', 'smartphone', 'mobile', 'iphone', 'galaxy', 'handset', 'android', 'tablet', 'ipad'],
        'Audio & Headphones': ['headphone', 'headphones', 'earphone', 'earbuds', 'speaker', 'soundbar', 'tws', 'anc'],
        'Cameras & Photography': ['camera', 'dslr', 'mirrorless', 'action cam', 'lens', 'camcorder', 'gopro'],
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
            r'(?:under|below|budget|within|around|less than|max|upto|up to|price|for)\s*(?:rs\.?|₹|inr|\$)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand|lakh)?',
            r'(?:rs\.?|₹|inr|\$)\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand|lakh)?',
            r'\b(\d+(?:,\d+)*)\s*(?:rs|inr|rupees|k|thousand|lakh)\b'
        ]
        for pat in patterns:
            match = re.search(pat, text)
            if match:
                raw = match.group(1).replace(',', '')
                try:
                    val = float(raw)
                    suffix = match.group(2) if len(match.groups()) > 1 and match.group(2) else ''
                    if not suffix and ('k' in text[match.start():match.end()+4]):
                        suffix = 'k'
                    elif not suffix and ('lakh' in text[match.start():match.end()+6]):
                        suffix = 'lakh'

                    if suffix == 'k' or suffix == 'thousand':
                        val *= 1000
                    elif suffix == 'lakh':
                        val *= 100000

                    if 100 <= val <= 10000000:
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

        storage_match = re.search(r'(\d+)\s*(?:gb|tb)\s*(?:ssd|storage|rom|hdd)|(?:ssd\s*(\d+)\s*(?:gb|tb))|(\d+)\s*tb', text)
        if storage_match:
            specs['storage'] = storage_match.group(0)

        screen_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|\"|\-inch)', text)
        if screen_match:
            specs['screen_size'] = float(screen_match.group(1))

        return specs
