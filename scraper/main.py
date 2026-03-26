import requests
import json
import time
import random
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from scraper import parse_book, parse_book_details, get_next_page

BASE_URL = "https://books.toscrape.com/"

# Using this header for browser compatibility 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Using this block to pass the rate-limiting, http and https retries
session = requests.Session()

# Session are more suitable for this case as we need to make continue handsake to the webpage
retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

def main():
    current_url = BASE_URL

    # These list are used to store the result and later used to dump in the JSon
    final_result = []
    failed_links = []

    # Adding count as to keep track of parsing
    total_success_count = 0
    total_failed_count = 0
    total_count = 0

    # USing while current_url so as when get_next_page returns None the loop will end
    while current_url:
        print(f"Parsing for page: {current_url}")
        try:
            html = fetch_page(current_url)
        except requests.exceptions.RequestException:
            print(f"\nFailed to fetch page: {current_url}\n")
            break

        links = parse_book(html=html, base_url=current_url)
        total_count += len(links)  # Count the total link in this page
        page_success_count = 0
        page_failed_count = 0
        for link in links:
            print(f"\nParsing for link: {link}\n")

            # Using random sleep to make request humane and not making bot behaviour
            time.sleep(random.uniform(0.5, 1.5))

            try:
                detail_html = fetch_page(link)
                detail = parse_book_details(detail_html, link)
                final_result.append(detail)
                total_success_count += 1
                page_success_count += 1

                # Dumping the json, takes json name and encdoing
                with open("output.json", "w", encoding="utf-8") as f:
                    json.dump(final_result, f, indent=4, ensure_ascii=False)

            except requests.exceptions.RequestException as e:
                print(f"\nFailed to fetch link: {link}\n")
                # Saving failed link to the list 
                failed_links.append({
                    "url": link,
                    "error": str(e),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                total_failed_count += 1 
                page_failed_count += 1

                # DUmping the failed links as json to keep track of them
                with open("failed_links.json", "w", encoding="utf-8") as f:
                    json.dump(failed_links, f, indent=4, ensure_ascii=False)

            # Summary for this iteration
            print(f"""
=====This Page Summary===============================================
Total Links: {len(links)}
Successfully Scraped:{page_success_count}  
Failed to Scraped {page_failed_count}
=====================================================================
                  """)


        # SUmmaary of this page extraction
        print(f"""
===================================== Page Done =====================================
Total so far:  {total_success_count}/{total_count} success    {total_failed_count} failed
=====================================
                """)

        current_url = get_next_page(html, current_url)
    
    # final summary after all pages
    print(f"""
  =====================================
  Scrape Complete
  Total Found : {total_count}
   Success   : {total_success_count}
   Failed    : {total_failed_count}
  =====================================
    """)

def fetch_page(url):
    response = session.get(url, headers=HEADERS, timeout=10)
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Status {response.status_code} for URL: {url}")
    return response.text

if __name__ == "__main__":
    main()