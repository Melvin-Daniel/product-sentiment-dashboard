import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reviews.json")

def get_all_reviews():
    with open(DATA_PATH, "r") as f:
        return json.load(f)