# API Contract – Product Sentiment Dashboard

All successful responses use the envelope:

```json
{
  "status": "success",
  "data": ...
}
```

Error responses:

```json
{
  "status": "error",
  "message": "string"
}
```

---

## GET /reviews

Returns a list of reviews. Optional query parameters:

- `sentiment` – filter by `positive`, `neutral`, or `negative`
- `rating` – filter by star rating (1–5)

**Response (200):**

```json
{
  "status": "success",
  "data": [
    {
      "product": "string",
      "review_text": "string",
      "rating": 1-5,
      "sentiment": "positive | neutral | negative"
    }
  ]
}
```

---

## POST /reviews

Add a new review. Sentiment is computed server-side using NLTK VADER.

**Request body:**

```json
{
  "product": "string (optional)",
  "rating": 1-5,
  "review_text": "string (required)"
}
```

**Response (201):**

```json
{
  "status": "success",
  "data": {
    "product": "string",
    "review_text": "string",
    "rating": 1-5,
    "sentiment": "positive | neutral | negative"
  }
}
```

**Errors:** 400 if `review_text` is missing/empty or `rating` is not 1–5.

---

## GET /analytics

Returns aggregated analytics for all reviews.

**Response (200):**

```json
{
  "status": "success",
  "data": {
    "sentiment_count": {
      "positive": 0,
      "neutral": 0,
      "negative": 0
    },
    "average_rating": 0.0,
    "total_reviews": 0,
    "top_keywords": [
      { "word": "string", "count": 0 }
    ]
  }
}
```

---

## GET /health

**Response (200):**

```json
{
  "status": "Backend running"
}
```
