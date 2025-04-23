import requests
import time
import random
import json


url = "https://v3-api.newscatcherapi.com/api/latest_headlines"

querystring = {"when":"365d", "sources":"www.banner-tribune.com", "page_size": "1000"}

headers = {"x-api-token": "J05Bvm2fYsKyp7BD3OQgTPZRH4lRTYwP"}

def exponential_backoff(retries):
    time.sleep((2**retries) + random.uniform(0, 1))

def fetch_all_pages():
    all_articles = []
    page = 1
    total_pages = None
    retries = 0
    max_retries = 2

    while total_pages is None or page <= total_pages:
        querystring["page"] = page
        try:
            response = requests.post(url, headers=headers, json=querystring)
            response.raise_for_status()
            data = response.json()

            if "total_pages" not in data or "articles" not in data:
                print(f"Unexpected response format on page {page}: {data}")
                break

            # Use the total_pages directly from the API response
            if total_pages is None:
                total_pages = data["total_pages"]

            all_articles.extend(data["articles"])
            print(f"Fetched page {page} of {total_pages}")

            if page >= total_pages:
                break

            page = page + 1
            time.sleep(1)  # Respect rate limits
            retries = 0  # Reset retries after a successful request

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page}: {e}")
            retries += 1
            if retries >= max_retries:
                print("Max retries reached, aborting.")
                break
            exponential_backoff(retries)

    return all_articles

# Writing to sample.json
with open("Batch53.1.json", "w") as outfile:
    json.dump(fetch_all_pages(), outfile, indent = 4)
