import requests
import json
from scraper import parse_book, parse_book_details

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def main():
    html = fetch_page(BASE_URL)
    links = parse_book(html=html, base_url=BASE_URL)

    if links:
        detail_html = fetch_page(links[0])
        detail = parse_book_details(detail_html, links[0])
        print(json.dumps(detail, indent=4, ensure_ascii=False))

def fetch_page(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")
    return response.text

if __name__ == "__main__":
    main()