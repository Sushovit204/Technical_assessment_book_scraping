from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def parse_book(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    links = []
    for book in books:
        a_tag = book.find("h3").find("a")
        relative_url = a_tag.get("href")
        absolute_url = urljoin(base_url, relative_url)
        links.append(absolute_url)
    return links

def parse_book_details(html, url):
    soup = BeautifulSoup(html, "html.parser")
    name = soup.find("h1").text.strip()
    price = soup.find("p", class_="price_color").text.strip()
    availability = soup.find("p", class_="availability").text.strip()
    description_tag = soup.find("div", id="product_description")
    if description_tag:
        description = description_tag.find_next_sibling("p").text.strip()
    else:
        description = ""
    table = soup.find("table")
    rows = table.find_all("tr")
    product_info = {}
    for row in rows:
        key = row.find("th").text.strip()
        value = row.find("td").text.strip()
        product_info[key] = value
    upc = product_info.get("UPC", "")
    tax = product_info.get("Tax", "")
    rating_tag = soup.find("p", class_="star-rating")
    rating_classes = rating_tag.get("class", [])
    rating = [c for c in rating_classes if c != "star-rating"][0]
    return {
        "name": name,
        "url": url,
        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
        "description": description[:50] + "...",
        "price": price,
        "tax": tax,
        "availability": availability,
        "upc": upc,
        "rating": rating,
    }

def get_next_page(html, current_url):
    soup = BeautifulSoup(html, "html.parser")
    next_tag = soup.find("li", class_="next")
    if next_tag:
        return urljoin(current_url, next_tag.find("a").get("href"))
    return None