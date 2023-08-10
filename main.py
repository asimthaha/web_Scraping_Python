import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.flipkart.com/search?q=tv+55+inch&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_2_2_na_na_ps&otracker1=AS_Query_OrganicAutoSuggest_2_2_na_na_ps&as-pos=2&as-type=RECENT&suggestionId=tv+55+inch&requestId=38af7f25-3721-4665-84b7-eb0b0fb51c8a&as-backfill=on"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

tv_data = []

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
tv_cards = soup.find_all("div", class_="_1AtVbE")

for tv in tv_cards:
    try:
        tv_name = tv.find("div", class_="_4rR01T").text
        tv_price = tv.find("div", class_="_30jeq3").text if tv.find("div",
                                                                                       class_="_30jeq3") else "N/A"
        tv_rating = tv.find("div", class_="_3LWZlK").text if tv.find("div",
                                                                                        class_="_3LWZlK") else "N/A"

        tv_data.append({
            "Name": tv_name,
            "Price": tv_price,
            "Rating": tv_rating
        })
    except Exception as e:
        print("Error in extracting TV data:", e)

df = pd.DataFrame(tv_data)
df.to_csv("tv_data.csv", index=False)

print("Data successfully extracted and CSV saved.")