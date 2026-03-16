"""
Analytics routes:
- GET /analytics           → overall sentiment, rating, keyword analytics (existing)
- GET /analytics/products  → per-product sentiment comparison
- GET /analytics/trends    → sentiment trend over time
"""
from flask import Blueprint, jsonify
from services.review_service import get_all_reviews
from services.sentiment_service import analyze_sentiments
from services.analytics_service import product_analytics, trend_analytics
from utils.response import success, error
import logging

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def analytics():
    logging.info("GET /analytics called")
    try:
        reviews = get_all_reviews()
        analytics_data = analyze_sentiments(reviews)
        return jsonify(success(analytics_data))
    except Exception as e:
        logging.exception("GET /analytics error")
        return jsonify(error(str(e))), 500


@analytics_bp.route("/analytics/products", methods=["GET"])
def analytics_products():
    logging.info("GET /analytics/products called")
    try:
        reviews = get_all_reviews()
        data = product_analytics(reviews)
        return jsonify(success(data))
    except Exception as e:
        logging.exception("GET /analytics/products error")
        return jsonify(error(str(e))), 500


@analytics_bp.route("/analytics/trends", methods=["GET"])
def analytics_trends():
    logging.info("GET /analytics/trends called")
    try:
        reviews = get_all_reviews()
        data = trend_analytics(reviews)
        return jsonify(success(data))
    except Exception as e:
        logging.exception("GET /analytics/trends error")
        return jsonify(error(str(e))), 500

