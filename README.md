# eBay Scraper

`ebay-dl.py` collects listings from the first 10 pages of an eBay search
and saves them to a JSON file named after the search term.

Each listing includes its name, price, condition, shipping cost,
free-return status, and number sold. Prices and shipping costs are
integer cents. Missing fields are saved as null.

## Setup

Install the required libraries in your activated Python environment:

```bash
python -m pip install requests beautifulsoup4
```

## Live searches

```bash
python ebay-dl.py --search "pokemon cards"
```

Live mode uses Requests to download pages and Beautiful Soup to extract
listings, with a one-second pause between pages.

## Saved searches: artificial practice data

eBay returned HTTP 403 during my live attempt, so all three included
JSON files contain the instructor's artificial practice listings,
not actual results for the search terms. Each file contains the same
30 listings from the 10 practice pages.

Download [practice-pages.zip](https://csci40.rtealwitter.com/projects/02_webscraping/practice-pages.zip)
into this repository and extract it:

```bash
python -m zipfile -e practice-pages.zip .
```

Generate the three saved searches:

```bash
python ebay-dl.py --search "pokemon cards" --pages-dir practice-pages
python ebay-dl.py --search "one piece cards" --pages-dir practice-pages
python ebay-dl.py --search "golf balls" --pages-dir practice-pages
```

## Assignment

[Project 2: Scraping eBay](https://csci40.rtealwitter.com/projects/02_webscraping/project.html)