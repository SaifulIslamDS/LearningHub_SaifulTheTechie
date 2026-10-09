---
title: "Data Contracts, Freshness and Alerting"
order: 3
summary: "Define a machine-readable orders contract, measure whether the source is fresh enough, and turn failures into useful operational alerts."
level: Intermediate
time: "50 min"
topics: ["Data contracts", "Freshness & alerting"]
prerequisites: ["phase-3/data-quality/01-validation-rules-pytest", "phase-3/etl-elt/02-replayable-pipelines-cdc"]
keywords: [data quality, data contract, json schema, freshness, alerting, sla, schema]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip, phase-3/orders_contract.schema.json]
resources:
  - title: "JSON Schema Draft 2020-12"
    url: "https://json-schema.org/draft/2020-12/"
    source: "JSON Schema"
    note: "Current published JSON Schema dialect used by the downloadable row contract."
  - title: "JSON Schema validation vocabulary"
    url: "https://json-schema.org/draft/2020-12/json-schema-validation"
    source: "JSON Schema"
    note: "Defines structural assertions such as required properties, types, enums and numeric bounds."
  - title: "Freshness configuration"
    url: "https://docs.getdbt.com/reference/resource-configs/freshness"
    source: "dbt Developer Hub"
    note: "A production-oriented example of warn/error freshness thresholds for analytical data."
---

## What is it?

A **data contract** is an explicit agreement about the structure and meaning a dataset promises to consumers. It can include:

- required fields and data types;
- primary or business keys;
- accepted categories and numeric bounds;
- ownership and versioning;
- delivery or freshness expectations;
- what happens when the contract is broken.

This lesson uses **JSON Schema Draft 2020-12** for row structure, then adds dataset-level uniqueness and freshness rules in Python.

**Freshness** asks a different question from row validity: *How old is the newest trustworthy data compared with when it was expected?* A perfectly valid table can still be operationally wrong if yesterday's load never arrived.

!!! job "Why it matters at work"
    Contracts reduce silent producer/consumer breakage. Freshness checks catch successful-but-stale pipelines. Alerting connects those checks to an operational response: warn someone, stop downstream publication, or escalate when an agreed threshold is crossed.

The downloadable contract is `orders_contract.schema.json`, and the runnable example is `18_data_contract_freshness.py`.

## Step 1: express row structure as a machine-readable contract

A few fields from the practice contract look like this:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["order_id", "order_date", "customer_id", "status", "revenue"],
  "properties": {
    "order_id": {"type": "integer", "minimum": 1},
    "status": {
      "type": "string",
      "enum": ["Delivered", "Cancelled", "Shipped", "Pending"]
    },
    "discount": {"type": "number", "minimum": 0, "maximum": 0.08}
  }
}
```

The full practice file declares all 16 fields. `additionalProperties: false` also makes an unexpected producer-side column visible instead of silently accepting schema drift.

JSON Schema validates individual row structure. The script separately enforces dataset-level rules such as unique `order_id` values and the expected 4,246-row practice snapshot.

## Step 2: validate every row against the contract

`jsonschema` can compile the Draft 2020-12 contract once and reuse it:

```python
validator = Draft202012Validator(schema)
errors = 0

for row in records_for_contract(df):
    errors += sum(1 for _ in validator.iter_errors(row))

duplicate_ids = int(df["order_id"].duplicated().sum())
```

Run:

```bash
python 18_data_contract_freshness.py
```

**RUN-HERE — real output:**

```text
contract: PASS | rows 4246 | schema errors 0 | duplicate order_ids 0
latest source date: 2025-12-31
freshness at 2026-01-01: PASS | age 1 day
freshness at 2026-01-02: WARN | age 2 days
freshness at 2026-01-04: ERROR | age 4 days
alert: ERROR -> stop downstream publish and notify data owner | age 4 days
```

The contract validates all 4,246 rows with zero row-schema errors and zero duplicate IDs.

## Step 3: define freshness thresholds before an incident

The example deliberately uses **fixed demonstration dates** so the output is deterministic:

```python
def freshness_status(latest_date, as_of):
    age_days = (as_of - latest_date).days
    if age_days <= 1:
        return "PASS", age_days
    if age_days == 2:
        return "WARN", age_days
    return "ERROR", age_days
