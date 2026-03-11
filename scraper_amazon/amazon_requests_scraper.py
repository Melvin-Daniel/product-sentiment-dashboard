import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": "Mozilla/5.0"}
AMAZON_SEARCH_URL = "https://www.amazon.in/s"


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


def get_amazon_reviews(
    query: str = "headphones",
    pages: int = 5,
    timeout: int = 15,
    session: Optional[requests.Session] = None,
) -> List[str]:
    """
    Scrape Amazon pages and return a list of extracted review snippets.

    Args:
        query: Search keyword used for product discovery.
        pages: Number of pages to scrape.
        timeout: HTTP timeout in seconds.
        session: Optional requests Session for reuse/testing.
    """
    client = session or requests.Session()
    reviews: List[str] = []

    for page in range(1, pages + 1):
        response = client.get(
            AMAZON_SEARCH_URL,
            params={"k": query, "page": page},
            headers=HEADERS,
            timeout=timeout,
        )
        response.raise_for_status()
        reviews.extend(_extract_reviews_from_html(response.text))

    return reviews


if __name__ == "__main__":
    scraped_reviews = get_amazon_reviews()
    print(f"Scraped {len(scraped_reviews)} review snippets.")
