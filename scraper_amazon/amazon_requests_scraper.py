import re
from typing import List

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
    "Great product and good sound quality",
    "Very bad battery life",
    "Average performance but acceptable",
    "Worth the price",
    "Poor build quality",
]


def _extract_reviews_from_html(html: str) -> List[str]:
    """Extract review snippets from Amazon search-result HTML."""
    soup = BeautifulSoup(html, "lxml")
    review_nodes = soup.select("span.a-size-base.s-underline-text")

    reviews: List[str] = []
    for node in review_nodes:
        text = re.sub(r"\s+", " ", node.get_text(strip=True))
        if text:
            reviews.append(text)

    return reviews


def _fallback_reviews(reason: str) -> List[str]:
    """Return local fallback reviews when scraping fails."""
    print(f"Warning: {reason}. Falling back to local reviews.")
    return FALLBACK_REVIEWS.copy()


def _build_retry_session() -> requests.Session:
    """Create a requests session configured with retry behavior."""
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_amazon_reviews() -> List[str]:
    """Scrape Amazon pages and always return a list of review strings."""
    try:
        session = _build_retry_session()
        reviews: List[str] = []

        for page in range(1, 6):
            response = session.get(
                AMAZON_SEARCH_URL,
                params={"k": "headphones", "page": page},
                headers=HEADERS,
                timeout=15,
            )

            if response.status_code != 200:
                return _fallback_reviews(f"Amazon returned status {response.status_code}")

            reviews.extend(_extract_reviews_from_html(response.text))

        if not reviews:
            return _fallback_reviews("No reviews found in scraped HTML")

        return [str(review) for review in reviews if isinstance(review, str) and review.strip()]
    except Exception as exc:  # noqa: BLE001 - scraper must never crash the pipeline.
        return _fallback_reviews(f"Amazon scraping failed with error: {exc}")


if __name__ == "__main__":
    print(get_amazon_reviews())
