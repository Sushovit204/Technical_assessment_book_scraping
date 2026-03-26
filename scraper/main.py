import requests
import json
import time
import random
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from scraper import parse_book, parse_book_details, get_next_page

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Use this block to pass the rate-limiting, http and https retries
session = requests.Session()
retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

def main():
    current_url = BASE_URL
    final_result = []
    while current_url:
        print(f"Parsing for page: {current_url}")
        try:
            html = fetch_page(current_url)
        except requests.exceptions.RequestException:
            sys.stderr.write(f"Failed to fetch page: {current_url}\n")
            break
        links = parse_book(html=html, base_url=current_url)
        for link in links:
            print(f"Parsing for link: {link}")
            time.sleep(random.uniform(0.5, 1.5))
            try:
                detail_html = fetch_page(link)
                detail = parse_book_details(detail_html, link)
                final_result.append(detail)
                with open("output.json", "w", encoding="utf-8") as f:
                    json.dump(final_result, f, indent=4, ensure_ascii=False)
            except requests.exceptions.RequestException:
                sys.stderr.write(f"Failed to fetch link: {link}\n")
                continue
        current_url = get_next_page(html, current_url)

def fetch_page(url):
    response = session.get(url, headers=HEADERS, timeout=10)
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Status {response.status_code} for URL: {url}")
    return response.text

if __name__ == "__main__":
    main()