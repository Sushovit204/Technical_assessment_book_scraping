from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


def parse_book(html:str, base_url:str) -> list[str]:
    """Function to parse the raw html"""
    soup = BeautifulSoup(html, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    links = []

    for book in books:
        a_tag = book.find("h3").find("a")
        relative_url = a_tag.get("href")

        absolute_url = urljoin(base_url, relative_url)

        links.append(absolute_url)
    
    return links