---
title: "Web Scraping and File Formats: HTML, CSV, JSON & Parquet"
order: 2
summary: "Scrape a web page responsibly with Beautiful Soup (robots.txt, delays, a real User-Agent), flatten nested JSON, and choose between CSV, JSON and Parquet by size, speed and type safety."
level: Intermediate
time: "50 min"
topics: ["Scraping", "CSV, JSON & Parquet"]
prerequisites: ["phase-3/data-ingestion/01-rest-apis-auth-pagination"]
keywords: [web scraping, scraping, beautifulsoup, beautiful soup, html, css selector, robots.txt, crawl delay, user-agent, terms of service, csv, json, jsonl, json lines, parquet, columnar, json_normalize, nested json, file format, compression, schema, data types]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Beautiful Soup documentation"
    url: "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
    source: "Beautiful Soup (official)"
    note: "Parsing HTML, CSS selectors and navigating the tree."
  - title: "Apache Parquet documentation"
    url: "https://parquet.apache.org/docs/"
    source: "Apache Parquet (official)"
    note: "How the columnar format stores and compresses data."
  - title: "pandas: IO tools (CSV, JSON, Parquet)"
    url: "https://pandas.pydata.org/docs/user_guide/io.html"
    source: "pandas official docs"
    note: "Every read_/to_ function and its options."
---

## What is it?

- **Web scraping** = extracting data from web pages (HTML) when there's no API. You download the page, then pick values out with **CSS selectors**.
- **File formats** decide how collected data is stored:

| Format | Shape | Types kept? | Size | Best for |
|---|---|---|---|---|
| **CSV** | Rows of text | ❌ everything is text | Medium | Exchanging tables with people and Excel |
| **JSON** | Nested objects | Partly (numbers, true/false; no dates) | Large | API responses, nested data |
| **JSON Lines** (`.jsonl`) | One JSON object per line | Partly | Large | Logs, streaming, appendable raw data |
| **Parquet** | Columns, compressed | ✅ ints, decimals, dates, nulls | Small | Analytics, data lakes, pipelines |

!!! job "Why it matters at work"
    Competitor prices, supplier catalogues and public statistics often exist only as web pages. And every pipeline decides on a storage format: Parquet is the default for analytics in modern data platforms, so knowing why (and when CSV or JSON is still right) is basic data engineering literacy.

The script is `02_scrape_formats.py`. Keep the practice API running: it also serves a small **product catalogue website**.

## Part 1: scrape responsibly

### Check the rules first

```python
from urllib import robotparser

rp = robotparser.RobotFileParser(f"{BASE}/robots.txt")
rp.read()
print("may fetch /catalog/page/1:", rp.can_fetch("practice-bot", f"{BASE}/catalog/page/1"))
print("may fetch /admin/prices:  ", rp.can_fetch("practice-bot", f"{BASE}/admin/prices"))
print("crawl delay:", rp.crawl_delay("practice-bot"), "second(s)")
```

```text
may fetch /catalog/page/1: True
may fetch /admin/prices:   False
crawl delay: 1 second(s)
```

!!! warning "Legal and ethical scraping"
    `robots.txt` states what the site owner allows automated tools to fetch. Also read the site's **terms of service**, never scrape personal data or anything behind a login without permission, identify yourself with a real `User-Agent`, and go slowly. If the site offers an API or a download, use that instead.

### Pick values out of the HTML

Each product on the page looks like this:

```html
<div class="product" data-sku="SKU-001">
  <h2 class="name">Cotton Twill</h2>
  <span class="category">Fabric</span>
  <span class="price">BDT 420.00</span>
  <span class="stock">In stock</span>
</div>
```

```python
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
```

```text
    sku      product category  price_bdt  in_stock
SKU-001 Cotton Twill   Fabric      420.0      True
SKU-002   Denim 12oz   Fabric      624.0      True
SKU-003 Poplin White   Fabric      348.0      True
12 products | 2 out of stock
```

- `soup.select("div.product")` finds every element matching the **CSS selector**; `select_one` finds the first.
- `card["data-sku"]` reads an attribute; `.get_text(strip=True)` reads the visible text.
- Clean as you go: `"BDT 420.00"` → `420.0`.
- Scrapers **break** when the site's HTML changes. Test that each field was found, and alert when a page returns 0 products.

Pages built by JavaScript in the browser don't contain the data in their HTML. Look for the JSON API the page calls (browser DevTools → Network tab), or use a browser automation tool such as Playwright.

## Part 2: CSV vs JSON vs Parquet

```python
orders.to_csv(OUT / "orders.csv", index=False)
orders.to_json(OUT / "orders.json", orient="records", date_format="iso")
orders.to_json(OUT / "orders.jsonl", orient="records", lines=True, date_format="iso")
orders.to_parquet(OUT / "orders.parquet", index=False)                 # needs pyarrow
```

```text
orders.csv          472 KB
orders.json        1373 KB
orders.jsonl       1373 KB
orders.parquet      106 KB
```

