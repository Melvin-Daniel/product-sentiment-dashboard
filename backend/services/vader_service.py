"""
NLTK VADER sentiment analysis for review text.
Ensures vader_lexicon is downloaded on first use.
"""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def _ensure_vader():
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)

_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _ensure_vader()
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer

def classify_sentiment(compound_score: float) -> str:
    """Map VADER compound score to positive / neutral / negative."""
    if compound_score >= 0.05:
        return "positive"
    if compound_score <= -0.05:
        return "negative"
    return "neutral"

def analyze_text(text: str) -> str:
    """Return sentiment label for given review text."""
    if not text or not str(text).strip():
        return "neutral"
    analyzer = get_analyzer()
    scores = analyzer.polarity_scores(str(text))
    return classify_sentiment(scores["compound"])
