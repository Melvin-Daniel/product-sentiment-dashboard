import re
from typing import List

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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


def get_amazon_reviews() -> List[str]:
    """Scrape Amazon pages and return a list of extracted review snippets."""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    reviews: List[str] = []

    for page in range(1, 6):
        response = session.get(
            AMAZON_SEARCH_URL,
            params={"k": "headphones", "page": page},
            headers=HEADERS,
            timeout=15,
        )

        if response.status_code != 200:
            print(f"Warning: Amazon returned status {response.status_code}")
            return []

        reviews.extend(_extract_reviews_from_html(response.text))

    return reviews


if __name__ == "__main__":
    print(get_amazon_reviews())
