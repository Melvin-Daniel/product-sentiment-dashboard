import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
AMAZON_SEARCH_URL = "https://www.amazon.in/s"
FALLBACK_REVIEWS = [
    "Great sound quality",
    "Battery life is poor",
    "Worth the price",
    "Average performance",
    "Build quality could be better",
]


def _extract_reviews_from_html(html: str) -> List[str]:
    """Extract review-like snippets from Amazon search-result HTML."""
    soup = BeautifulSoup(html, "lxml")

    # Amazon HTML varies by request context; keep a broad selector set for resilience.
    selectors = [
        "span.a-size-base.s-underline-text",
        "div.a-row.a-size-small span.a-size-base",
        "span.a-size-base.a-color-secondary",
        "span[data-hook='review-body']",
    ]

    reviews: List[str] = []
    seen = set()

    for selector in selectors:
        for node in soup.select(selector):
            text = re.sub(r"\s+", " ", node.get_text(strip=True))
            if not text:
                continue

            # Skip non-review fragments often found in Amazon pages.
            if text.lower() in {"sponsored", "prime", "amazon's choice"}:
                continue

            if text not in seen:
                seen.add(text)
                reviews.append(text)

    return reviews


def _fallback_reviews(reason: str) -> List[str]:
    """Return local fallback reviews when scraping fails."""
    print(f"Warning: {reason}. Falling back to local reviews.")
    return [str(review) for review in FALLBACK_REVIEWS]


def _build_retry_session() -> requests.Session:
    """Create a requests session configured with retry behavior."""
    scraper_session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    scraper_session.mount("http://", adapter)
    scraper_session.mount("https://", adapter)
    return scraper_session


def get_amazon_reviews(query="headphones", pages=5, timeout=15, session=None) -> List[str]:
    """Scrape Amazon pages and always return a list of review strings."""
    own_session = session is None
    scraper_session: Optional[requests.Session] = session or _build_retry_session()

    try:
        reviews: List[str] = []

        for page in range(1, max(1, int(pages)) + 1):
            response = scraper_session.get(
                AMAZON_SEARCH_URL,
                params={"k": query, "page": page},
                headers=HEADERS,
                timeout=timeout,
            )

            if response.status_code != 200:
                return _fallback_reviews(f"Amazon returned status {response.status_code}")

            reviews.extend(_extract_reviews_from_html(response.text))

        cleaned_reviews = [str(review) for review in reviews if isinstance(review, str) and review.strip()]
        if not cleaned_reviews:
            return _fallback_reviews("No reviews found in scraped HTML")

        return cleaned_reviews

    except Exception as exc:  # noqa: BLE001 - scraper must never crash the pipeline.
        return _fallback_reviews(f"Amazon scraping failed with error: {exc}")
    finally:
        if own_session and scraper_session is not None:
            scraper_session.close()


if __name__ == "__main__":
    scraped_reviews = get_amazon_reviews()
    print(scraped_reviews)
