import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0"}

data = []

for page in range(1,6):

    url = f"https://www.amazon.in/s?k=headphones&page={page}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "lxml")

    items = soup.select(".s-result-item")

    for item in items:

        name = item.select_one(".a-size-medium.a-color-base.a-text-normal")
        price = item.select_one(".a-price-whole")
        rating = item.select_one(".a-icon-alt")

        name = name.text if name else "N/A"
        price = price.text if price else "N/A"
        rating = rating.text if rating else "N/A"

        data.append([name, price, rating])

df = pd.DataFrame(data, columns=["Product","Price","Rating"])

df.to_csv("amazon_products.csv", index=False)

print(df.head())
