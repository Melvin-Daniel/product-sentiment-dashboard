"""
Insights service: AI-style summary and fake review scoring using simple heuristics.
"""
from typing import List, Dict, Any

from services.keyword_service import extract_keywords


def build_summary(reviews: List[Dict[str, Any]]) -> str:
    """
    Generate a short natural-language insight summary using sentiment counts
    and top keywords.
    """
    if not reviews:
        return "There are no reviews yet. Add some reviews to see insights."

    positive = sum(1 for r in reviews if (r.get("sentiment") or "").lower() == "positive")
    neutral = sum(1 for r in reviews if (r.get("sentiment") or "").lower() == "neutral")
    negative = sum(1 for r in reviews if (r.get("sentiment") or "").lower() == "negative")
    total = len(reviews)

    texts = [
        (r.get("review_text") or r.get("review") or "")
        for r in reviews
    ]
    keywords = extract_keywords(texts, top_n=5)
    important_words = [k["word"] for k in keywords][:3]

    lines = []
    # Sentiment distribution sentence
    if positive >= negative and positive >= neutral:
        lines.append("Customers are mostly positive overall.")
    elif negative > positive and negative >= neutral:
        lines.append("A noticeable portion of customers share negative feedback.")
    else:
        lines.append("Customer sentiment is mixed, with many neutral reviews.")

    # Keyword-based sentence
    if important_words:
        joined = ", ".join(important_words[:-1]) + (" and " + important_words[-1] if len(important_words) > 1 else important_words[0])
        lines.append(f"Reviews frequently mention {joined}.")

    # Mention negatives if any
    if negative and positive:
        lines.append("While many appreciate the products, some reviews point out drawbacks that may need attention.")
    elif negative and not positive:
        lines.append("Most comments highlight issues rather than strengths.")

    # Fallback
    if not lines:
        return "Reviews are available, but there is no clear dominant sentiment yet."

    return " ".join(lines)


def score_fake_probability(review_text: str) -> float:
    """
    Simple heuristic fake-review score in [0, 1].
    - excessive punctuation
    - very short reviews
    - repeated words
    """
    if not review_text:
        return 0.0
    text = str(review_text)
    length = len(text)
    words = [w.lower() for w in text.split() if w]
    unique_words = set(words)

    score = 0.0

    # Very short generic review
    if length < 20 or len(words) < 4:
        score += 0.3

    # Excessive punctuation / exclamation
    exclamations = text.count("!")
    if exclamations >= 3:
        score += 0.3
    elif exclamations == 2:
        score += 0.2

    # Repeated words ratio
    if words:
        repetition_ratio = 1.0 - (len(unique_words) / float(len(words)))
        if repetition_ratio > 0.4:
            score += 0.3
        elif repetition_ratio > 0.25:
            score += 0.15

    # clamp to [0,1]
    if score > 1.0:
        score = 1.0
    return round(score, 2)

