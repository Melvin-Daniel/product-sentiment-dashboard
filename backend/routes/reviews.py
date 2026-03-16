"""
GET /reviews - list reviews with optional ?sentiment= & ?rating=
POST /reviews - add a review (product, rating, review_text); sentiment computed server-side.
"""
from flask import Blueprint, request, jsonify
from services.review_service import get_all_reviews, add_review
from utils.response import success, error
import logging

reviews_bp = Blueprint("reviews_bp", __name__)

@reviews_bp.route("/reviews", methods=["GET"])
def list_reviews():
    logging.info("GET /reviews called")
    try:
        sentiment = request.args.get("sentiment")
        rating = request.args.get("rating")
        reviews = get_all_reviews(sentiment=sentiment, rating=rating)
        return jsonify(success(reviews))
    except Exception as e:
        logging.exception("GET /reviews error")
        return jsonify(error(str(e))), 500

@reviews_bp.route("/reviews", methods=["POST"])
def create_review():
    logging.info("POST /reviews called")
    try:
        body = request.get_json(force=False) or {}
        product = body.get("product", "")
        rating = body.get("rating")
        review_text = body.get("review_text", "")

        if review_text is None or not str(review_text).strip():
            return jsonify(error("review_text is required and cannot be empty")), 400
        try:
            r = int(rating)
            if r < 1 or r > 5:
                return jsonify(error("rating must be between 1 and 5")), 400
        except (TypeError, ValueError):
            return jsonify(error("rating must be an integer between 1 and 5")), 400

        new_review = add_review(product=product, rating=int(rating), review_text=review_text)
        return jsonify(success(new_review)), 201
    except Exception as e:
        logging.exception("POST /reviews error")
        return jsonify(error(str(e))), 500
