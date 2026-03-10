from sentiment_engine import analyze_sentiment
from analytics import sentiment_summary
from test_reviews import reviews

results = []

for r in reviews:

    result = analyze_sentiment(r["review_text"], r["rating"])

    results.append(result)

print("Sentiment Results\n")

for r in results:
    print(r)

print("\nSentiment Summary\n")

print(sentiment_summary(results))
