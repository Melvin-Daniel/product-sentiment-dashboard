from flask import Flask, jsonify
from flask_cors import CORS
from config import DEBUG, HOST, PORT
from routes.reviews import reviews_bp
from routes.analytics import analytics_bp
from utils.logger import setup_logger

# Ensure VADER lexicon is available for sentiment analysis
def _ensure_nltk():
    try:
        import nltk
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)

_ensure_nltk()

app = Flask(__name__)
CORS(app)

logger = setup_logger()
logger.info("Starting backend application")

app.register_blueprint(reviews_bp)
app.register_blueprint(analytics_bp)

@app.route("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "Backend running"}
@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception")
    return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)