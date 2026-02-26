API CONTRACT – FINAL (DO NOT CHANGE)

GET /reviews
Response:
[
  {
    "review_text": "string",
    "rating": number,
    "sentiment": "positive | neutral | negative"
  }
]

GET /analytics
Response:
{
  "positive": number,
  "neutral": number,
  "negative": number,
  "avg_rating": number
}