---
title: "REST APIs, Authentication & Pagination: Pull Data Like a Pro"
order: 1
summary: "Call a REST API from Python with a token, follow pagination to the last page, retry politely on rate limits, save the raw responses, and load only what changed — against a practice API on your own machine."
level: Intermediate
time: "55 min"
topics: ["REST APIs", "Auth & pagination"]
prerequisites: ["phase-0/programming-refresher/03-files-exceptions", "phase-2/pandas/01-dataframe-basics"]
keywords: [rest api, api, http, get, json, endpoint, status code, requests, session, authentication, bearer token, api key, authorization header, pagination, next link, page size, rate limit, 429, retry-after, backoff, timeout, incremental load, landing zone, secrets, environment variable]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Requests: Quickstart"
    url: "https://requests.readthedocs.io/en/latest/user/quickstart/"
    source: "Requests official docs"
    note: "GET, parameters, headers, JSON, timeouts and errors."
  - title: "HTTP response status codes"
    url: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"
    source: "MDN Web Docs"
    note: "What 200, 401, 404, 429 and 503 mean."
  - title: "Retry-After header"
    url: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After"
    source: "MDN Web Docs"
    note: "How servers tell clients when to try again."
---

## What is it?

- A **REST API** is a set of web addresses (**endpoints**) that return data, usually as **JSON**, when you send an HTTP request such as `GET /api/v1/orders`.
- **Authentication** proves who you are, usually with an **API key** or **token** in a request header (`Authorization: Bearer <token>`).
- **Pagination** splits big results into pages; your code must keep asking for the next page until there are no more.

```text
your script ──GET /api/v1/orders?page=1  (Authorization: Bearer …)──►  API
            ◄── 200 {"data": [500 orders], "next": "/api/v1/orders?page=2", "total": 4246}
            ──GET page=2 … page=9 ──►   (sometimes: 429 Too Many Requests → wait, retry)
```

!!! job "Why it matters at work"
    Most company data lives in SaaS tools (CRM, ERP, e-commerce, ads, payments) that you can only reach through their APIs. Data engineers write and maintain these connectors, and the classic failures are exactly what this lesson covers: an expired token, a forgotten last page, a rate limit, or a silent partial load.

Start the practice API (`uv run mock_api.py`) in one terminal, then run `01_api_ingest.py` in another. The practice API serves the 4,246 orders from Phase 2, requires a token, pages its results and rate-limits every 5th request, like real APIs do.

## Step 1: a request without and with a token

```python
import requests

r = requests.get(f"{BASE}/api/v1/orders", params={"page_size": 2}, timeout=10)
print(r.status_code, r.json())

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"})
r = session.get(f"{BASE}/api/v1/orders", params={"page_size": 2}, timeout=10)
body = r.json()
print(r.status_code, {k: body[k] for k in ["page", "page_size", "total", "total_pages", "next"]})
print(body["data"][0])
```

```text
401 {'error': 'missing or invalid token'}
200 {'page': 1, 'page_size': 2, 'total': 4246, 'total_pages': 2123, 'next': '/api/v1/orders?page=2&page_size=2'}
{'order_id': 10001, 'order_date': '2025-01-01', 'customer_id': 'C042', 'region': 'Chattogram', 'segment': 'Knitting Mill', 'channel': 'Phone', 'category': 'Trims', 'product': 'Metal Buttons', 'quantity': 4616, 'unit_price': 0.041, 'discount': 0.0, 'unit_cost': 0.025, 'status': 'Delivered', 'promised_days': 5, 'delivery_days': 3, 'revenue': 189.26}
```

- `params=` builds the query string (`?page_size=2`), so you don't have to.
- A **Session** reuses the connection and sends the same headers with every request.
- **Always set `timeout=`.** Without it, a hung server can freeze your pipeline forever.

| Status | Meaning | What your code should do |
|---|---|---|
| **200** | OK | Use the data |
| **400** | Bad request (your parameters) | Fix the code; don't retry |
| **401 / 403** | Not authenticated / not allowed | Check the token or permissions; don't retry |
| **404** | Not found | Check the URL; don't retry |
| **429** | Too many requests | Wait (`Retry-After`), then retry |
| **500–503** | Server problem | Retry with increasing waits, then fail loudly |

!!! warning "Keep tokens out of code"
    The script reads the token from an environment variable (`ORDERS_API_TOKEN`). Real tokens go in environment variables or a secrets manager, never in code, notebooks or Git.

## Step 2: a polite GET with retries

```python
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
```

- Retry only **temporary** problems (429, 5xx). Retrying a 401 just hammers the server.
- Respect `Retry-After` when the server sends it; otherwise use **exponential back-off** (2, 4, 8… seconds).
- After a few attempts, **fail loudly**. A pipeline that silently gives up is worse than one that crashes.

## Step 3: follow pagination to the end, and save the raw pages

