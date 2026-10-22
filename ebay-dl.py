import time
import requests
import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def get_text(item, selector):
    element = item.select_one(selector)
    if element is None:
        return None
    return element.get_text(" ", strip=True)


def money_to_cents(text):
    if text is None:
        return None

    match = re.search(r"\$\s*([\d,]+)(?:\.(\d{2}))?", text)
    if match is None:
        return None

    dollars = int(match.group(1).replace(",", ""))
    cents = int(match.group(2) or "0")
    return dollars * 100 + cents


def extract_items(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    for item in soup.select(".s-item"):
        shipping_text = get_text(item, ".s-item__shipping")
        returns_text = get_text(item, ".s-item__free-returns")
        sold_text = get_text(item, ".s-item__hotness")

        shipping = money_to_cents(shipping_text)
        if shipping_text and "free" in shipping_text.lower():
            shipping = 0

        free_returns = None
        if returns_text is not None:
            free_returns = "free returns" in returns_text.lower()

        items_sold = None
        if sold_text:
            match = re.search(r"([\d,]+)\+?\s+sold", sold_text)
            if match:
                items_sold = int(match.group(1).replace(",", ""))

        listings.append({
            "name": get_text(item, ".s-item__title"),
            "price": money_to_cents(get_text(item, ".s-item__price")),
            "status": get_text(item, ".SECONDARY_INFO"),
            "shipping": shipping,
            "free_returns": free_returns,
            "items_sold": items_sold,
        })

    return listings


parser = argparse.ArgumentParser()
parser.add_argument("--search", required=True)
parser.add_argument("--pages-dir")
args = parser.parse_args()

listings = []

for page_number in range(1, 11):
    if args.pages_dir:
        page_path = Path(args.pages_dir) / f"page-{page_number}.html"
        html = page_path.read_text(encoding="utf-8")
    else:
        response = requests.get(
            "https://www.ebay.com/sch/i.html",
            params={"_nkw": args.search, "_pgn": page_number},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        response.raise_for_status()
        html = response.text

    page_items = extract_items(html)

    if not page_items:
        raise RuntimeError(
            "No listings found. Stop live requests and use --pages-dir practice-pages."
        )

    listings.extend(page_items)
    print(f"Page {page_number}: {len(page_items)} listings")

    if not args.pages_dir and page_number < 10:
        time.sleep(1)

output_path = Path(f"{args.search}.json")
with output_path.open("w", encoding="utf-8") as file:
    json.dump(listings, file, indent=2, ensure_ascii=False)

print(f"Saved {len(listings)} listings to {output_path}")