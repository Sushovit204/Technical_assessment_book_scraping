import requests

BASE_URL = "https://books.toscrape.com/"

def main():
    result = fetch_page(BASE_URL)
    print(result)

def fetch_page(url):
    """Function used to fetch page"""
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from {BASE_URL}")
    
    return response.text

if __name__ == "__main__":
    main()