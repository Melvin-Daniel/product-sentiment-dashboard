# Product Sentiment Dashboard

A web-based dashboard that analyzes product reviews, classifies sentiment with **NLTK VADER**, and visualizes sentiment distribution and analytics. Built for a university demo with a Flask backend and vanilla JS frontend.

---

## Project overview

- **Backend:** Flask REST API serving reviews and analytics; sentiment computed server-side with NLTK VADER.
- **Frontend:** Single-page app (HTML + CSS + JS) with Chart.js for visualizations.
- **Data:** Stored in a JSON file (`backend/data/sample_reviews.json`); no database required.
- **Features:** List reviews, filter by sentiment/rating, search, add new reviews (sentiment auto-computed), view sentiment distribution, average rating, total reviews, and top keywords.

---

## Architecture

```
frontend/
  index.html    → structure, styles, script tags
  app.js        → API calls, state, search/filters, add review, loading
  charts.js     → Chart.js rendering (doughnut, insight, keywords)

backend/
  app.py        → Flask app, CORS, NLTK vader_lexicon download, blueprints
  config.py     → HOST, PORT, DEBUG
  routes/
    reviews.py  → GET /reviews (optional ?sentiment=, ?rating=), POST /reviews
    analytics.py→ GET /analytics
  services/
    db_service.py         → read/write JSON file
    review_service.py     → get/add reviews, filtering, normalize review_text
    sentiment_service.py  → aggregate counts, avg rating, total, keywords
    vader_service.py      → NLTK VADER sentiment label (positive/neutral/negative)
  data/
    sample_reviews.json   → list of { product, review_text, rating, sentiment }
```

**Request flow:** Browser → `app.js` (API_BASE) → Flask routes → services → JSON file. New reviews get a sentiment label from `vader_service` before being saved.

---

## How to run

### 1. Backend (Flask)

```bash
# From project root
cd backend
pip install -r ../requirements.txt
```

If you use a virtual environment (recommended):

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r ../requirements.txt
```

The backend automatically runs `nltk.download('vader_lexicon')` on first import. To pre-download (e.g. offline use), run once:

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

Start the server (run from the `backend` folder so imports resolve correctly):

```bash
cd backend
python app.py
```

The API runs at **http://127.0.0.1:5000**.

### 2. Frontend

- Open `frontend/index.html` in a browser (double-click or “Open with Live Server” in VS Code).
- The page uses `API_BASE = "http://127.0.0.1:5000"` in `app.js`. Change this if your backend runs elsewhere.

**Note:** If you open the file via `file://`, some browsers may block requests to `http://127.0.0.1:5000`. Use a local server (e.g. Live Server) or run the frontend from the same origin if needed.

---

## Example API calls

**Health check**

```bash
curl http://127.0.0.1:5000/health
```

**Get all reviews**

```bash
curl http://127.0.0.1:5000/reviews
```

**Get reviews filtered by sentiment and rating**

```bash
curl "http://127.0.0.1:5000/reviews?sentiment=positive"
curl "http://127.0.0.1:5000/reviews?rating=5"
curl "http://127.0.0.1:5000/reviews?sentiment=negative&rating=2"
```

**Add a review** (sentiment is computed by the backend)

```bash
curl -X POST http://127.0.0.1:5000/reviews \
  -H "Content-Type: application/json" \
  -d "{\"product\":\"Demo Product\",\"rating\":4,\"review_text\":\"Really good quality and fast delivery.\"}"
```

**Get analytics**

```bash
curl http://127.0.0.1:5000/analytics
```

Response shape:

```json
{
  "status": "success",
  "data": {
    "sentiment_count": { "positive": 0, "neutral": 0, "negative": 0 },
    "average_rating": 0.0,
    "total_reviews": 0,
    "top_keywords": [ { "word": "string", "count": 0 } ]
  }
}
```

Full request/response details: **docs/contract.md**.

---

## Configurable API base

In **frontend/app.js**, the first line of the script sets:

```javascript
var API_BASE = "http://127.0.0.1:5000";
```

Change this to your backend URL (e.g. for production or another machine).

---

## Error handling

- **Backend:** Routes return JSON with `{ "status": "error", "message": "..." }` and appropriate status codes (400 for validation, 500 for server errors). Unhandled exceptions are caught by a global handler and returned as JSON.
- **Frontend:** Failed fetches show a message in `#errorMessage`; loading state is toggled so the UI does not assume data is present.

---

## Tech stack

| Layer     | Technology        |
|----------|-------------------|
| Backend  | Python 3, Flask, Flask-CORS |
| Frontend | HTML, CSS, JavaScript (no framework) |
| Charts   | Chart.js (CDN)    |
| Sentiment| NLTK VADER        |
| Data     | JSON file         |

---

## License and purpose

This project is for educational/demo use. Adjust as needed for your course or deployment environment.
