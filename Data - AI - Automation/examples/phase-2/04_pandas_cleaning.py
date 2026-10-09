"""Phase 2 · pandas · Cleaning a messy export (orders_2025_raw.csv -> clean table)."""

# %% 1. Load the raw export and profile it
import pandas as pd

pd.set_option("display.width", 120)
raw = pd.read_csv("data/orders_2025_raw.csv")
print(raw.shape)
print(raw.dtypes[["Qty", "Unit Price", "Delivery Days"]])
print(raw["Region"].unique())
print(raw["Status"].value_counts())

# %% 2. Tidy column names
df = raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.rename(columns={"qty": "quantity"})
print(list(df.columns))

# %% 3. Clean text: spaces and capitals
df["region"] = df["region"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.title()
print(df["region"].value_counts())
print(df["status"].value_counts())

# %% 4. Numbers stored as text: "5,000" -> 5000
bad = pd.to_numeric(df["quantity"], errors="coerce").isna()
print(df.loc[bad, "quantity"].head(3).tolist(), bad.sum())
df["quantity"] = df["quantity"].str.replace(",", "", regex=False).astype("int64")
print(df["quantity"].dtype)

# %% 5. Duplicates
print(df.duplicated().sum(), "exact duplicate rows")
print(df["order_id"].duplicated().sum(), "duplicate order IDs")
df = df.drop_duplicates()
print(len(df), df["order_id"].is_unique)

# %% 6. Impossible values: negative quantities
print(df.loc[df["quantity"] <= 0, ["order_id", "product", "quantity"]])
df["quantity"] = df["quantity"].abs()          # assumption (confirmed with ERP owner): sign error

# %% 7. Outliers that are errors: price typed x100
median_price = df.groupby("product")["unit_price"].transform("median")
ratio = df["unit_price"] / median_price
print(df.loc[ratio > 10, ["order_id", "product", "unit_price"]].assign(median=median_price[ratio > 10]))
df.loc[ratio > 10, "unit_price"] = df.loc[ratio > 10, "unit_price"] / 100

# %% 8. Missing values: explain them, don't just fill them
print(df.isna().sum()[lambda s: s > 0])
print(df.loc[df["delivery_days"].isna(), "status"].value_counts())

# %% 9. Types, a derived column, and validation against the known clean file
df["order_date"] = pd.to_datetime(df["order_date"])
df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)

clean = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
cols = [c for c in df.columns]
check = clean[cols]
print(len(df) == len(check), df["order_id"].is_unique)
pd.testing.assert_frame_equal(df.reset_index(drop=True), check, check_dtype=False)
print("Cleaned data matches orders_2025.csv")
print(round(df.loc[df["status"] != "Cancelled", "revenue"].sum(), 2))

# %% Try it yourself — solution: a reusable cleaning function with checks
def clean_orders(path: str) -> pd.DataFrame:
    d = pd.read_csv(path)
    d.columns = d.columns.str.strip().str.lower().str.replace(" ", "_")
    d = d.rename(columns={"qty": "quantity"})
    for col in ["region", "status"]:
        d[col] = d[col].str.strip().str.title()
    d["quantity"] = d["quantity"].str.replace(",", "", regex=False).astype("int64").abs()
    d = d.drop_duplicates()
    med = d.groupby("product")["unit_price"].transform("median")
    d.loc[d["unit_price"] / med > 10, "unit_price"] /= 100
    d["order_date"] = pd.to_datetime(d["order_date"])
    d["revenue"] = (d["quantity"] * d["unit_price"] * (1 - d["discount"])).round(2)
    assert d["order_id"].is_unique, "duplicate order IDs"
    assert (d["quantity"] > 0).all(), "non-positive quantities"
    assert d["status"].isin(["Delivered", "Shipped", "Pending", "Cancelled"]).all(), "unknown status"
    return d


result = clean_orders("data/orders_2025_raw.csv")
print(result.shape, round(result.loc[result.status != "Cancelled", "revenue"].sum(), 2))
