import requests
import json
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

def main():
    current_url = BASE_URL
    final_result = []
    while current_url:
        print(f"Parsing for page:{current_url}")
        html = fetch_page(current_url)
        links = parse_book(html=html, base_url=current_url)
        for link in links:
            print(f"Parsing for link:{link}")
            detail_html = fetch_page(link)
            detail = parse_book_details(detail_html, link)
            print(detail)
            print("\n")
            final_result.append(detail)
        current_url = get_next_page(html, current_url)
    print(json.dumps(final_result, indent=4, ensure_ascii=False))


def fetch_page(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")
    return response.text

if __name__ == "__main__":
    main()