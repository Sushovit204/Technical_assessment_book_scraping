# Book Scraper

A web scraper for `https://books.toscrape.com/` that extracts book details and saves them to a JSON file.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```text
.
├── scraper/
│   ├── main.py
│   └── scraper.py
├── output.json
├── README.md
└── requirements.txt
```

## Running the Scraper

To run the scraper, execute:
```bash
python3 scraper/main.py
```

The extracted data will be saved incrementally to `output.json`.

## Extracted book details json format

```json
{
"name": "A Light in the Attic",
"url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
"scrape_date": "2026-03-16",
"description": "It's hard to imagine a world without A Light in the Attic...",
"price": "£51.77",
"tax": "£0.00",
"availability": "In stock (22 available)",
"upc": "a897fe39b1053632"
}
```

## Features

1. Pagination is handled automatically.
2. Edge cases and network errors are handled efficiently with retries and timeouts.
