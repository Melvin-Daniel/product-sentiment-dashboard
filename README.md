Product Sentiment Analysis Dashboard

This project analyzes product reviews, classifies their sentiment, and visualizes the overall sentiment distribution using a web-based dashboard.

📌 Project Overview

The Product Sentiment Analysis Dashboard is a web-based application designed to analyze customer product reviews and present sentiment insights visually.

The system follows a modular, role-based architecture, where backend services, frontend UI, and visualization modules are developed independently and integrated using REST APIs.

This project demonstrates real-world concepts such as API-driven architecture, frontend–backend integration, and data visualization.

🧩 Project Structure
Product-Sentiment-Analysis-Dashboard/
│
├── backend/
│   └── Flask REST API for reviews and analytics
│
├── frontend/
│   ├── index.html
│   └── visualization/
│       └── charts.js
│
├── scraper_amazon/
│   └── Module reserved for Amazon review scraping (future enhancement)
│
├── scraper_flipkart/
│   └── Module reserved for Flipkart review scraping (future enhancement)
│
├── sentiment/
│   └── Module reserved for sentiment analysis logic (future enhancement)
│
├── database/
│   └── Database schema and data handling logic
│
├── docs/
│   └── contract.md
│
└── README.md
🔌 API Endpoints
GET /reviews

Returns product reviews along with sentiment labels.

GET /analytics

Returns aggregated sentiment counts and average product rating.

API request and response formats are defined in docs/contract.md.

📊 Data Visualization

Sentiment analytics are visualized using Chart.js, including:

Pie chart for sentiment distribution

Average product rating display

Visualization logic is separated into a dedicated module under:

frontend/visualization/charts.js
🛠️ Technologies Used

Backend: Python, Flask, REST API

Frontend: HTML, CSS, JavaScript

Visualization: Chart.js

Data Format: JSON

Architecture: Modular, role-based

Tools: Git, GitHub

🚀 How to Run the Project
Backend
cd backend
python app.py

The Flask server runs on http://127.0.0.1:5000.

Frontend

Navigate to the frontend/ directory.

Open index.html using Live Server or directly in a web browser.

The frontend automatically fetches data from the backend APIs.

📈 Output

Displays product reviews with sentiment labels

Visualizes sentiment distribution using a pie chart

Shows average product rating

Frontend and backend are integrated using REST APIs with CORS enabled

🔮 Future Enhancements

Implement live review scraping from Amazon and Flipkart

Integrate NLP-based sentiment analysis

Add database persistence

Deploy the application to the cloud

Enhance UI and analytics features

✅ Conclusion

The Product Sentiment Analysis Dashboard demonstrates a clean backend-driven architecture integrated with frontend visualization.
The project is designed to be extensible, scalable, and suitable for real-world sentiment analysis use cases.