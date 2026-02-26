def analyze_sentiments(reviews):
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    total_rating = 0

    for review in reviews:
        sentiment_count[review["sentiment"]] += 1
        total_rating += review["rating"]

    avg_rating = round(total_rating / len(reviews), 2) if reviews else 0

    return {
        "sentiment_count": sentiment_count,
        "average_rating": avg_rating
    }