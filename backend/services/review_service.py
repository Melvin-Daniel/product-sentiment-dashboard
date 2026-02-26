import json
import os
from scrapers.amazon_scraper import fetch_amazon_reviews
from scrapers.flipkart_scraper import fetch_flipkart_reviews
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reviews.json")

def get_all_reviews():
    with open(DATA_PATH, "r") as f:
        return json.load(f)
def get_reviews_by_product(product_name):
    amazon = fetch_amazon_reviews(product_name)
    flipkart = fetch_flipkart_reviews(product_name)
    return amazon + flipkart