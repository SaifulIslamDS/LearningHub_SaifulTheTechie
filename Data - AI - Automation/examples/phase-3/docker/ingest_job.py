"""Containerised ingestion job: read every order from the API and save one Parquet file.

Settings come from environment variables (set them in compose.yaml), never from the code.
"""
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

BASE = os.environ["ORDERS_API_URL"]
TOKEN = os.environ["ORDERS_API_TOKEN"]
OUT = Path(os.environ.get("OUTPUT_DIR", "/out"))

session = requests.Session()
session.headers["Authorization"] = f"Bearer {TOKEN}"


def get_json(url: str, params: dict | None = None) -> dict:
    for attempt in range(1, 6):
        r = session.get(url, params=params, timeout=10)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"gave up: {url}")


def main() -> int:
    url, params, rows = f"{BASE}/api/v1/orders", {"page_size": 1000}, []
    while url:
        body = get_json(url, params)
        rows.extend(body["data"])
        url, params = (f"{BASE}{body['next']}", None) if body["next"] else (None, None)
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT / "orders.parquet", index=False)
    print(f"ingested {len(df)} orders (API total {body['total']}) -> {OUT / 'orders.parquet'}", flush=True)
    return 0 if len(df) == body["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
