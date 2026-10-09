"""A small local web server that behaves like a real company API and website.

    python mock_api.py            # serves http://127.0.0.1:8765  (Ctrl+C to stop)

Endpoints (all data comes from data/orders_2025.csv and data/products_2025.csv):
    GET /api/v1/orders?page=1&page_size=500&since=2025-10-01   JSON, needs "Authorization: Bearer <token>"
    GET /api/v1/customers                                     JSON, same token
    GET /catalog/page/1 ... /catalog/page/2                   an HTML product catalogue (for scraping)
    GET /robots.txt                                           crawling rules

Like many real APIs it has a rate limit: every 5th request gets "429 Too Many Requests"
with a Retry-After header, so your client must retry politely.
"""
from __future__ import annotations

import csv
import json
import math
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).parent
TOKEN = os.environ.get("ORDERS_API_TOKEN", "practice-token-123")
PORT = int(os.environ.get("MOCK_API_PORT", "8765"))
HOST = os.environ.get("MOCK_API_HOST", "127.0.0.1")
NUMERIC = {"order_id": int, "quantity": int, "unit_price": float, "discount": float, "unit_cost": float,
           "promised_days": int, "revenue": float, "list_price": float}


def load_rows(name: str) -> list[dict]:
    with (HERE / "data" / name).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, cast in NUMERIC.items():
            if k in r and r[k] != "":
                r[k] = cast(r[k])
        if "delivery_days" in r:
            r["delivery_days"] = int(float(r["delivery_days"])) if r["delivery_days"] else None
    return rows


ORDERS = load_rows("orders_2025.csv")
CUSTOMERS = load_rows("customers_2025.csv")
PRODUCTS = load_rows("products_2025.csv")
STATE = {"requests": 0}


class Handler(BaseHTTPRequestHandler):
    server_version = "PracticeAPI/1.0"

    def log_message(self, fmt, *args):  # quiet console
        if os.environ.get("MOCK_API_LOG"):
            super().log_message(fmt, *args)

    def send_json(self, status: int, body: dict, headers: dict | None = None):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def send_text(self, status: int, text: str, ctype: str = "text/html; charset=utf-8"):
        data = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802 (name required by http.server)
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        if url.path == "/robots.txt":
            return self.send_text(200, "User-agent: *\nDisallow: /admin/\nCrawl-delay: 1\n", "text/plain")
        if url.path.startswith("/catalog/page/"):
            return self.catalog(int(url.path.rsplit("/", 1)[-1] or 1))
        if not url.path.startswith("/api/"):
            return self.send_json(404, {"error": "not found"})

        STATE["requests"] += 1
        if STATE["requests"] % 5 == 0:                          # simulated rate limit
            return self.send_json(429, {"error": "rate limit exceeded"}, {"Retry-After": "1"})
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self.send_json(401, {"error": "missing or invalid token"})

        if url.path == "/api/v1/customers":
            return self.send_json(200, {"data": CUSTOMERS, "total": len(CUSTOMERS)})
        if url.path == "/api/v1/orders":
            rows = [r for r in ORDERS if r["order_date"] >= q.get("since", "0000")]
            try:
                page, size = int(q.get("page", 1)), min(int(q.get("page_size", 500)), 1000)
            except ValueError:
                return self.send_json(400, {"error": "page and page_size must be integers"})
            pages = max(1, math.ceil(len(rows) / size))
            chunk = rows[(page - 1) * size: page * size]
            nxt = None
            if page < pages:
                nxt = f"/api/v1/orders?page={page + 1}&page_size={size}" + (f"&since={q['since']}" if "since" in q else "")
            return self.send_json(200, {"data": chunk, "page": page, "page_size": size, "total": len(rows),
                                        "total_pages": pages, "next": nxt})
        return self.send_json(404, {"error": "unknown endpoint"})

    def catalog(self, page: int):
        per = 6
        items = PRODUCTS[(page - 1) * per: page * per]
        if not items:
            return self.send_text(404, "<h1>Not found</h1>")
        cards = "\n".join(
            f'''  <div class="product" data-sku="SKU-{(page - 1) * per + i + 1:03d}">
    <h2 class="name">{p["product"]}</h2>
    <span class="category">{p["category"]}</span>
    <span class="price">BDT {p["list_price"] * 120:,.2f}</span>
    <span class="stock">{"In stock" if (i + page) % 4 else "Out of stock"}</span>
  </div>''' for i, p in enumerate(items))
        nav = f'<a class="next" href="/catalog/page/{page + 1}">Next</a>' if page * per < len(PRODUCTS) else ""
        html = f"""<!DOCTYPE html>
<html><head><title>Textile Supplies Catalogue — page {page}</title></head>
<body>
<h1>Product catalogue</h1>
<div class="products">
{cards}
</div>
{nav}
</body></html>"""
        return self.send_text(200, html)


def main():
    print(f"Practice API on http://{HOST}:{PORT}  (token: {TOKEN})  Ctrl+C to stop")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
