import pytest
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.nlp.intent_classifier import IntentClassifier
from app.ai.nlp.sentiment_analyzer import AspectSentimentAnalyzer
from app.ai.nlp.vector_similarity import VectorSimilarityEngine
from app.ai.nlp.tokenizer import TextTokenizer


class TestNLPExtendedMatrix:
    """Comprehensive test matrix validating NLP entity extraction, intent classification, and vector ranking."""

    def test_budget_extraction_formats(self):
        cases = [
            ("laptop under 60000", 60000.0),
            ("phone below Rs. 25,000", 25000.0),
            ("headphones for ₹5,000", 5000.0),
            ("gaming pc budget 1.5 lakh", 150000.0),
            ("mechanical keyboard under 8k", 8000.0),
            ("study table around 12000 rupees", 12000.0),
            ("ultrabook max price 90000 inr", 90000.0),
            ("wireless earbuds within 3500", 3500.0)
        ]
        for query, expected_budget in cases:
            res = EntityExtractor.extract_entities(query)
            assert res['budget'] == expected_budget, f"Failed on query: {query}"

    def test_category_and_brand_extraction(self):
        cases = [
            ("Apple MacBook Air M2 for college", "Laptops & Computers", "Apple"),
            ("Sony wireless noise cancelling headphones", "Audio & Headphones", "Sony"),
            ("Samsung 27 inch gaming monitor 144hz", "Monitors & Displays", "Samsung"),
            ("Logitech ergonomic mouse for coding", "Computer Peripherals", "Logitech"),
            ("ErgoSmart high back desk chair", "Office & Study Furniture", None),
            ("PlayStation 5 console with controller", "Gaming & Consoles", None),
            ("GoPro action camera 4k 60fps", "Cameras & Photography", "GoPro")
        ]
        for query, expected_cat, expected_brand in cases:
            res = EntityExtractor.extract_entities(query)
            if expected_cat:
                assert res['category'] == expected_cat, f"Category mismatch on: {query}"
            if expected_brand:
                assert res['brand'] == expected_brand, f"Brand mismatch on: {query}"

    def test_hardware_specs_extraction(self):
        res1 = EntityExtractor.extract_entities("Laptop with 16GB RAM and 512GB SSD")
        assert res1['specs'].get('ram_gb') == 16
        assert '512gb' in str(res1['specs'].get('storage', '')).lower()

        res2 = EntityExtractor.extract_entities("27 inch 4K monitor")
        assert res2['specs'].get('screen_size') == 27.0

    def test_target_usage_intent_detection(self):
        usages_cases = [
            ("laptop for python coding and software development", "coding"),
            ("monitor for competitive fps gaming with high hz", "gaming"),
            ("travel friendly lightweight slim laptop for flights", "portability"),
            ("audiophile headphones with hi-res lossless sound and deep bass", "audiophile")
        ]
        for text, expected_use in usages_cases:
            res = EntityExtractor.extract_entities(text)
            assert expected_use in res['usage'], f"Usage '{expected_use}' not detected in '{text}'"

    def test_vector_similarity_cosine_ranking(self):
        docs = [
            (1, "Lenovo ThinkPad E14 AMD Ryzen 7 16GB RAM 512GB SSD coding laptop"),
            (2, "Sony WH-1000XM5 wireless noise cancelling headphones audio anc"),
            (3, "LG UltraGear 27 inch 144Hz IPS gaming monitor display"),
            (4, "ErgoSmart mesh high back desk chair lumbar ergonomics office")
        ]

        # Query 1: should rank ThinkPad at #1
        ranked_laptops = VectorSimilarityEngine.rank_documents("lightweight coding laptop with 16GB RAM", docs)
        assert ranked_laptops[0][0] == 1

        # Query 2: should rank Sony headphones at #1
        ranked_audio = VectorSimilarityEngine.rank_documents("noise cancelling ANC headphones for music", docs)
        assert ranked_audio[0][0] == 2

        # Query 3: should rank LG monitor at #1
        ranked_display = VectorSimilarityEngine.rank_documents("144hz gaming monitor screen", docs)
        assert ranked_display[0][0] == 3

    def test_tokenizer_and_stopwords(self):
        raw = "The MacBook Air is an amazingly fast and lightweight laptop!"
        tokens = TextTokenizer.tokenize(raw, remove_stopwords=True)
        assert 'the' not in tokens
        assert 'is' not in tokens
        assert 'an' not in tokens
        assert 'macbook' in tokens
        assert 'laptop' in tokens
