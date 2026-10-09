from pathlib import Path
import duckdb

db = Path(__file__).resolve().parents[1] / "data" / "phase3.duckdb"
con = duckdb.connect(str(db), read_only=True)
rows = con.sql("""
select customer_id, credit_days, dbt_valid_from, dbt_valid_to
from main_snapshots.customers_snapshot
where customer_id = 'C007'
order by dbt_valid_from
""").fetchall()
for row in rows:
    print(row)