```python
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
```

```text
page 1/9: 500 rows
page 2/9: 500 rows
  429 on attempt 1; waiting 1s
page 3/9: 500 rows
page 4/9: 500 rows
page 5/9: 500 rows
page 6/9: 500 rows
  429 on attempt 1; waiting 1s
page 7/9: 500 rows
page 8/9: 500 rows
page 9/9: 246 rows
(4246, 16) | net revenue: 5478357.79
```

*(Where the 429s appear depends on how many requests the practice API has already served.)*

Four professional habits in one function:

1. **Follow `next` until it's empty**, rather than guessing the number of pages.
2. **Save every raw response** in a *landing zone* (`landing/orders/page-001.json` …) before transforming anything. If your parsing has a bug, you can reprocess without calling the API again.
3. **Reconcile:** compare your row count with the API's `total`. The net revenue matches the Phase 2 known answer (5,478,357.79).
4. Survive rate limits: two 429s, two polite waits, no data lost.

| Pagination style | Looks like | Watch out for |
|---|---|---|
| **Page number** | `?page=3&page_size=500` | Rows inserted while you read can shift pages |
| **Offset/limit** | `?offset=1000&limit=500` | Same; slow on huge offsets |
| **Cursor** | `?cursor=eyJpZCI6MTAwfQ` (from the last response) | Most robust; just pass the cursor back |
| **Next link** | `"next": "/orders?page=2"` (or a `Link` header) | Simplest: follow it until null |

## Step 4: incremental loads

A daily job shouldn't download a whole year every day. Ask only for what changed:

```python
recent = ingest_orders(since="2025-12-01")
print(len(recent), "orders since 2025-12-01")
```

```text
page 1/1: 396 rows
396 orders since 2025-12-01
```

In production you store the **high-water mark** (the latest date or ID you've loaded) and start the next run from there. Real APIs usually filter on `updated_since`, so that corrected old orders are picked up too. Incremental loads come back in Phase 3B (ETL/ELT).

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| No `timeout=` | The job hangs forever on a stuck connection | Always pass a timeout |
| Reading only page 1 | Silently missing 90% of the data | Follow `next` / cursor; check against `total` |
| Retrying every error | 401s hammer the API; your key gets blocked | Retry only 429 and 5xx, with back-off |
| Token in the code or notebook | Leaked credentials in Git | Environment variables or a secrets manager |
| Transforming before saving | A parsing bug means re-calling the API | Land raw responses first |

## Try it yourself

**Task:** The API also has `/api/v1/customers`. Ingest it with `get_json`, then join the customers' `credit_days` onto the orders. How many orders have no matching customer?

<details markdown="1">
<summary>Show the solution</summary>

```python
customers = pd.DataFrame(get_json(f"{BASE}/api/v1/customers")["data"])
merged = orders.merge(customers[["customer_id", "credit_days"]], on="customer_id", how="left", validate="many_to_one")
print(customers.shape, "| orders without a customer match:", merged["credit_days"].isna().sum())
```

```text
  429 on attempt 1; waiting 1s
(63, 6) | orders without a customer match: 0
```

All 4,246 orders match one of the 63 customers, and `validate="many_to_one"` would have raised an error if a customer appeared twice. Notice that the retry logic handled another rate limit without you thinking about it: that's why it lives in one shared function.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. An API returns status 429. What should your code do?

1. Stop and report a bug
2. Wait (respecting `Retry-After`) and retry
3. Retry immediately in a tight loop

<details markdown="1"><summary>Show answer</summary>
**B.** 429 = too many requests: a temporary condition.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why save raw API responses before transforming them?

1. JSON is smaller than Parquet
2. You can reprocess after a bug without calling the API again, and you keep evidence of what was received
3. APIs require it

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Where should an API token be stored?

1. In the script, so it always works
2. In an environment variable or secrets manager
3. In the README

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Use `requests.Session` with an `Authorization` header, `params=` and a **timeout**.
- Handle status codes deliberately: retry **429/5xx** with back-off; fail fast on 4xx.
- Follow pagination until the end, **save raw pages** to a landing zone, and **reconcile counts** with the API's total.
- Load **incrementally** with a high-water mark; keep secrets out of code.

!!! job "Job-ready check"
    **Interview question:** *"How would you build a reliable daily extract from a third-party REST API?"*

    **Strong answer:** "A small client with a session, auth from a secrets store, timeouts, and retries with back-off only for 429 and 5xx. It follows pagination (preferably a cursor) to the end, lands the raw JSON with the run date before any transformation, reconciles the row count with the API's total, and requests only records updated since the last successful run. Failures alert someone instead of loading partial data."

    **Mini project:** Turn `ingest_orders` into a command-line tool (Phase 0 style) with `--since` and `--output`, logging, exit codes, and a pytest test that uses the practice API.
