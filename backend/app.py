from flask import Flask
from flask_cors import CORS

from routes.reviews import reviews_bp
from routes.analytics import analytics_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(reviews_bp)
app.register_blueprint(analytics_bp)

@app.route("/health")
def health():
    return {"status": "Backend running"}

if __name__ == "__main__":
    app.run(debug=True)