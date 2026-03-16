import json
from config import DATA_FILE as DATA_PATH

def get_reviews_from_db():
    """
    Simulates fetching reviews from a database.
    Currently reads from JSON file.
    """
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_reviews_to_db(reviews):
    """
    Simulates saving reviews to a database.
    Currently writes to JSON file.
    """
    with open(DATA_PATH, "w") as f:
        json.dump(reviews, f, indent=2)