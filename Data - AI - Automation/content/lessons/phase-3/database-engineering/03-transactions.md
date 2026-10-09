---
title: "Transactions: All or Nothing, Even When Things Go Wrong"
order: 3
summary: "Use transactions so multi-step changes either fully happen or not at all, let constraints stop impossible updates, and prevent lost updates when two sessions change the same row — with BEGIN, COMMIT, ROLLBACK and SELECT … FOR UPDATE."
level: Intermediate
time: "45 min"
topics: ["Transactions"]
prerequisites: ["phase-3/database-engineering/01-postgresql-normalization"]
keywords: [transaction, acid, atomicity, consistency, isolation, durability, begin, commit transaction, rollback, savepoint, lost update, concurrency, race condition, row lock, select for update, lock timeout, isolation level, read committed, psycopg, idempotent]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Tutorial: Transactions"
    url: "https://www.postgresql.org/docs/current/tutorial-transactions.html"
    source: "PostgreSQL official docs"
    note: "BEGIN, COMMIT, ROLLBACK and savepoints with a bank-transfer example."
  - title: "Transaction Isolation"
    url: "https://www.postgresql.org/docs/current/transaction-iso.html"
    source: "PostgreSQL official docs"
    note: "Read Committed, Repeatable Read and Serializable explained."
  - title: "Transactions management (psycopg 3)"
    url: "https://www.psycopg.org/psycopg3/docs/basic/transactions.html"
    source: "psycopg official docs"
    note: "How Python connections start, commit and roll back transactions."
---

## What is it?

A **transaction** groups several database changes into one unit: either **all** of them are saved (`COMMIT`) or **none** are (`ROLLBACK`). Databases guarantee four properties, **ACID**:

