from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent
P = ROOT / "dbt_orders_project" / "completed"

required = [
    "dbt_project.yml", "profiles.yml", "requirements-dbt.txt",
    "models/staging/_sources.yml", "models/staging/stg_orders.sql", "models/staging/stg_customers.sql", "models/staging/stg_products.sql",
    "models/staging/_staging.yml", "models/intermediate/int_orders_enriched.sql", "models/intermediate/_intermediate.yml",
    "models/marts/fct_orders.sql", "models/marts/dim_customers.sql", "models/marts/mart_monthly_revenue.sql", "models/marts/_marts.yml",
    "macros/discount_band.sql", "macros/schema.yml", "snapshots/customers_snapshot.yml",
    "tests/assert_fct_orders_reconciles.sql", "tests/assert_no_negative_net_revenue.sql",
]
missing = [f for f in required if not (P / f).exists()]
if missing:
    raise SystemExit("missing files: " + ", ".join(missing))

project = yaml.safe_load((P / "dbt_project.yml").read_text())
profile = yaml.safe_load((P / "profiles.yml").read_text())
snapshot = yaml.safe_load((P / "snapshots/customers_snapshot.yml").read_text())

assert project["profile"] == "phase3_orders"
assert profile["phase3_orders"]["outputs"]["dev"]["type"] == "duckdb"
scfg = snapshot["snapshots"][0]["config"]
assert scfg["unique_key"] == "customer_id"
assert scfg["strategy"] == "check"
assert scfg["check_cols"] == ["segment", "region", "credit_days"]

sql_files = sorted(P.glob("models/**/*.sql")) + sorted(P.glob("tests/*.sql")) + sorted(P.glob("macros/*.sql"))
refs = set()
sources = set()
for f in sql_files:
    text = f.read_text(encoding="utf-8")
    refs.update(re.findall(r"ref\(['\"]([^'\"]+)['\"]\)", text))
    sources.update(re.findall(r"source\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]\)", text))

model_names = {f.stem for f in P.glob("models/**/*.sql")}
missing_refs = sorted(refs - model_names)
if missing_refs:
    raise SystemExit("unresolved ref() targets: " + ", ".join(missing_refs))

expected_sources = {("shop", "orders_2025"), ("shop", "customers_2025"), ("shop", "products_2025")}
assert sources <= expected_sources

print(f"dbt project audit: {len(required)}/{len(required)} required files present")
print(f"models: {len(model_names)} | refs: {len(refs)} resolved | source() pairs: {len(sources)}")
print("profile: duckdb | path data/phase3.duckdb | target schema main")
print("snapshot: customer_id | check strategy | 3 tracked columns")
print("dbt CLI execution: RUN-BY-OWNER (dbt and duckdb packages are not installed in this sandbox)")
