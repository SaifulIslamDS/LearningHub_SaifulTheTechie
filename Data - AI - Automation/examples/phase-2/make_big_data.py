"""Create a large synthetic orders file for the "larger local data" lesson.

    uv run make_big_data.py                 # 2,000,000 rows -> data/orders_big.parquet and data/orders_big.csv
    uv run make_big_data.py 5000000         # choose your own size

Not included in the download because of its size. Same seed = same file for everyone.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
rng = np.random.default_rng(2026)
regions = ["Dhaka", "Chattogram", "Gazipur", "Narayanganj", "Khulna"]
products = ["Cotton Twill", "Denim 12oz", "Poplin White", "Jersey Knit", "Metal Buttons", "Zippers",
            "Elastic Tape", "Woven Labels", "Cotton Yarn 30s", "Polyester Yarn", "Viscose Yarn", "Sewing Thread"]
prices = np.array([3.50, 5.20, 2.90, 4.10, 0.04, 0.30, 0.12, 0.06, 2.90, 2.10, 3.30, 0.85])
days = pd.date_range("2021-01-01", "2025-12-31", freq="D")
pi = rng.integers(0, len(products), n)
df = pd.DataFrame({
    "order_id": np.arange(1, n + 1),
    "order_date": days[rng.integers(0, len(days), n)],
    "customer_id": pd.Series(rng.integers(1, 2001, n)).map("C{:04d}".format),
    "region": rng.choice(regions, n, p=[0.34, 0.22, 0.20, 0.14, 0.10]),
    "product": np.array(products)[pi],
    "quantity": np.maximum(1, rng.lognormal(5.5, 0.9, n).round()).astype("int64"),
    "unit_price": (prices[pi] * rng.normal(1, 0.03, n)).round(3),
    "status": rng.choice(["Delivered", "Shipped", "Cancelled"], n, p=[0.90, 0.04, 0.06]),
})
out = Path(__file__).parent / "data"
df.to_parquet(out / "orders_big.parquet", index=False)
df.to_csv(out / "orders_big.csv", index=False)
for f in ("orders_big.csv", "orders_big.parquet"):
    print(f"{f}: {(out / f).stat().st_size / 1e6:.0f} MB")
print(f"{n:,} rows")
