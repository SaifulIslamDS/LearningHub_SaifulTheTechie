#!/usr/bin/env python3
"""
Generate the Phase 2 (Data Science) practice datasets.

    python tools/make_phase2_data.py            # writes content/downloads/phase-2/ and examples/phase-2/data/
    python tools/make_phase2_data.py --big 2000000 --out orders_big.parquet   # large local file (not shipped)

The data is SYNTHETIC: a textile-supplies wholesaler in Bangladesh, calendar
year 2025, built with a fixed random seed so every learner gets identical
files. Patterns are planted on purpose so the lessons have something real to
find (seasonality, a Friday weekend, region delivery times, an Eid dip,
cancellation drivers, a confounded "portal" effect and an A/B test).
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "downloads" / "phase-2"
EXAMPLES_DATA = ROOT / "examples" / "phase-2" / "data"      # same files, bundled with the lesson scripts
SEED = 2025

REGIONS = ["Dhaka", "Chattogram", "Gazipur", "Narayanganj", "Khulna"]
REGION_W = [0.34, 0.22, 0.20, 0.14, 0.10]
REGION_DAYS = {"Dhaka": 2.0, "Gazipur": 2.5, "Narayanganj": 2.5, "Chattogram": 4.0, "Khulna": 5.0}
SEGMENTS = ["Garment Factory", "Knitting Mill", "Trader", "Retailer"]
SEGMENT_W = [0.35, 0.20, 0.25, 0.20]
SEGMENT_SIZE = {"Garment Factory": 2.2, "Knitting Mill": 1.6, "Trader": 1.0, "Retailer": 0.45}

PRODUCTS = [  # product, category, list price, unit cost, base quantity
    ("Cotton Twill", "Fabric", 3.50, 2.60, 220),
    ("Denim 12oz", "Fabric", 5.20, 3.90, 180),
    ("Poplin White", "Fabric", 2.90, 2.10, 260),
    ("Jersey Knit", "Fabric", 4.10, 3.00, 200),
    ("Metal Buttons", "Trims", 0.04, 0.025, 6000),
    ("Zippers", "Trims", 0.30, 0.19, 1200),
    ("Elastic Tape", "Trims", 0.12, 0.08, 2500),
    ("Woven Labels", "Trims", 0.06, 0.035, 5000),
    ("Cotton Yarn 30s", "Yarn", 2.90, 2.20, 320),
    ("Polyester Yarn", "Yarn", 2.10, 1.55, 380),
    ("Viscose Yarn", "Yarn", 3.30, 2.45, 240),
    ("Sewing Thread", "Yarn", 0.85, 0.55, 900),
]

FIRST = ["Rahim", "Karim", "Nova", "Delta", "Sun", "Blue", "Green", "Star", "Crescent", "Padma", "Meghna", "Jamuna",
         "Royal", "Prime", "Unique", "Asian", "Bengal", "Golden", "Silver", "Ocean"]
LAST = {"Garment Factory": ["Garments", "Apparel", "Fashion", "Wear"], "Knitting Mill": ["Knit", "Knitwear", "Knitting"],
        "Trader": ["Traders", "Enterprise", "Trading"], "Retailer": ["Cloth Store", "Tailors", "Boutique"]}


def make_customers(rng) -> pd.DataFrame:
    rows, used = [], set()
    for i in range(1, 61):
        seg = rng.choice(SEGMENTS, p=SEGMENT_W)
        while True:
            name = f"{rng.choice(FIRST)} {rng.choice(LAST[seg])}"
            if name not in used:
                used.add(name)
                break
        credit = int(rng.choice([0, 15, 30, 60], p=[0.25, 0.30, 0.30, 0.15]))
        signup = date(2021, 1, 1) + timedelta(days=int(rng.integers(0, 1460)))
        rows.append({"customer_id": f"C{i:03d}", "customer_name": name, "segment": seg,
                     "region": rng.choice(REGIONS, p=REGION_W), "signup_date": signup.isoformat(),
                     "credit_days": credit, "size": SEGMENT_SIZE[seg] * float(rng.lognormal(0, 0.35))})
    return pd.DataFrame(rows)


def day_weight(d: date) -> float:
    w = 1.0
    if d.weekday() == 4:          # Friday: weekend in Bangladesh
        return 0.05
    if d.weekday() == 5:          # Saturday: half day
        w *= 0.55
    # season: export peak Sep–Nov, slow Jan–Feb
    w *= {1: 0.80, 2: 0.82, 3: 0.95, 4: 0.85, 5: 1.00, 6: 0.90, 7: 1.00, 8: 1.10, 9: 1.30, 10: 1.40, 11: 1.35, 12: 1.05}[d.month]
    # Eid holidays 2025 (approximate dates): Eid al-Fitr ~31 Mar, Eid al-Adha ~7 Jun
    for eid in (date(2025, 3, 31), date(2025, 6, 7)):
        if -2 <= (d - eid).days <= 6:
            w *= 0.15
    return w


def make_orders(rng, customers: pd.DataFrame) -> pd.DataFrame:
    days = [date(2025, 1, 1) + timedelta(days=i) for i in range(365)]
    weights = np.array([day_weight(d) for d in days])
    n_per_day = rng.poisson(weights * 14.5)
    cust_p = customers["size"].to_numpy() / customers["size"].sum()
    rows, oid = [], 10001
    for d, n in zip(days, n_per_day):
        for _ in range(int(n)):
            c = customers.iloc[rng.choice(len(customers), p=cust_p)]
            prod, cat, price, cost, base_q = PRODUCTS[rng.integers(len(PRODUCTS))]
            qty = max(1, int(round(base_q * SEGMENT_SIZE[c["segment"]] * rng.lognormal(0, 0.55))))
            if rng.random() < 0.006:                       # occasional bulk order (real, not an error)
                qty *= 8
            # channel: factories and mills use the portal more (planted confounder)
            p_portal = {"Garment Factory": 0.62, "Knitting Mill": 0.50, "Trader": 0.25, "Retailer": 0.15}[c["segment"]]
            r = rng.random()
            channel = "Portal" if r < p_portal else ("Sales rep" if r < p_portal + (1 - p_portal) * 0.6 else "Phone")
            discount = float(rng.choice([0, 0.02, 0.05, 0.08], p=[0.55, 0.20, 0.18, 0.07]))
            if qty * price > 1500:
                discount = max(discount, 0.05)
            unit_price = round(price * float(rng.normal(1, 0.03)), 3 if price < 1 else 2)
            value = qty * unit_price * (1 - discount)
            # cancellation risk: long credit, retailers, phone orders, very large orders
            logit = -3.4 + 0.022 * c["credit_days"] + (0.7 if c["segment"] == "Retailer" else 0) \
                + (0.45 if channel == "Phone" else 0) + (0.6 if value > 3000 else 0)
            cancelled = rng.random() < 1 / (1 + np.exp(-logit))
            promised = {"Dhaka": 3, "Gazipur": 3, "Narayanganj": 3, "Chattogram": 5, "Khulna": 6}[c["region"]]
            if cancelled:
                status, ddays = "Cancelled", np.nan
            elif d >= date(2025, 12, 24):
                status, ddays = ("Pending" if rng.random() < 0.5 else "Shipped"), np.nan
            else:
                status = "Delivered"
                ddays = max(1, int(round(rng.gamma(4, REGION_DAYS[c["region"]] / 4) + (1.5 if d.month in (10, 11) else 0))))
            rows.append({"order_id": oid, "order_date": d.isoformat(), "customer_id": c["customer_id"],
                         "region": c["region"], "segment": c["segment"], "channel": channel, "category": cat,
                         "product": prod, "quantity": qty, "unit_price": unit_price, "discount": discount,
                         "unit_cost": cost, "status": status, "promised_days": promised, "delivery_days": ddays})
            oid += 1
    df = pd.DataFrame(rows)
    df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
    return df


def make_raw(rng, orders: pd.DataFrame) -> pd.DataFrame:
    """The messy export used in the pandas cleaning lesson."""
    raw = orders.drop(columns=["revenue", "unit_cost"]).copy()
    raw["delivery_days"] = raw["delivery_days"].astype("Float64")
    idx = rng.choice(raw.index, size=40, replace=False)
    raw.loc[idx, "region"] = raw.loc[idx, "region"].str.upper() + " "          # DHAKA_
    idx = rng.choice(raw.index, size=30, replace=False)
    raw.loc[idx, "status"] = " " + raw.loc[idx, "status"].str.lower()          # _delivered
    price_typos = rng.choice(raw.index[raw["unit_price"] > 1], size=3, replace=False)
    raw.loc[price_typos, "unit_price"] = raw.loc[price_typos, "unit_price"] * 100   # 3.50 -> 350
    neg = rng.choice(raw.index, size=2, replace=False)
    raw.loc[neg, "quantity"] = -raw.loc[neg, "quantity"]
    raw["quantity"] = raw["quantity"].astype(object)
    big = raw.index[raw["quantity"].astype(int) >= 1000]
    commas = rng.choice(big, size=25, replace=False)
    raw.loc[commas, "quantity"] = raw.loc[commas, "quantity"].map(lambda q: f"{int(q):,}")
    dup = raw.loc[rng.choice(raw.index, size=18, replace=False)]
    raw = pd.concat([raw, dup]).sort_values("order_id", kind="stable").reset_index(drop=True)
    raw = raw.rename(columns={"order_id": "Order ID", "order_date": "Order Date", "customer_id": "Customer ID",
                              "region": "Region", "segment": "Segment", "channel": "Channel", "category": "Category",
                              "product": "Product", "quantity": "Qty", "unit_price": "Unit Price",
                              "discount": "Discount", "status": "Status", "promised_days": "Promised Days",
                              "delivery_days": "Delivery Days"})
    return raw


def make_ab(rng) -> pd.DataFrame:
    """Portal checkout experiment, 1–28 Nov 2025: A = current checkout, B = one-page checkout."""
    rows, sid = [], 500001
    start = date(2025, 11, 1)
    for i in range(28):
        d = start + timedelta(days=i)
        n = int(rng.poisson(430 if d.weekday() != 4 else 120))
        for _ in range(n):
            variant = "A" if rng.random() < 0.5 else "B"
            device = "mobile" if rng.random() < 0.58 else "desktop"
            new = rng.random() < 0.30
            p = 0.080 + (0.012 if variant == "B" else 0) - (0.020 if device == "mobile" else 0) - (0.015 if new else 0)
            conv = rng.random() < p
            value = round(float(rng.lognormal(np.log(620), 0.6)), 2) if conv else 0.0
            rows.append({"session_id": sid, "date": d.isoformat(), "variant": variant, "device": device,
                         "new_customer": int(new), "converted": int(conv), "order_value": value})
            sid += 1
    return pd.DataFrame(rows)


def make_big(n: int, out: Path):
    rng = np.random.default_rng(SEED + 1)
    days = pd.date_range("2021-01-01", "2025-12-31", freq="D")
    prods = np.array([p[0] for p in PRODUCTS])
    prices = np.array([p[2] for p in PRODUCTS])
    pi = rng.integers(0, len(PRODUCTS), n)
    df = pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "order_date": days[rng.integers(0, len(days), n)],
        "customer_id": np.char.add("C", np.char.zfill(rng.integers(1, 2001, n).astype(str), 4)),
        "region": rng.choice(REGIONS, n, p=REGION_W),
        "product": prods[pi],
        "quantity": np.maximum(1, rng.lognormal(5.5, 0.9, n).round()).astype("int64"),
        "unit_price": (prices[pi] * rng.normal(1, 0.03, n)).round(3),
        "status": rng.choice(["Delivered", "Shipped", "Cancelled"], n, p=[0.90, 0.04, 0.06]),
    })
    if out.suffix == ".parquet":
        df.to_parquet(out, index=False)
    else:
        df.to_csv(out, index=False)
    print(f"Wrote {out} ({n:,} rows, {out.stat().st_size / 1e6:.1f} MB)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--big", type=int, help="also write a large synthetic file with this many rows")
    ap.add_argument("--out", default="orders_big.parquet", help="file for --big (.parquet or .csv)")
    a = ap.parse_args()
    if a.big:
        make_big(a.big, Path(a.out))
        return
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    customers = make_customers(rng)
    orders = make_orders(rng, customers)
    raw = make_raw(rng, orders)
    # three new December sign-ups with no orders yet (used in the anti-join example)
    new = pd.DataFrame([
        {"customer_id": "C061", "customer_name": "Lotus Knitwear", "segment": "Knitting Mill", "region": "Gazipur",
         "signup_date": "2025-12-08", "credit_days": 30, "size": 0.0},
        {"customer_id": "C062", "customer_name": "Padma Boutique", "segment": "Retailer", "region": "Khulna",
         "signup_date": "2025-12-15", "credit_days": 0, "size": 0.0},
        {"customer_id": "C063", "customer_name": "Harbor Trading", "segment": "Trader", "region": "Chattogram",
         "signup_date": "2025-12-21", "credit_days": 15, "size": 0.0},
    ])
    customers = pd.concat([customers, new], ignore_index=True)
    ab = make_ab(rng)
    customers.drop(columns="size").to_csv(OUT / "customers_2025.csv", index=False)
    pd.DataFrame([{"product": p, "category": c, "list_price": lp, "unit_cost": uc} for p, c, lp, uc, _ in PRODUCTS]) \
        .to_csv(OUT / "products_2025.csv", index=False)
    orders.to_csv(OUT / "orders_2025.csv", index=False)
    raw.to_csv(OUT / "orders_2025_raw.csv", index=False)
    ab.to_csv(OUT / "ab_test_checkout.csv", index=False)
    EXAMPLES_DATA.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.csv"):
        (EXAMPLES_DATA / f.name).write_bytes(f.read_bytes())
    print(f"customers {len(customers)}, orders {len(orders)}, raw {len(raw)}, ab sessions {len(ab)}")
    print(orders["status"].value_counts().to_dict())
    print("revenue (excl. cancelled):", round(orders.loc[orders.status != "Cancelled", "revenue"].sum(), 2))


if __name__ == "__main__":
    main()
