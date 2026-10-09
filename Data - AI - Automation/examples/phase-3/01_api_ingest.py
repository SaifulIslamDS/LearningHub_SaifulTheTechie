"""Phase 3 · Data ingestion · REST APIs, authentication and pagination.

Start the practice API first, in another terminal:   python mock_api.py
"""

# %% 0. Setup
import json
import os
import time
from pathlib import Path

import pandas as pd
import requests

BASE = os.environ.get("ORDERS_API_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("ORDERS_API_TOKEN", "practice-token-123")   # in real projects: never hard-code secrets
LANDING = Path("landing/orders")

# %% 1. A request without a token, then with one
r = requests.get(f"{BASE}/api/v1/orders", params={"page_size": 2}, timeout=10)
print(r.status_code, r.json())

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"})
r = session.get(f"{BASE}/api/v1/orders", params={"page_size": 2}, timeout=10)
body = r.json()
print(r.status_code, {k: body[k] for k in ["page", "page_size", "total", "total_pages", "next"]})
print(body["data"][0])


# %% 2. A polite GET: timeout, retry on 429/5xx with back-off, fail loudly on other errors
def get_json(url: str, params: dict | None = None, max_retries: int = 5) -> dict:
    for attempt in range(1, max_retries + 1):
        resp = session.get(url, params=params, timeout=10)
        if resp.status_code == 429 or resp.status_code >= 500:
            wait = float(resp.headers.get("Retry-After", 2 ** attempt))
            print(f"  {resp.status_code} on attempt {attempt}; waiting {wait:.0f}s")
            time.sleep(wait)
            continue
        resp.raise_for_status()                      # 400/401/403/404 -> exception, don't retry
        return resp.json()
    raise RuntimeError(f"gave up after {max_retries} attempts: {url}")


# %% 3. Follow the "next" links until there are no more pages; save every raw page
def ingest_orders(since: str | None = None, page_size: int = 500) -> list[dict]:
    LANDING.mkdir(parents=True, exist_ok=True)
    url, params, rows, page = f"{BASE}/api/v1/orders", {"page_size": page_size}, [], 0
    if since:
        params["since"] = since
    while url:
        body = get_json(url, params)
        page += 1
        (LANDING / f"page-{page:03d}.json").write_text(json.dumps(body))
        rows.extend(body["data"])
        print(f"page {body['page']}/{body['total_pages']}: {len(body['data'])} rows")
        url, params = (f"{BASE}{body['next']}", None) if body["next"] else (None, None)
    assert len(rows) == body["total"], "row count does not match the API's total"
    return rows


rows = ingest_orders()
orders = pd.DataFrame(rows)
print(orders.shape, "| net revenue:", round(orders.loc[orders.status != "Cancelled", "revenue"].sum(), 2))

# %% 4. Incremental load: only orders since a date (what a daily job would request)
recent = ingest_orders(since="2025-12-01")
print(len(recent), "orders since 2025-12-01")

# %% Try it yourself — solution: ingest customers and join them to the orders
customers = pd.DataFrame(get_json(f"{BASE}/api/v1/customers")["data"])
merged = orders.merge(customers[["customer_id", "credit_days"]], on="customer_id", how="left", validate="many_to_one")
print(customers.shape, "| orders without a customer match:", merged["credit_days"].isna().sum())
