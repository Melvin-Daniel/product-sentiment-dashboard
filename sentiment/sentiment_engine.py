from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from cleaner import clean_text

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(review_text, rating):

    cleaned = clean_text(review_text)

    scores = analyzer.polarity_scores(cleaned)

    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"

    elif compound <= -0.05:
        label = "negative"

    else:
        label = "neutral"

    return {
        "review_text": review_text,
        "rating": rating,
        "sentiment_score": compound,
        "sentiment_label": label
    }
