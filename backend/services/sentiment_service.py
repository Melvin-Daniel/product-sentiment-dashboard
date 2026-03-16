"""
Aggregate sentiment analytics: counts, average rating, total reviews, top keywords.
"""
import re
from collections import Counter

# Simple English stopwords for keyword extraction
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "is", "it", "this", "that", "are", "was", "were",
    "been", "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "can", "i", "you", "he", "she",
    "we", "they", "my", "your", "very", "not", "no", "just", "so", "as", "if",
}

def _tokenize(text):
    """Lowercase and extract words (letters only)."""
    if not text:
        return []
    lowered = (text or "").lower()
    words = re.findall(r"[a-z]+", lowered)
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]

def analyze_sentiments(reviews):
    """Compute sentiment_count, average_rating, total_reviews, top_keywords."""
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    total_rating = 0
    all_words = []

    for review in reviews:
        sentiment_count[review.get("sentiment", "neutral")] += 1
        total_rating += review.get("rating", 0)
        text = review.get("review_text") or review.get("review") or ""
        all_words.extend(_tokenize(text))

    total = len(reviews)
    avg_rating = round(total_rating / total, 2) if total else 0.0
    keyword_counts = Counter(all_words)
    top_keywords = [{"word": w, "count": c} for w, c in keyword_counts.most_common(10)]

    return {
        "sentiment_count": sentiment_count,
        "average_rating": avg_rating,
        "total_reviews": total,
        "top_keywords": top_keywords,
    }
