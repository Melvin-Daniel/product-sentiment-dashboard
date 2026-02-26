from flask import Flask
from flask_cors import CORS
from config import DEBUG, HOST, PORT
from routes.reviews import reviews_bp
from routes.analytics import analytics_bp
from utils.logger import setup_logger

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
    return {
        "status": "error",
        "message": str(e)
    }, 500

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)