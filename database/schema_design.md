# Product Sentiment Dashboard - Database Design (MongoDB)

## 1) Database Overview

**Database name:** `product_sentiment_dashboard`

**Recommended Git branch for DB documentation updates:** `database`

The data model is centered around the three required entities:
- `products`
- `reviews`
- `sentiments`

To support dashboard speed and analytics queries, this design also includes an optional materialized collection:
- `product_analytics`

---

## 2) Collections and Fields

## 2.1 `products`

Stores product-level metadata and source ownership.

```json
{
  "_id": "ObjectId",
  "product_id": "string (unique, app-level id)",
  "name": "string",
  "brand": "string",
  "category": "string",
  "source": "string (amazon|flipkart|other)",
  "source_product_url": "string",
  "source_product_key": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_active": "boolean"
}
```

### Notes
- `product_id` is the shared identifier used by API (`/reviews`, `/analytics`) and internal modules.
- `source_product_key` stores source-native id (e.g., ASIN for Amazon).

---

## 2.2 `reviews`

Stores raw review data from scraper modules and normalized fields used by backend and UI.

```json
{
  "_id": "ObjectId",
  "review_id": "string (unique)",
  "product_id": "string (FK -> products.product_id)",
  "source": "string (amazon|flipkart)",
  "review_text": "string",
  "rating": "number (1-5)",
  "review_date": "datetime",
  "reviewer_name": "string|null",
  "review_title": "string|null",
  "verified_purchase": "boolean|null",
  "helpful_votes": "number|null",
  "language": "string|null",
  "scraped_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Notes
- Preserves required scraper output: `review_text`, `rating`, `date` (`review_date`).
- `review_id` should be stable across re-scrapes to avoid duplicates.

---

## 2.3 `sentiments`

Stores NLP inference output per review.

```json
{
  "_id": "ObjectId",
  "sentiment_id": "string (unique)",
  "review_id": "string (FK -> reviews.review_id)",
  "product_id": "string (denormalized FK -> products.product_id)",
  "sentiment_score": "number (-1 to +1 or 0 to 1 by model)",
  "sentiment_label": "string (positive|neutral|negative)",
  "model_name": "string (vader|textblob|custom)",
  "model_version": "string",
  "confidence": "number|null",
  "processed_text": "string|null",
  "processed_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Notes
- Preserves required NLP output: `sentiment_score`, `sentiment_label`.
- Keeping `product_id` here avoids expensive join-like lookups in some analytics queries.

---

## 2.4 `product_analytics` (Optional but recommended)

Materialized aggregate for fast dashboard rendering.

```json
{
  "_id": "ObjectId",
  "product_id": "string (unique)",
  "total_reviews": "number",
  "avg_rating": "number",
  "positive_count": "number",
  "neutral_count": "number",
  "negative_count": "number",
  "positive_pct": "number",
  "neutral_pct": "number",
  "negative_pct": "number",
  "rating_distribution": {
    "1": "number",
    "2": "number",
    "3": "number",
    "4": "number",
    "5": "number"
  },
  "last_review_date": "datetime|null",
  "last_scraped_at": "datetime|null",
  "updated_at": "datetime"
}
```

---

## 3) Relationships

1. `products (1) -> (N) reviews`
   - Join key: `products.product_id = reviews.product_id`
2. `reviews (1) -> (1) sentiments` (or `(N)` if storing multiple model runs)
   - Join key: `reviews.review_id = sentiments.review_id`
3. `products (1) -> (1) product_analytics`
   - Join key: `products.product_id = product_analytics.product_id`

---

## 4) Indexing Strategy

### `products`
- Unique: `{ product_id: 1 }`
- Search: `{ name: "text" }`
- Lookup by source: `{ source: 1, source_product_key: 1 }` (unique when available)

### `reviews`
- Unique: `{ review_id: 1 }`
- Query by product/date: `{ product_id: 1, review_date: -1 }`
- Query by source/date: `{ source: 1, review_date: -1 }`
- Optional dedupe index: `{ product_id: 1, review_text: 1, review_date: 1 }`

### `sentiments`
- Unique: `{ sentiment_id: 1 }`
- One sentiment per review: `{ review_id: 1 }` (unique)
- Analytics by product/label: `{ product_id: 1, sentiment_label: 1 }`

### `product_analytics`
- Unique: `{ product_id: 1 }`

---

## 5) API Contract Mapping

Given your API blueprint:
- `POST /search` with `product_name` -> create/find a record in `products`, return `product_id`
- `GET /reviews?product_id=...` -> read from `reviews` (+ optional sentiment join)
- `GET /analytics?product_id=...` -> read from `product_analytics` (or aggregate from `reviews + sentiments`)

---

## 6) Data Validation Rules

- `rating` must be numeric in range `[1, 5]`
- `sentiment_label` must be one of `positive | neutral | negative`
- `review_text` should be non-empty after trim
- `product_id`, `review_id`, `sentiment_id` are immutable after creation
- Timestamps stored in UTC (`created_at`, `updated_at`, `processed_at`, `scraped_at`)

---

## 7) Example End-to-End Data Flow

1. User searches product name.
2. Backend resolves/creates `products` document.
3. Scraper stores normalized `reviews` documents.
4. NLP module writes `sentiments` per review.
5. Analytics worker updates `product_analytics`.
6. Frontend dashboard reads `/reviews` and `/analytics`.

---

## 8) Suggested Folder-Level Ownership

- **Database Designer**: schema creation, indexes, migration scripts
- **Backend Developer**: repository layer + query optimization
- **NLP Developer**: sentiment write contract
- **Scraper Developers**: review normalization contract

This keeps all modules aligned with a stable DB contract before coding expansion.