```

For a source whose latest date is 2025-12-31:

- on 2026-01-01 it is one day old → **PASS**;
- on 2026-01-02 it is two days old → **WARN**;
- on 2026-01-04 it is four days old → **ERROR**.

In a real daily pipeline, compare the latest successful source/load timestamp with the scheduler's run time or an agreed service-level expectation. Do not use these exact thresholds blindly for every dataset.

Current dbt documentation uses the same operational pattern: configurable `warn_after` and `error_after` freshness thresholds, with a loaded-at timestamp or query used to identify the newest data.

## Step 4: make alerts actionable

An alert needs enough context for a person to decide what to do. A useful message includes:

```text
Dataset: orders_2025
Check: freshness
Status: ERROR
Latest data: 2025-12-31
Age: 4 days
Action: stop downstream publish; notify data owner
```

A simple response model is:

| State | Pipeline behaviour | Human response |
|---|---|---|
| PASS | Continue | No action |
| WARN | Continue or mark output degraded | Investigate if warning persists |
| ERROR | Stop dependent publish | Notify owner/on-call; investigate source or load |

The important part is not which messaging tool you use. It is that the alert has an owner and a defined action.

## Step 5: version contracts instead of silently editing them

A contract becomes useful when producers and consumers know which version they depend on.

For example:

- **v1:** current 16 columns and current status values;
- **v1.1:** clarify documentation without breaking consumers;
- **v2:** deliberately add or change a field in a way that requires consumer migration.

When a producer needs a breaking change, coordinate it rather than silently changing the source and hoping downstream jobs still work.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Calling a schema file a complete contract | Ownership, freshness and operational behaviour remain undefined | Treat schema as one machine-readable part of a wider agreement |
| Using the current wall clock in a teaching test | Lesson output changes depending on when it runs | Use fixed demo timestamps; use real scheduler time in production |
| Alerting without an owner | Failures create noise but no response | Route alerts to a named team/person with a runbook action |
| Setting thresholds without business context | Normal delays trigger incidents, or real incidents are missed | Agree expected delivery time and tolerated delay with consumers |
| Making a breaking schema change in place | Downstream jobs fail unexpectedly | Version the contract and coordinate consumer migration |

## Try it yourself

**Task:** Copy the JSON contract, change the maximum allowed `discount` from `0.08` to `0.05`, and run the validator. Explain whether the failures mean the data is bad or the new contract is incompatible with existing valid business behaviour.

<details markdown="1">
<summary>Show a hint</summary>

A failed contract does not automatically tell you which side is wrong. Compare the proposed rule with the existing business definition before changing either the data or the contract.
</details>

<details markdown="1">
<summary>Show the solution</summary>

Change:

```json
"discount": {"type": "number", "minimum": 0, "maximum": 0.05}
```

Then rerun the script. If current legitimate orders contain discounts above 5%, the new rule represents a breaking contract change. The right action is to confirm the business rule with the producer/consumer owners rather than deleting or rewriting valid orders just to make the test green.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What problem does a data contract primarily address?

1. It makes every pipeline run faster
2. It makes producer/consumer expectations explicit and testable
3. It replaces all data documentation

<details markdown="1"><summary>Show answer</summary>
**B.** A contract reduces ambiguity about the structure and behaviour consumers can rely on.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. A dataset passes every row validation but its newest load is four days late. What kind of problem is this?

1. Freshness
2. Uniqueness
3. Syntax highlighting

<details markdown="1"><summary>Show answer</summary>
**A.** Correct rows can still be too stale for the business decision they support.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What should an ERROR-level freshness alert do in this lesson's policy?

1. Silently continue publishing
2. Delete the source data
3. Stop downstream publication and notify the data owner

<details markdown="1"><summary>Show answer</summary>
**C.** A blocking stale-data condition should prevent consumers from receiving an apparently current output.
</details>
</div>

## Summary

- A data contract makes producer/consumer expectations explicit and testable.
- JSON Schema Draft 2020-12 provides the machine-readable row structure in this exercise.
- The real practice run validates **4,246 rows**, with **0 schema errors** and **0 duplicate order IDs**.
- Freshness needs agreed warning and error thresholds based on the dataset's expected delivery schedule.
- Alerts are useful only when severity maps to a clear pipeline action and an accountable owner.

!!! job "Job-ready check"
    **Interview question:** *"How is a data contract different from a data-quality test?"*

    **Strong answer:** "A quality test is an executable check on a particular property of data. A data contract is the broader producer/consumer agreement: schema and types, key semantics, accepted values, ownership, versioning, freshness expectations and what happens when those promises are broken. I implement important contract clauses as automated tests and route failures according to severity."

    **Mini project:** Add an `owner`, contract version and expected delivery schedule to the practice contract package, then write a small alert function that produces a JSON incident payload when freshness reaches ERROR.
