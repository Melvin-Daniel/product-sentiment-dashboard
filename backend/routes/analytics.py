from flask import Blueprint, jsonify
from services.review_service import get_all_reviews
from services.sentiment_service import analyze_sentiments
from utils.response import success
import logging
analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def analytics():
    logging.info("GET /analytics called")
    reviews = get_all_reviews()
    analytics_data = analyze_sentiments(reviews)
    return jsonify(success(analytics_data))