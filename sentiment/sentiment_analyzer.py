import json
import re
import string
from typing import Dict, List

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from scraper_amazon.amazon_requests_scraper import get_amazon_reviews


def _ensure_vader_lexicon() -> None:
    """Ensure the VADER lexicon is available in the runtime environment."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


def preprocess_text(text: str) -> str:
    """Normalize text by lowercasing and removing punctuation."""
    lowered = text.lower()
    no_punctuation = lowered.translate(str.maketrans("", "", string.punctuation))
    return re.sub(r"\s+", " ", no_punctuation).strip()


def classify_sentiment(score: float) -> str:
    """Classify sentiment label from VADER compound score."""
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def analyze_amazon_reviews() -> Dict[str, object]:
    """
    Fetch reviews from scraper and return aggregate + detailed sentiment output.
    """
    _ensure_vader_lexicon()
    reviews = get_amazon_reviews()
    analyzer = SentimentIntensityAnalyzer()

    results: List[Dict[str, str]] = []
    summary = {"positive": 0, "negative": 0, "neutral": 0}

    for review in reviews:
        cleaned_review = preprocess_text(review)
        score = analyzer.polarity_scores(cleaned_review)["compound"]
        sentiment = classify_sentiment(score)
        summary[sentiment] += 1
        results.append({"review": review, "sentiment": sentiment})

    return {
        "total_reviews": len(reviews),
        "positive": summary["positive"],
        "negative": summary["negative"],
        "neutral": summary["neutral"],
        "detailed_results": results,
    }


if __name__ == "__main__":
    result = analyze_amazon_reviews()
    print(json.dumps(result, indent=2))
