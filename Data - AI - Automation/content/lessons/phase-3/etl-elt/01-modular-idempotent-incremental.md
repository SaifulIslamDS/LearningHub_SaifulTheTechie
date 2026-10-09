---
title: "Modular, Idempotent Pipelines with Incremental Loads"
order: 1
summary: "Build a pipeline in small testable steps, load only new orders, and make retries safe without creating duplicates."
level: Intermediate
time: "45 min"
topics: ["Modular pipelines", "Idempotency", "Incremental loads"]
prerequisites: ["phase-3/data-ingestion/01-rest-apis-auth-pagination", "phase-3/lakehouse/01-delta-lake-medallion"]
keywords: [etl, elt, data pipeline, idempotent, idempotency, incremental load, watermark, upsert]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Incremental copy in Copy job"
    url: "https://learn.microsoft.com/en-us/fabric/data-factory/incremental-copy-job"
    source: "Microsoft Learn"
    note: "Current explanation of full vs incremental copy, watermarks and CDC."
  - title: "Incrementally load data from a source data store"
    url: "https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview"
    source: "Microsoft Learn"
    note: "Shows the common watermark pattern for database and file sources."
  - title: "Configure incremental models"
    url: "https://docs.getdbt.com/docs/build/incremental-models"
    source: "dbt Developer Hub"
    note: "Shows how warehouse transformations filter new or changed rows and use a unique key for updates."
---

## What is it?

A **data pipeline** is a repeatable sequence that moves and transforms data. A reliable pipeline is easier to operate when it is split into small **modules** with one clear job each:

1. **Extract** — read the source.
2. **Transform** — validate, clean and reshape.
3. **Load** — write to the target safely.

That is **ETL** when transformation happens before the target is loaded. In **ELT**, you extract and load first, then transform inside a warehouse or lakehouse. The choice changes *where* transformation happens, not the need for reliable steps.

For daily work, you usually do not want to reload every historical row. An **incremental load** moves only data that is new or changed since the last successful run. A **watermark** records where the last run stopped, such as the maximum date or update timestamp.

!!! job "Why it matters at work"
    Full reloads are simple but become slow and expensive as data grows. Incremental jobs are faster, but they introduce state: you must know what was already processed and make retries safe. Interviewers often ask how you would prevent a scheduled job from duplicating rows after a retry.

The script is `14_modular_incremental_pipeline.py`. It uses the 2025 order data and only `pandas`.

## Step 1: keep extract, transform and load separate

The extractor owns source filtering:

```python
def extract_orders(start_exclusive=None, end_inclusive=None):
    df = pd.read_csv(SOURCE, parse_dates=["order_date"])
    if start_exclusive:
        df = df[df["order_date"] > pd.Timestamp(start_exclusive)]
    if end_inclusive:
        df = df[df["order_date"] <= pd.Timestamp(end_inclusive)]
    return df.copy()
```

The transformer owns business and data-quality rules:

```python
def transform_orders(df):
    out = df.copy()
    if out["order_id"].duplicated().any():
        raise ValueError("source batch contains duplicate order_id values")
    if (out["quantity"] <= 0).any():
        raise ValueError("quantity must be positive")
    if out["status"].isna().any():
        raise ValueError("status must not be null")
    out["order_date"] = pd.to_datetime(out["order_date"]).dt.strftime("%Y-%m-%d")
    return out.sort_values("order_id").reset_index(drop=True)
```

The loader owns target-writing behaviour. Because each function has one purpose, you can test or replace it without rewriting the whole pipeline.

## Step 2: use a watermark for the incremental window

Our first run loads everything through 30 November. The second run starts *after* that watermark and loads December only:

```python
run_window("initial", None, "2025-11-30")
run_window("incremental", "2025-11-30", "2025-12-31")
```

Real output from the script:

```text
initial: extracted 3850 | target 3850 | watermark 2025-11-30
incremental: extracted 396 | target 4246 | watermark 2025-12-31
```

The **396 December orders** match the existing Phase 3A API-ingestion known answer. The important rule is: advance the stored watermark **only after the load succeeds**. If the job fails before completion, keep the old watermark and retry the same window.

A date works for this practice dataset because orders are historical and fixed. In a live source, prefer a reliable `updated_at`, sequence number, database change-tracking token or CDC position when updates can arrive for old dates.

## Step 3: make retries idempotent

**Idempotent** means: running the same job again gives the same final state as running it once.

An unsafe incremental loader simply appends rows. If a scheduler retries the December batch, you get duplicates. Instead, this loader uses `order_id` as the business key and keeps the newest copy:

