import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ASIN = "B09MNVKH6H"
url = f"https://www.amazon.in/product-reviews/{ASIN}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)

if "captcha" in response.text.lower() or "robot" in response.text.lower():
    print("Amazon blocked request. Loading sample dataset instead.")
    
    # Sample data fallback
    sample_data = [
        ["Great product", "5.0 out of 5 stars", "Amazing sound quality and battery life"],
        ["Not worth money", "2.0 out of 5 stars", "Battery drains quickly"],
        ["Good for price", "4.0 out of 5 stars", "Decent performance at this price range"]
    ]
    
    df = pd.DataFrame(sample_data, columns=["Title", "Rating", "Review"])
else:
    soup = BeautifulSoup(response.text, "html.parser")
    reviews = soup.find_all("div", {"data-hook": "review"})
    
    reviews_list = []
    
    for review in reviews:
        try:
            title = review.find("a", {"data-hook": "review-title"}).text.strip()
            rating = review.find("i", {"data-hook": "review-star-rating"}).text.strip()
            body = review.find("span", {"data-hook": "review-body"}).text.strip()
            reviews_list.append([title, rating, body])
        except:
            pass
    
    df = pd.DataFrame(reviews_list, columns=["Title", "Rating", "Review"])

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    if score['compound'] >= 0.05:
        return "Positive"
    elif score['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Review"].apply(get_sentiment)

df.to_csv("amazon_reviews_output.csv", index=False)

print("Process Completed Successfully!")