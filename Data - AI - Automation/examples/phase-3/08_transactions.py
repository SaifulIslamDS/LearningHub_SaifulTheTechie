"""Phase 3 · Database engineering · Transactions (ACID), rollback and concurrent updates.

Needs PostgreSQL with the shop schema loaded (03_load_postgres.py) and:  uv add "psycopg[binary]"
"""
import os

import psycopg

DSN = os.environ.get("DATABASE_URL", "postgresql://postgres:practice@localhost:5432/postgres")

# %% 0. A small stock table: units of each product in two warehouses
with psycopg.connect(DSN, autocommit=True) as conn:
    conn.execute("DROP TABLE IF EXISTS shop.stock")
    conn.execute("""CREATE TABLE shop.stock (
        warehouse text, product text, units integer NOT NULL CHECK (units >= 0),
        PRIMARY KEY (warehouse, product))""")
    conn.execute("""INSERT INTO shop.stock VALUES
        ('Dhaka', 'Denim 12oz', 500), ('Chattogram', 'Denim 12oz', 100)""")


def show(label: str):
    with psycopg.connect(DSN) as c:
        rows = c.execute("SELECT warehouse, units FROM shop.stock ORDER BY warehouse").fetchall()
    print(f"{label:38s}", dict(rows), "| total", sum(u for _, u in rows))


show("start")


# %% 1. A transfer is TWO updates that must both happen, or neither (atomicity)
def transfer(units: int, fail_halfway: bool = False):
    with psycopg.connect(DSN) as conn:               # the with-block = one transaction: commit or roll back
        conn.execute("UPDATE shop.stock SET units = units - %s WHERE warehouse = 'Dhaka'", [units])
        if fail_halfway:
            raise ConnectionError("network dropped after the first UPDATE")
        conn.execute("UPDATE shop.stock SET units = units + %s WHERE warehouse = 'Chattogram'", [units])


transfer(200)
show("after transferring 200")
try:
    transfer(50, fail_halfway=True)
except ConnectionError as exc:
    print("error:", exc)
show("after a failed transfer (rolled back)")

# %% 2. Consistency: a constraint stops the whole transaction
try:
    transfer(1000)                                   # Dhaka only has 300 -> units would go negative
except psycopg.errors.CheckViolation as exc:
    print("rejected:", exc.diag.message_primary)
show("after an impossible transfer")

# %% 3. Concurrency: two sessions read-then-write the same row (the "lost update")
a, b = psycopg.connect(DSN), psycopg.connect(DSN)
units_a = a.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram'").fetchone()[0]
units_b = b.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram'").fetchone()[0]
a.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_a - 30])   # A ships 30
a.commit()
b.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_b - 20])   # B ships 20
b.commit()
show("two shipments (30 + 20), naive code")
print("  expected Chattogram:", units_a - 50, "-> 30 units were 'lost'")

# %% 4. The fix: let the database do the arithmetic, or lock the row with FOR UPDATE
with psycopg.connect(DSN) as c:
    c.execute("UPDATE shop.stock SET units = 300 WHERE warehouse = 'Chattogram'")
units_a = a.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram' FOR UPDATE").fetchone()[0]
b.execute("SET lock_timeout = '2s'")
try:
    b.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram' FOR UPDATE")   # waits for A's lock
except psycopg.errors.LockNotAvailable:
    print("B had to wait: the row is locked by A (timed out after 2 s)")
    b.rollback()
a.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_a - 30])
a.commit()                                           # A's lock is released here
units_b = b.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram' FOR UPDATE").fetchone()[0]
b.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_b - 20])
b.commit()
show("same shipments with FOR UPDATE")
a.close()
b.close()

# %% Try it yourself — solution: move 100 units in ONE statement, atomically, with a check
with psycopg.connect(DSN) as conn:
    moved = conn.execute("""
        WITH take AS (UPDATE shop.stock SET units = units - 100
                      WHERE warehouse = 'Dhaka' AND units >= 100 RETURNING 100 AS n)
        UPDATE shop.stock SET units = units + (SELECT n FROM take)
        WHERE warehouse = 'Chattogram' AND EXISTS (SELECT 1 FROM take)
        RETURNING units""").fetchone()
print("moved 100 in one statement:", moved is not None)
show("final")
