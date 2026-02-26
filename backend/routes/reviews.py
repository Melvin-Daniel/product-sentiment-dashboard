from flask import Blueprint, jsonify
from services.review_service import get_all_reviews
from utils.response import success

reviews_bp = Blueprint("reviews_bp", __name__)

@reviews_bp.route("/reviews", methods=["GET"])
def reviews():
    reviews = get_all_reviews()
    return jsonify(success(reviews))