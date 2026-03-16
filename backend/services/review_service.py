"""
Review CRUD and filtering. All review records use review_text (and optionally product).
"""
from datetime import datetime
from services.db_service import get_reviews_from_db, save_reviews_to_db
from services.vader_service import analyze_text
from services.insights_service import score_fake_probability

def _normalize_review(r):
    """Ensure each review has review_text (support legacy 'review' key)."""
    out = dict(r)
    if "review" in out and "review_text" not in out:
        out["review_text"] = out["review"]
    out.setdefault("product", "")
    # Attach fake_probability if missing so frontend can render a badge.
    if "fake_probability" not in out:
        out["fake_probability"] = score_fake_probability(out.get("review_text", ""))
    return out

def get_all_reviews(sentiment=None, rating=None):
    """Return list of reviews, optionally filtered by sentiment and/or rating."""
    raw = get_reviews_from_db()
    reviews = [_normalize_review(r) for r in raw]
    if sentiment:
        sentiment_lower = str(sentiment).strip().lower()
        if sentiment_lower in ("positive", "neutral", "negative"):
            reviews = [r for r in reviews if (r.get("sentiment") or "").lower() == sentiment_lower]
    if rating is not None:
        try:
            r_val = int(rating)
            if 1 <= r_val <= 5:
                reviews = [r for r in reviews if r.get("rating") == r_val]
        except (TypeError, ValueError):
            pass
    return reviews

def add_review(product, rating, review_text):
    """
    Append a new review: compute sentiment via VADER, save to JSON.
    Returns the created review dict with sentiment.
    """
    sentiment = analyze_text(review_text or "")
    reviews = get_reviews_from_db()
    reviews = [_normalize_review(r) for r in reviews]
    now = datetime.utcnow().strftime("%Y-%m-%d")
    new_review = {
        "product": (product or "").strip(),
        "review_text": (review_text or "").strip(),
        "rating": int(rating),
        "sentiment": sentiment,
        "date": now,
        "fake_probability": score_fake_probability(review_text or ""),
    }
    reviews.append(new_review)
    save_reviews_to_db(reviews)
    return new_review