| Property | Promise | In this lesson |
|---|---|---|
| **Atomicity** | All or nothing | A failed transfer leaves no half-move |
| **Consistency** | Rules (constraints) always hold | Stock can never go negative |
| **Isolation** | Concurrent transactions don't corrupt each other | Two shipments don't lose an update |
| **Durability** | Once committed, it survives crashes | (Handled by PostgreSQL's write-ahead log) |

!!! job "Why it matters at work"
    Pipelines fail halfway: a network drops, a file is malformed, a server restarts. Without transactions you get half-loaded tables and totals that don't reconcile. And when jobs or users run at the same time, missing locks cause "lost updates" that are almost impossible to find later. Every data and backend engineer needs these basics.

The script is `08_transactions.py`. It creates a small `shop.stock` table: Denim 12oz in two warehouses.

```text
start                                  {'Chattogram': 100, 'Dhaka': 500} | total 600
```

## Part 1: atomicity — a transfer is two updates

```python
def transfer(units: int, fail_halfway: bool = False):
    with psycopg.connect(DSN) as conn:               # the with-block = one transaction: commit or roll back
        conn.execute("UPDATE shop.stock SET units = units - %s WHERE warehouse = 'Dhaka'", [units])
        if fail_halfway:
            raise ConnectionError("network dropped after the first UPDATE")
        conn.execute("UPDATE shop.stock SET units = units + %s WHERE warehouse = 'Chattogram'", [units])


transfer(200)
transfer(50, fail_halfway=True)
```

```text
after transferring 200                 {'Chattogram': 300, 'Dhaka': 300} | total 600
error: network dropped after the first UPDATE
after a failed transfer (rolled back)  {'Chattogram': 300, 'Dhaka': 300} | total 600
```

The second transfer took 50 units out of Dhaka, then crashed. Because both updates were in **one transaction**, PostgreSQL rolled back the first update too: total stock is still 600. With psycopg, a `with psycopg.connect(...)` block commits if it finishes normally and **rolls back on an exception**.

In plain SQL the same thing looks like this:

```sql
BEGIN;
UPDATE shop.stock SET units = units - 200 WHERE warehouse = 'Dhaka';
UPDATE shop.stock SET units = units + 200 WHERE warehouse = 'Chattogram';
COMMIT;            -- or ROLLBACK; to undo both
```

`%s` placeholders pass values **separately** from the SQL. Never build SQL with f-strings from user input: that's how SQL injection happens.

## Part 2: consistency — constraints stop impossible changes

```python
transfer(1000)                                   # Dhaka only has 300 -> units would go negative
```

```text
rejected: new row for relation "stock" violates check constraint "stock_units_check"
after an impossible transfer           {'Chattogram': 300, 'Dhaka': 300} | total 600
```

The table has `CHECK (units >= 0)`. The first update would have made Dhaka −700, so the **whole** transaction is rejected. The rule is enforced by the database, whichever program sends the update.

## Part 3: isolation — the lost update

Two people ship from Chattogram at the same time. Each one's code **reads** the stock, subtracts in Python, and **writes** the result back:

```python
units_a = a.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram'").fetchone()[0]
units_b = b.execute("SELECT units FROM shop.stock WHERE warehouse = 'Chattogram'").fetchone()[0]
a.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_a - 30])   # A ships 30
a.commit()
b.execute("UPDATE shop.stock SET units = %s WHERE warehouse = 'Chattogram'", [units_b - 20])   # B ships 20
b.commit()
```

```text
two shipments (30 + 20), naive code    {'Chattogram': 280, 'Dhaka': 300} | total 580
  expected Chattogram: 250 -> 30 units were 'lost'
```

Both read 300. A wrote 270, then B wrote 280 over it. **A's shipment vanished from the books**, with no error anywhere. This is a **race condition**, and it gets more likely as traffic grows.

### Fix 1: let the database do the arithmetic

```sql
UPDATE shop.stock SET units = units - 30 WHERE warehouse = 'Chattogram';
```

One statement reads and writes in one step; PostgreSQL makes concurrent updates of the same row wait for each other.

### Fix 2: lock the row while you decide (`SELECT … FOR UPDATE`)

When your code must read, think, then write:

```python
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
```

```text
B had to wait: the row is locked by A (timed out after 2 s)
same shipments with FOR UPDATE         {'Chattogram': 250, 'Dhaka': 300} | total 550
```

`FOR UPDATE` locks the row until A commits. B **waits** (here, for demonstration, it gives up after 2 seconds and tries again) and then reads the up-to-date value: 300 − 30 − 20 = **250**. Correct.

| Isolation level (PostgreSQL) | You get | Use |
|---|---|---|
| **Read Committed** (default) | Each statement sees data committed before it started | Most work; add `FOR UPDATE` for read-then-write |
| **Repeatable Read** | The whole transaction sees one snapshot | Consistent multi-query reports |
| **Serializable** | As if transactions ran one at a time; may raise errors you must retry | Strict correctness, e.g. finance |

## Transactions in data pipelines

- Load a batch into a table **inside one transaction**, so readers never see half a load.
- Or load into a new table and **swap** it in at the end (also atomic).
- Combine with **idempotent** logic (safe to re-run), as in the SCD lesson. If a job dies, just run it again.
- Keep transactions **short**: long-open transactions hold locks and block other work.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Autocommit on multi-step changes | Half-finished updates after a crash | One transaction per logical change |
| Read in Python, write back a computed value | Lost updates under concurrency | `SET x = x - n`, or `SELECT … FOR UPDATE` |
| Building SQL with f-strings | SQL injection, quoting bugs | Parameters (`%s`) |
| Long transactions (e.g. waiting on user input) | Locks block everyone else | Do slow work before `BEGIN`; commit quickly |
| Swallowing errors without rollback | The connection stays in a failed transaction | Roll back (or use `with` blocks that do it) |

## Try it yourself

**Task:** Move 100 units from Dhaka to Chattogram in **one SQL statement** that only does anything if Dhaka has at least 100 units.

<details markdown="1">
<summary>Show a hint</summary>

A data-modifying CTE: `WITH take AS (UPDATE … RETURNING …) UPDATE … WHERE EXISTS (SELECT 1 FROM take)`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
WITH take AS (UPDATE shop.stock SET units = units - 100
              WHERE warehouse = 'Dhaka' AND units >= 100 RETURNING 100 AS n)
UPDATE shop.stock SET units = units + (SELECT n FROM take)
WHERE warehouse = 'Chattogram' AND EXISTS (SELECT 1 FROM take)
RETURNING units;
```

```text
moved 100 in one statement: True
final                                  {'Chattogram': 350, 'Dhaka': 200} | total 550
```

One statement = one transaction, with the database doing all the arithmetic. If Dhaka had fewer than 100 units, the first UPDATE would return nothing and the second would do nothing.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A job updates two tables and crashes after the first. With both updates in one transaction, what happens?

1. The first update stays
2. Both updates are rolled back
3. The database repairs the second update

<details markdown="1"><summary>Show answer</summary>
**B.** Atomicity.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Two sessions read stock = 300, subtract in Python and write back. What can go wrong?

1. Nothing
2. A lost update: one session overwrites the other's change
3. A syntax error

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `SELECT … FOR UPDATE` do?

1. Updates the row immediately
2. Locks the selected rows until the transaction ends, so other writers wait
3. Copies the table

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- A **transaction** is all-or-nothing: `BEGIN` … `COMMIT` / `ROLLBACK`. psycopg's `with connect()` commits, or rolls back on errors.
- **Constraints** make impossible states impossible, for every client.
- Avoid **lost updates**: do arithmetic in SQL (`units = units - n`) or lock with `SELECT … FOR UPDATE`.
- In pipelines: atomic loads, idempotent jobs, short transactions, parameters instead of string-built SQL.

!!! job "Job-ready check"
    **Interview question:** *"What does ACID mean, and how does it help a data pipeline?"*

    **Strong answer:** "Atomicity, consistency, isolation and durability. For a pipeline, atomicity means a batch load either fully appears or not at all, so a crash never leaves half-loaded data; consistency means constraints still hold; isolation means readers don't see a load in progress and concurrent writers don't lose updates; durability means committed loads survive restarts. I combine that with idempotent jobs so a failed run can simply be re-run."

    **Mini project:** Write `reserve_stock(order_id, warehouse, units)` that, in one transaction, locks the stock row, checks availability, decrements it and inserts a reservation row, and run it from two Python processes at once to show no lost updates.