```python
def load_upsert(batch):
    if TARGET.exists():
        current = pd.read_csv(TARGET)
        combined = pd.concat([current, batch], ignore_index=True)
    else:
        combined = batch.copy()

    combined = (
        combined.drop_duplicates(subset=["order_id"], keep="last")
                .sort_values("order_id")
                .reset_index(drop=True)
    )
    combined.to_csv(TARGET, index=False, lineterminator="\n")
    return combined
```

This is a small-file demonstration of an **upsert**: insert new keys, update keys that already exist.

The script deliberately loads the December batch twice:

```text
retry same batch: extracted 396 | target 4246 | duplicate order_ids 0
known answer: rows 4246 | net revenue 5478357.79
```

The retry does not create another 396 rows. The result still reconciles to the shared known answer: **4,246 orders and BDT 5,478,357.79 net revenue excluding Cancelled orders**.

In a database or lakehouse, use native `MERGE` / upsert logic rather than rewriting a whole CSV. The design principle stays the same: identify the row grain with a stable unique key.

## Step 4: ETL vs ELT in the same design

The same modular pipeline can be implemented in either order:

| Pattern | Typical flow | Good fit |
|---|---|---|
| ETL | source → Python validation/cleanup → curated target | Smaller pipelines, strict pre-load rules, external APIs/files |
| ELT | source → raw warehouse/lakehouse → SQL/dbt transformations | Modern warehouses/lakehouses, scalable SQL transformation |

The practice script is ETL because `transform_orders()` runs before the curated CSV is written. In a later dbt module, the project will use an ELT-style approach: land data first, then transform it inside the analytical platform.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| One giant pipeline function | Failures are hard to isolate and test | Separate extract, transform and load responsibilities |
| Advancing the watermark before the load succeeds | Failed rows can be skipped forever | Commit state only after a successful target write |
| Appending every incremental batch | Retries create duplicate business rows | Upsert/MERGE on a stable unique key |
| Using `order_date` when old rows can be edited | Late updates to old dates are missed | Use `updated_at`, a sequence, change tracking or CDC |
| Rebuilding all history every day | Runtime and compute cost grow with history | Use incremental loading once correctness is proven |

## Try it yourself

**Task:** Add a guard to `load_upsert()` that fails if the final target contains duplicate `order_id` values. Then rerun the script and confirm the retry still succeeds.

<details markdown="1">
<summary>Show a hint</summary>

After the `drop_duplicates(...)` step, check `combined["order_id"].duplicated().any()`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
if combined["order_id"].duplicated().any():
    raise AssertionError("target grain broken: duplicate order_id")
```

Place the check immediately before `to_csv()`. It turns the expected target grain into an executable rule.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does an incremental load do after the initial load?

1. Reloads every historical row
2. Processes only new or changed data since the previous successful point
3. Deletes the target and starts again

<details markdown="1"><summary>Show answer</summary>
**B.** Incremental loading reduces repeated work by processing the delta.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why is an idempotent load important?

1. A retry can run safely without changing the intended final result
2. It makes every pipeline real-time
3. It removes the need for validation

<details markdown="1"><summary>Show answer</summary>
**A.** Retries are normal in production, so the same batch must not create duplicate effects.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. When should a pipeline save its new watermark?

1. Before extraction starts
2. After extraction but before loading
3. After the target load has completed successfully

<details markdown="1"><summary>Show answer</summary>
**C.** Otherwise a failure can move the state forward while data is still missing.
</details>
</div>

## Summary

- A modular pipeline separates **extract → transform → load** so each part is easier to test and replace.
- **ETL** transforms before loading; **ELT** loads first and transforms in the target platform.
- A **watermark** records the last successful point so later runs can process only the delta.
- **Idempotency** makes retries safe; an upsert on a stable key prevents duplicate effects.
- The practice run loads 3,850 rows first, 396 incrementally, and still finishes at the known 4,246 orders after retrying the same batch.

!!! job "Job-ready check"
    **Interview question:** *"How would you design a daily incremental orders pipeline so a retry cannot duplicate rows?"*

    **Strong answer:** "I would separate extraction, transformation and loading. I would read only rows after the last successful watermark, validate the batch, then MERGE into the target using `order_id` as the unique key. I would update the stored watermark only after that transaction succeeds. If the scheduler retries the same window, the MERGE updates the same keys instead of appending duplicates, so the job is idempotent. I would also reconcile row counts and business totals after each run."

    **Mini project:** Replace the CSV target with PostgreSQL or Delta Lake. Keep the same 3,850 + 396 load windows, use a native MERGE/upsert, retry December twice, and prove the final table still has 4,246 unique order IDs.
