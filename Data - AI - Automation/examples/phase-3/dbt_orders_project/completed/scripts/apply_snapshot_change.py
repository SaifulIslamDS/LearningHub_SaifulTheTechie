from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "seeds" / "customers_2025.csv"
df = pd.read_csv(path)
mask = df["customer_id"].eq("C007")
if mask.sum() != 1:
    raise SystemExit("Expected exactly one C007 row")
old = int(df.loc[mask, "credit_days"].iloc[0])
df.loc[mask, "credit_days"] = 45
df.to_csv(path, index=False, lineterminator="\n")
print(f"C007 credit_days: {old} -> 45")