The same 4,246 orders: **Parquet is 4.5× smaller than CSV and 13× smaller than JSON**. JSON repeats every column name on every row; Parquet stores each column together and compresses repeated values like `Dhaka`, `Delivered` and `Fabric` very well.

### Types survive (or don't)

```text
CSV     order_date: str | delivery_days: float64
Parquet order_date: datetime64[us] | delivery_days: float64
```

After a round trip through CSV, dates come back as **text** until you parse them again. Parquet stores the schema with the data, so dates stay dates.

### Read only the columns you need

```text
read 2 columns: CSV 10.5 ms | Parquet 3.8 ms
```

*(Timings depend on your machine.)* Parquet can read two columns without touching the others; a CSV has to be scanned in full. On millions of rows this is the difference between seconds and minutes (the DuckDB lesson in Phase 2 showed it at scale).

### Nested JSON → a flat table

APIs often nest objects and lists. `pd.json_normalize` flattens them:

```python
nested = [{"order_id": 1, "customer": {"id": "C010", "region": "Dhaka"}, "lines": [{"sku": "SKU-001", "qty": 120}]},
          {"order_id": 2, "customer": {"id": "C044", "region": "Gazipur"}, "lines": [{"sku": "SKU-005", "qty": 6000},
                                                                                       {"sku": "SKU-006", "qty": 900}]}]
print(pd.json_normalize(nested, record_path="lines", meta=["order_id", ["customer", "id"], ["customer", "region"]]))
```

```text
       sku   qty order_id customer.id customer.region
0  SKU-001   120        1        C010           Dhaka
1  SKU-005  6000        2        C044         Gazipur
2  SKU-006   900        2        C044         Gazipur
```

One row per order **line**, with the order's fields repeated: the grain changes from "order" to "order line", so be careful with sums afterwards.

## Choosing a format

| Situation | Choose |
|---|---|
| Raw API responses in a landing zone | JSON / JSON Lines (exactly as received) |
| Cleaned data for analysis or a data lake | **Parquet** |
| Sending a table to a business user | CSV or Excel |
| Appending events one at a time | JSON Lines |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Ignoring robots.txt and terms | Blocked IPs, legal risk | Check the rules; prefer APIs; go slowly |
| No delay between requests | You overload a small site | `time.sleep`; respect crawl delays |
| Assuming selectors never change | Scraper silently returns 0 rows | Validate counts and fields; alert on zero |
| CSV for pipeline storage | Lost types, slow reads, big files | Parquet |
| Summing after flattening nested lists | Order totals double-counted | Know your grain after `json_normalize` |

## Try it yourself

**Task:** Compare the scraped website prices (BDT) with `products_2025.csv` (list prices). Does every product match, and what exchange rate does the website imply?

<details markdown="1">
<summary>Show the solution</summary>

```python
prices = pd.read_csv("data/products_2025.csv")
check = catalog.merge(prices, on=["product", "category"], how="left")
check["implied_rate"] = (check["price_bdt"] / check["list_price"]).round(1)
print(check[["product", "list_price", "price_bdt", "implied_rate"]].head(4).to_string(index=False))
print("every product matched:", check["list_price"].notna().all(), "| rates:", sorted(float(x) for x in check["implied_rate"].unique()))
```

```text
     product  list_price  price_bdt  implied_rate
Cotton Twill         3.5      420.0         120.0
  Denim 12oz         5.2      624.0         120.0
Poplin White         2.9      348.0         120.0
 Jersey Knit         4.1      492.0         120.0
every product matched: True | rates: [120.0]
```

All 12 products match, and the website uses one consistent rate (120 BDT per unit of list price, the practice site's assumption). In real projects this kind of reconciliation between a scraped source and an internal file catches both scraper bugs and genuine price-list errors.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What should you check before scraping a website?

1. Nothing; public pages are free to scrape
2. robots.txt, the terms of service, and whether an API or download exists
3. Only the page speed

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why is Parquet much smaller than JSON for the same table?

1. It deletes rows
2. It stores and compresses each column together, without repeating column names on every row
3. It only stores numbers

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You save orders as CSV and read them back. What happens to the date column?

1. It stays a date
2. It comes back as text until you parse it
3. It disappears

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Scrape only when allowed: robots.txt, terms, a real User-Agent, delays; prefer APIs.
- Beautiful Soup + CSS selectors extract values; validate counts so layout changes don't fail silently.
- `pd.json_normalize` flattens nested JSON; watch the new grain.
- **Parquet** for pipelines (small, fast, typed); JSON for raw API data; CSV for people.

!!! job "Job-ready check"
    **Interview question:** *"Why do data lakes store data as Parquet rather than CSV?"*

    **Strong answer:** "Parquet is columnar and compressed, so files are several times smaller and queries can read only the columns and row groups they need. It also stores the schema, so types like dates and decimals survive. CSV is still useful for exchanging small tables with people, and raw API responses are often kept as JSON for traceability."

    **Mini project:** Scrape the practice catalogue daily into `catalog_YYYY-MM-DD.parquet`, then write a script that compares two days and lists price and stock changes.
