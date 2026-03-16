"""
Higher-level analytics for the sentiment dashboard.

Includes:
- overall_analytics: wraps existing sentiment_service for /analytics
- product_analytics: per-product sentiment and rating stats
- trend_analytics: sentiment counts per day
"""
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

from services.sentiment_service import analyze_sentiments


DATE_FMT = "%Y-%m-%d"


def _ensure_date(review: Dict[str, Any]) -> str:
    """
    Ensure a review has a date string (YYYY-MM-DD).
    If missing, derive from `created_at` or default to today's date.
    """
    if "date" in review and review["date"]:
        return str(review["date"])[:10]
    created = review.get("created_at")
    if created:
        # try to parse, then normalize to date component
        try:
            dt = datetime.fromisoformat(str(created))
            return dt.strftime(DATE_FMT)
        except ValueError:
            pass
    # fallback: today
    return datetime.utcnow().strftime(DATE_FMT)


def overall_analytics(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Keep existing overall analytics behavior."""
    return analyze_sentiments(reviews)


def product_analytics(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build per-product sentiment counts and average rating.
    Output format is suitable for GET /analytics/products.
    """
    by_product: Dict[str, Dict[str, Any]] = {}
    for r in reviews:
        product = (r.get("product") or "").strip() or "Unknown"
        entry = by_product.setdefault(
            product,
            {
                "product": product,
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "average_rating": 0.0,
                "_rating_sum": 0,
                "_count": 0,
            },
        )
        sentiment = (r.get("sentiment") or "neutral").lower()
        if sentiment not in ("positive", "neutral", "negative"):
            sentiment = "neutral"
        entry[sentiment] += 1
        rating = r.get("rating")
        if isinstance(rating, (int, float)):
            entry["_rating_sum"] += rating
        entry["_count"] += 1

    results: List[Dict[str, Any]] = []
    for product, data in by_product.items():
        count = data.pop("_count")
        rating_sum = data.pop("_rating_sum")
        data["average_rating"] = round(rating_sum / count, 2) if count else 0.0
        results.append(data)
    # optionally sort by product name
    results.sort(key=lambda d: d["product"].lower())
    return results


def trend_analytics(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build sentiment trend over time (by date).
    Output format is suitable for GET /analytics/trends.
    """
    buckets: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"positive": 0, "neutral": 0, "negative": 0}
    )
    for r in reviews:
        date_key = _ensure_date(r)
        sentiment = (r.get("sentiment") or "neutral").lower()
        if sentiment not in ("positive", "neutral", "negative"):
            sentiment = "neutral"
        buckets[date_key][sentiment] += 1

    # sort dates ascending
    dates = sorted(buckets.keys())
    positive = [buckets[d]["positive"] for d in dates]
    neutral = [buckets[d]["neutral"] for d in dates]
    negative = [buckets[d]["negative"] for d in dates]

    return {
        "dates": dates,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }

