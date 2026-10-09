---
title: Validation Rules and pytest for Data
order: 1
summary: Turn assumptions about an orders dataset into executable checks, then test those checks automatically with pytest.
level: Intermediate
time: 50 min
topics:
- Validation
- pytest for data
prerequisites:
- phase-3/etl-elt/01-modular-idempotent-incremental
keywords:
- data quality
- validation
- pytest
- data tests
- schema
- uniqueness
- business rule
reviewed: 2026-10-09
files:
- phase-3/data-engineering-scripts.zip
resources:
- title: 'pytest: how to parametrize fixtures and test functions'
  url: https://docs.pytest.org/en/stable/how-to/parametrize.html
  source: pytest documentation
  note: Official guide to running one test against several data-quality cases.
- title: pytest fixtures
  url: https://docs.pytest.org/en/stable/how-to/fixtures.html
  source: pytest documentation
  note: Explains reusable test setup such as loading one practice dataset for several checks.
- title: Pandas duplicate detection
  url: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html
  source: pandas documentation
  note: Reference for detecting duplicate business keys in a DataFrame.
youtube:
  title: How to integrate data quality test in Python ETL pipeline
  creator: BI Insights Inc
  url: https://www.youtube.com/watch?v=7FPksG-LYOA
  video_id: 7FPksG-LYOA
  duration: '6:03'
  language: English
  level: Intermediate
  reviewed: '2026-10-09'
  why_recommended: A short practical companion showing data-quality checks inside a Python ETL workflow. Use it after this
    lesson’s validation functions and pytest tests so you can compare the same engineering idea in another pipeline.
---

## What is it?

**Data validation** turns assumptions about data into checks that can pass or fail. A useful rule is specific enough that a pipeline can evaluate it automatically.

For the textile wholesaler, examples include:

- every `order_id` must be present and unique;
- `status` must be one of four accepted values;
- `quantity` must be positive;
- `discount` must stay between 0 and 0.08;
- `revenue` must agree with the row-level business formula;
- a Cancelled order should not have a delivery duration.

A rule written only in a document can be forgotten. A rule written as code can run every time data moves.

!!! job "Why it matters at work"
    A pipeline can finish successfully and still publish bad data. A duplicated primary key can double-count revenue; an unexpected status can disappear from a dashboard filter; a changed source column can break an ML feature later. Data tests move these failures closer to the point where they were introduced.

The practice code is `16_data_quality_validation.py` plus `test_16_data_quality_validation.py`. This environment ran both with pandas 2.2.3 and pytest 9.0.2.

## Step 1: define the dataset's expected shape

Start with a clear list of required columns and accepted categories:

```python
EXPECTED_COLUMNS = [
    "order_id", "order_date", "customer_id", "region", "segment", "channel",
    "category", "product", "quantity", "unit_price", "discount", "unit_cost",
    "status", "promised_days", "delivery_days", "revenue",
]

ALLOWED_STATUSES = {"Delivered", "Cancelled", "Shipped", "Pending"}
```

The script compares the incoming columns with that contract-like list before it checks individual values.

## Step 2: make each assumption executable

A uniqueness check combines two questions: is the business key present, and is it duplicated?

```python
id_nulls = int(df["order_id"].isna().sum())
duplicates = int(df["order_id"].duplicated().sum())
passed = id_nulls == 0 and duplicates == 0
```

A domain rule checks whether new categories have appeared unexpectedly:

```python
statuses = set(df["status"].dropna().astype(str))
invalid_statuses = sorted(statuses - ALLOWED_STATUSES)
```

A business-formula rule recalculates revenue from the source inputs:

```python
expected_revenue = (
    df["quantity"] * df["unit_price"] * (1 - df["discount"])
).round(2)

revenue_mismatches = int(
    ((df["revenue"] - expected_revenue).abs() > 0.001).sum()
)
```

Run the script:

```bash
python 16_data_quality_validation.py
```

**RUN-HERE — real output:**

```text
validation summary: 9/9 checks passed | rows 4246
PASS | schema               | required 16 columns | missing 0 | unexpected 0
PASS | row count            | expected 4246 | actual 4246
PASS | order_id grain       | nulls 0 | duplicates 0
PASS | status domain        | invalid none | nulls 0
PASS | positive quantity    | invalid rows 0
PASS | discount range       | outside 0.00..0.08: 0
PASS | order date           | unparseable/outside 2025: 0
PASS | revenue formula      | mismatches 0
PASS | cancelled delivery   | cancelled rows with delivery_days: 0
known answer: rows 4246 | unique order_ids 4246 | net revenue 5478357.79
corruption demo: 4 failed checks | order_id grain, status domain, positive quantity, revenue formula
```

The clean dataset reconciles to the shared known answers: **4,246 orders** and **BDT 5,478,357.79 net revenue excluding Cancelled orders**.

The final line is also important. The script deliberately corrupts four rows in memory and confirms that four relevant checks fail. A quality check that never sees a bad case is only half-tested.

