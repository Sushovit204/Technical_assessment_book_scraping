import requests
from scraper import parse_book

BASE_URL = "https://books.toscrape.com/"

def main():
    html = fetch_page(BASE_URL)
    print(html)

    links = parse_book(html=html, base_url=BASE_URL)
    print(links)

    for link in links:
        print(link)

    print(f"Total books found:{len(links)}")

def fetch_page(url):
    """Function used to fetch page"""
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from {BASE_URL}")
    
    return response.text

if __name__ == "__main__":
    main()