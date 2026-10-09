"""Phase 3 · Data ingestion · Scraping, and CSV vs JSON vs Parquet.

Start the practice API/website first:   python mock_api.py
"""

# %% 0. Setup
import time
from pathlib import Path
from urllib import robotparser

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "http://127.0.0.1:8765"
OUT = Path("formats")
OUT.mkdir(exist_ok=True)

# %% 1. Read robots.txt before crawling anything
rp = robotparser.RobotFileParser(f"{BASE}/robots.txt")
rp.read()
print("may fetch /catalog/page/1:", rp.can_fetch("practice-bot", f"{BASE}/catalog/page/1"))
print("may fetch /admin/prices:  ", rp.can_fetch("practice-bot", f"{BASE}/admin/prices"))
print("crawl delay:", rp.crawl_delay("practice-bot"), "second(s)")

# %% 2. Scrape every catalogue page by following the "Next" link
headers = {"User-Agent": "practice-bot/1.0 (learner@example.com)"}
url, products = f"{BASE}/catalog/page/1", []
while url:
    html = requests.get(url, headers=headers, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    for card in soup.select("div.product"):
        products.append({
            "sku": card["data-sku"],
            "product": card.select_one(".name").get_text(strip=True),
            "category": card.select_one(".category").get_text(strip=True),
            "price_bdt": float(card.select_one(".price").get_text(strip=True).replace("BDT", "").replace(",", "")),
            "in_stock": card.select_one(".stock").get_text(strip=True) == "In stock",
        })
    nxt = soup.select_one("a.next")
    url = f"{BASE}{nxt['href']}" if nxt else None
    time.sleep(rp.crawl_delay("practice-bot") or 1)          # be polite
catalog = pd.DataFrame(products)
print(catalog.head(3).to_string(index=False))
print(len(catalog), "products |", (~catalog["in_stock"]).sum(), "out of stock")

# %% 3. Same orders, four file formats
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
orders.to_csv(OUT / "orders.csv", index=False)
orders.to_json(OUT / "orders.json", orient="records", date_format="iso")
orders.to_json(OUT / "orders.jsonl", orient="records", lines=True, date_format="iso")
orders.to_parquet(OUT / "orders.parquet", index=False)                 # needs pyarrow
for f in ["orders.csv", "orders.json", "orders.jsonl", "orders.parquet"]:
    print(f"{f:15s} {(OUT / f).stat().st_size / 1024:7.0f} KB")

# %% 4. What survives a round trip? Types!
back_csv = pd.read_csv(OUT / "orders.csv")
back_pq = pd.read_parquet(OUT / "orders.parquet")
print("CSV     order_date:", back_csv["order_date"].dtype, "| delivery_days:", back_csv["delivery_days"].dtype)
print("Parquet order_date:", back_pq["order_date"].dtype, "| delivery_days:", back_pq["delivery_days"].dtype)

# %% 5. Read only what you need: Parquet stores columns separately
t = time.perf_counter()
for _ in range(20):
    pd.read_csv(OUT / "orders.csv", usecols=["region", "revenue"])
t_csv = (time.perf_counter() - t) / 20
t = time.perf_counter()
for _ in range(20):
    pd.read_parquet(OUT / "orders.parquet", columns=["region", "revenue"])
t_pq = (time.perf_counter() - t) / 20
print(f"read 2 columns: CSV {t_csv * 1000:.1f} ms | Parquet {t_pq * 1000:.1f} ms")

# %% 6. Nested JSON (as many APIs return it) -> a flat table
nested = [{"order_id": 1, "customer": {"id": "C010", "region": "Dhaka"}, "lines": [{"sku": "SKU-001", "qty": 120}]},
          {"order_id": 2, "customer": {"id": "C044", "region": "Gazipur"}, "lines": [{"sku": "SKU-005", "qty": 6000},
                                                                                       {"sku": "SKU-006", "qty": 900}]}]
print(pd.json_normalize(nested, record_path="lines", meta=["order_id", ["customer", "id"], ["customer", "region"]]))

# %% Try it yourself — solution: compare list price on the website with the price list file
prices = pd.read_csv("data/products_2025.csv")
check = catalog.merge(prices, on=["product", "category"], how="left")
check["implied_rate"] = (check["price_bdt"] / check["list_price"]).round(1)
print(check[["product", "list_price", "price_bdt", "implied_rate"]].head(4).to_string(index=False))
print("every product matched:", check["list_price"].notna().all(), "| rates:", sorted(float(x) for x in check["implied_rate"].unique()))
