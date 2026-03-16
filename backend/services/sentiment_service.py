"""
Aggregate sentiment analytics: counts, average rating, total reviews, top keywords.

This module is kept for backwards compatibility with the existing /analytics
endpoint. Newer analytics (product comparison, trends, insights) live in
analytics_service.py and reuse the helpers defined here and in keyword_service.
"""
from services.keyword_service import extract_keywords

def analyze_sentiments(reviews):
    """Compute sentiment_count, average_rating, total_reviews, top_keywords."""
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    total_rating = 0

    for review in reviews:
        sentiment_count[review.get("sentiment", "neutral")] += 1
        total_rating += review.get("rating", 0)

    total = len(reviews)
    avg_rating = round(total_rating / total, 2) if total else 0.0
    texts = [
        (r.get("review_text") or r.get("review") or "")
        for r in reviews
    ]
    top_keywords = extract_keywords(texts, top_n=10)

    return {
        "sentiment_count": sentiment_count,
        "average_rating": avg_rating,
        "total_reviews": total,
        "top_keywords": top_keywords,
    }
