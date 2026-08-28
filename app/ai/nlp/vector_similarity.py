import math
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
