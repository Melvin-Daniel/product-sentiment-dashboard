"""
Insights routes.

- GET /insights/summary → short AI-style review summary
"""
from flask import Blueprint, jsonify
from services.review_service import get_all_reviews
from services.insights_service import build_summary
from utils.response import success, error
import logging

insights_bp = Blueprint("insights_bp", __name__)


@insights_bp.route("/insights/summary", methods=["GET"])
def insights_summary():
    logging.info("GET /insights/summary called")
    try:
        reviews = get_all_reviews()
        summary = build_summary(reviews)
        return jsonify(success({"summary": summary}))
    except Exception as e:
        logging.exception("GET /insights/summary error")
        return jsonify(error(str(e))), 500

