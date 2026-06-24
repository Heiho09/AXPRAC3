import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_index(records):
    questions = [r["question"] for r in records]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3), min_df=1)
    matrix = vectorizer.fit_transform(questions)
    return vectorizer, matrix


def search(query, records, vectorizer, matrix, top_n=5, min_score=0.1):
    if not query.strip():
        return []

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_indices = np.argsort(scores)[::-1][:top_n]

    results = []
    for idx in top_indices:
        if scores[idx] >= min_score:
            result = records[idx].copy()
            result["score"] = float(scores[idx])
            results.append(result)

    return results
