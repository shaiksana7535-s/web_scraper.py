"""
Web Scraper for Quotes and Headlines
Internship Project
"""

import csv
import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com"
OUTPUT_FILE = "scraped_quotes.csv"


def scrape_quotes():
    print(f"Fetching data from: {URL}...")
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching website: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    quote_elements = soup.find_all("div", class_="quote")

    extracted_data = []

    print("\n--- Scraped Quotes & Authors ---")
    for item in quote_elements:
        text = item.find("span", class_="text").get_text(strip=True)
        author = item.find("small", class_="author").get_text(strip=True)
        tags = [
            tag.get_text(strip=True)
            for tag in item.find_all("a", class_="tag")
        ]
        tags_str = ", ".join(tags) if tags else "N/A"

        print(f"Quote : {text}")
        print(f"Author: {author}")
        print(f"Tags  : {tags_str}\n" + "-" * 40)

        extracted_data.append(
            {"Quote": text, "Author": author, "Tags": tags_str}
        )

    # Save results to CSV
    try:
        with open(
            OUTPUT_FILE, mode="w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=["Quote", "Author", "Tags"]
            )
            writer.writeheader()
            writer.writerows(extracted_data)
        print(
            f"Successfully saved {len(extracted_data)} quotes to '{OUTPUT_FILE}'."
        )
    except Exception as e:
        print(f"Error saving to CSV: {e}")


if __name__ == "__main__":
    scrape_quotes()