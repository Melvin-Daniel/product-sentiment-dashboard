from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/reviews")
def reviews():
    return jsonify([
        {"review_text": "Great phone", "rating": 5, "sentiment": "positive"},
        {"review_text": "Battery is average", "rating": 3, "sentiment": "neutral"},
        {"review_text": "Too expensive", "rating": 2, "sentiment": "negative"}
    ])

@app.route("/analytics")
def analytics():
    return jsonify({
        "positive": 1,
        "neutral": 1,
        "negative": 1,
        "avg_rating": 3.3
    })

if __name__ == "__main__":
    app.run(debug=True)