## Step 3: test the validation code with pytest

Data-quality code is software, so the checks themselves should have tests.

The test file loads one clean dataset with a fixture:

```python
@pytest.fixture
def orders() -> pd.DataFrame:
    return module.load_orders()
```

Then it uses parametrization to inject several bad values:

```python
@pytest.mark.parametrize(
    ("column", "value", "expected_check"),
    [
        ("status", "Returned", "status domain"),
        ("quantity", 0, "positive quantity"),
        ("discount", 0.50, "discount range"),
        ("order_date", "2026-01-01", "order date"),
        ("revenue", -1.0, "revenue formula"),
    ],
)
def test_bad_value_is_detected(orders, column, value, expected_check):
    bad = orders.copy()
    bad.loc[0, column] = value
    assert expected_check in failed_checks(bad)
```

Run:

```bash
pytest -q test_16_data_quality_validation.py
```

**RUN-HERE — real output:**

```text
.........                                                                [100%]
9 passed in 0.17s
```

## Step 4: decide which failures block the pipeline

Not every rule has the same operational meaning.

| Example | Suggested severity | Why |
|---|---|---|
| Duplicate `order_id` | Error / block | It breaks the table grain and can double-count metrics |
| Missing required column | Error / block | Downstream code may be unable to run correctly |
| Unknown `status` | Error or warning | Depends on whether the source deliberately added a new valid state |
| Small drop in daily volume | Warning first | It may be a business pattern rather than bad data |
| Stale source | Warning → error | Severity should increase after an agreed threshold |

A mature pipeline records the result, affected rule, dataset, run time and severity rather than printing only `True` or `False`.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Checking only nulls | Duplicates, invalid ranges and broken business rules pass unnoticed | Test several quality dimensions: schema, uniqueness, validity and logic |
| Hard-coding every observed value as a rule | Normal business change causes false alarms | Separate stable contracts from monitoring thresholds |
| Testing only clean data | Broken validation code can still look successful | Inject known defects and prove each important rule fails |
| Making every anomaly fatal | Pipelines become noisy and fragile | Classify rules by warning vs blocking severity |
| Running tests only on a laptop | Production data can bypass the checks | Put validation in CI and/or the scheduled data pipeline |

## Try it yourself

**Task:** Add a validation rule stating that `promised_days` must be between 3 and 6 inclusive. Add a pytest case that deliberately changes one row to `10` and proves the rule fails.

<details markdown="1">
<summary>Show a hint</summary>

Use `Series.between(3, 6, inclusive="both")`, then count rows where that expression is false.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
bad_promised = int((~df["promised_days"].between(3, 6, inclusive="both")).sum())
results.append(CheckResult(
    "promised days",
    bad_promised == 0,
    f"outside 3..6: {bad_promised}",
))
```

Then copy the DataFrame in a test, set one `promised_days` value to `10`, and assert that `"promised days"` appears in the failed-check set.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Why test `order_id` for both nulls and duplicates?

1. Because a business key must identify exactly one row
2. Because pytest requires two assertions per column
3. Because duplicate values automatically become null

<details markdown="1"><summary>Show answer</summary>
**A.** A key that is missing or repeated cannot reliably identify one business record.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What is the main benefit of parametrizing a pytest test?

1. It automatically repairs bad source data
2. It runs the same test logic against several input cases
3. It replaces the need for production monitoring

<details markdown="1"><summary>Show answer</summary>
**B.** Parametrization is useful when several bad values should trigger the same validation behaviour.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which check should usually block publishing most quickly?

1. A minor volume change that may be seasonal
2. A cosmetic column-order preference
3. Duplicate values in the declared primary business key

<details markdown="1"><summary>Show answer</summary>
**C.** A broken key can corrupt joins and aggregates, so it is normally a blocking integrity failure.
</details>
</div>

## Summary

- Validation turns assumptions into executable rules.
- Good data tests cover structure, uniqueness, allowed values, ranges and business logic.
- The clean practice data passes **9/9** rules and still reconciles to 4,246 orders and BDT 5,478,357.79 net revenue.
- pytest tests the validation code itself; this lesson's suite ran **9 tests successfully**.
- Injecting known defects proves that your tests can fail for the right reasons.

!!! job "Job-ready check"
    **Interview question:** *"How would you add data-quality tests to a daily orders pipeline?"*

    **Strong answer:** "I would first define the table grain and stable business rules: required columns, primary-key uniqueness, accepted status values, numeric ranges, date validity and key calculations. I would implement those rules as reusable validation functions, write pytest tests that include both clean and intentionally bad cases, and run them in CI plus the scheduled pipeline. Blocking failures would stop downstream publication; warning-level rules would alert and be tracked without necessarily stopping the run."

    **Mini project:** Add three domain-specific rules to `16_data_quality_validation.py`, create corrupted test cases for each, and make the pytest suite run in a GitHub Actions workflow.
