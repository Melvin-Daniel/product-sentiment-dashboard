from flask import Blueprint, jsonify
from services.review_service import get_all_reviews
from utils.response import success
import logging
reviews_bp = Blueprint("reviews_bp", __name__)
@reviews_bp.route("/reviews", methods=["GET"])
def reviews():
    logging.info("GET /reviews called")
    reviews = get_all_reviews()
    return jsonify(success(reviews))