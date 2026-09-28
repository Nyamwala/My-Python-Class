import csv
from datetime import datetime
import re  # Used to safely extract numbers from price text
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Configuration
BASE_URL = "https://books.toscrape.com/"
API_URL = "https://open.er-api.com/v6/latest/GBP"  # Free exchange rate API (Base: GBP)
TARGET_CURRENCY = "KES"  # Change to your desired currency (e.g., USD, EUR, KES)
OUTPUT_FILE = "converted_books_prices.csv"


def fetch_exchange_rate(target_currency):
  """Fetches the latest conversion rate for the target currency with error handling."""
  try:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    rate = data["rates"].get(target_currency)
    if not rate:
      raise ValueError(f"Currency '{target_currency}' not found in API response.")
    print(f"Successfully fetched exchange rate: 1 GBP = {rate} {target_currency}")
    return rate
  except requests.exceptions.RequestException as e:
    print(f"Network error while fetching exchange rates: {e}")
  except (ValueError, KeyError) as e:
    print(f"Data error: {e}")
  return None


def scrape_books():
  """Scrapes at least 10 book titles and prices from books.toscrape.com."""
  print(f"Scraping products from {BASE_URL}...")
  try:
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"  # Fixes character encoding mismatch for symbols
  except requests.exceptions.RequestException as e:
    print(f"Failed to connect to the website: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  products = []

  # Find all product pods on the page
  book_pods = soup.find_all("article", class_="product_pod")

  for pod in book_pods[:10]:  # Limit to at least 10 products
    try:
      # Extract title
      title = pod.find("h3").find("a")["title"]

      # Extract price text (e.g., '£51.77')
      price_text = pod.find("p", class_="price_color").text.strip()

      # Use regex to strip out non-digit characters except the decimal point
      numeric_string = re.sub(r"[^\d.]", "", price_text)
      price_numeric = float(numeric_string)

      products.append({"title": title, "price_gbp": price_numeric})
    except (AttributeError, ValueError) as e:
      print(f"Skipping an item due to parsing error: {e}")
      continue

  print(f"Successfully scraped {len(products)} products.")
  return products


def main():
  # 1. Scrape products
  products = scrape_books()
  if not products:
    print("No products scraped. Exiting program.")
    return

  # 2. Get Exchange Rate
  exchange_rate = fetch_exchange_rate(TARGET_CURRENCY)
  if not exchange_rate:
    print("Could not retrieve exchange rate. Exiting program.")
    return

  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # 3. Process and convert data
  processed_data = []
  for item in products:
    converted_price = round(item["price_gbp"] * exchange_rate, 2)
    processed_data.append(
        {
            "Product Title": item["title"],
            "Price (GBP)": item["price_gbp"],
            f"Price ({TARGET_CURRENCY})": converted_price,
            "Timestamp": timestamp,
        }
    )

  # 4. Save to CSV file
  df = pd.DataFrame(processed_data)
  df.to_csv(OUTPUT_FILE, index=False)
  print(f"\nData successfully saved to {OUTPUT_FILE}")

  # 5. Display in a readable table format using tabulate
  print("\n--- Converted Product Prices ---")
  print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))

  # 6. Optional Extension: Plot a simple bar chart
  try:
    plt.figure(figsize=(10, 6))
    # Shorten titles for cleaner chart labels
    short_titles = [
        title[:25] + "..." if len(title) > 25 else title
        for title in df["Product Title"]
    ]

    x = range(len(short_titles))
    width = 0.35

    plt.bar(
        [i - width / 2 for i in x],
        df["Price (GBP)"],
        width=width,
        label="Price (GBP)",
        color="skyblue",
    )
    # Scaling converted price for visual comparison alongside GBP values
    plt.bar(
        [i + width / 2 for i in x],
        df[f"Price ({TARGET_CURRENCY})"] / 10,
        width=width,
        label=f"Price ({TARGET_CURRENCY}) / 10",
        color="orange",
    )

    plt.xlabel("Book Titles")
    plt.ylabel("Value")
    plt.title(f"Original vs Converted Prices (Timestamp: {timestamp})")
    plt.xticks(x, short_titles, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()
  except Exception as e:
    print(f"Could not generate plot: {e}")


if __name__ == "__main__":
  main()