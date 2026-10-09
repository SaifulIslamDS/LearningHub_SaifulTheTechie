---
title: "Great Expectations"
order: 2
summary: "Express reusable data-quality assertions as Expectations and validate the 2025 orders through an Expectation Suite."
level: Intermediate
time: "45 min"
topics: ["Great Expectations"]
prerequisites: ["phase-3/data-quality/01-validation-rules-pytest"]
keywords: [data quality, great expectations, expectation, expectation suite, validation definition, data tests]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Define Expectations"
    url: "https://docs.greatexpectations.io/docs/core/define_expectations/"
    source: "Great Expectations"
    note: "Official GX Core guide to Expectations and Expectation Suites."
  - title: "Connect to dataframe data"
    url: "https://docs.greatexpectations.io/docs/core/connect_to_data/dataframes/"
    source: "Great Expectations"
    note: "Official pattern for a pandas Data Source, Data Asset and whole-dataframe Batch Definition."
  - title: "Create a Validation Definition"
    url: "https://docs.greatexpectations.io/docs/core/run_validations/create_a_validation_definition/"
    source: "Great Expectations"
    note: "Shows how a Batch Definition and Expectation Suite are linked for validation."
---

## What is it?

**Great Expectations (GX)** is a data-quality framework that expresses checks as **Expectations**. An Expectation is a verifiable assertion such as *“`order_id` values are unique.”* An **Expectation Suite** groups related assertions for a dataset.

GX then connects the Suite to a particular batch of data and produces a structured Validation Result instead of only a custom print statement.

The official documentation checked on **2026-10-09** shows GX Core **1.24.0**. The practice script is written for that API.

!!! job "Why it matters at work"
    Hand-written validation functions are excellent for learning and for highly custom business logic. A framework becomes useful when a team wants a shared vocabulary, reusable suites, structured validation results, checkpoints, documentation and integrations. The trade-off is an extra dependency and framework concepts that the team must operate well.

## Step 1: create an ephemeral GX context

For this lesson we do not need to persist a GX project directory. An ephemeral context keeps the example self-contained:

```python
import great_expectations as gx

context = gx.get_context(mode="ephemeral")
```

GX 1.24.0 supports ephemeral contexts for temporary or CI-style validation work.

## Step 2: connect an in-memory pandas DataFrame

GX organizes the connection as **Data Source → Data Asset → Batch Definition**:

```python
data_source = context.data_sources.add_pandas(name="orders_pandas")
data_asset = data_source.add_dataframe_asset(name="orders_2025")
batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_orders")
```

The DataFrame itself is passed later as a runtime batch parameter.

## Step 3: build an Expectation Suite

The practice suite encodes six high-value rules:

```python
suite = gx.ExpectationSuite(name="orders_quality_suite")
suite = context.suites.add(suite)

suite.add_expectation(gx.expectations.ExpectTableRowCountToEqual(value=4246))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["Delivered", "Cancelled", "Shipped", "Pending"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="quantity", min_value=1, strict_min=False
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="discount", min_value=0, max_value=0.08
    )
)
```

Notice the separation of concerns: the Suite says what good data looks like, while the Batch Definition says which data to validate.

## Step 4: link the Suite to data with a Validation Definition

```python
validation_definition = gx.ValidationDefinition(
    data=batch_definition,
    suite=suite,
    name="orders_2025_validation",
)
validation_definition = context.validation_definitions.add(validation_definition)

result = validation_definition.run(
    batch_parameters={"dataframe": df}
)
```

That is the core pattern you can later place behind a checkpoint or pipeline task.

## Verification status for this lesson

**RUN-BY-OWNER.** GX Core is not installed in this execution environment, and the environment cannot currently install new packages from PyPI. I therefore compiled the Python script for syntax but did **not** invent a GX validation result.

The complete script is `17_great_expectations_orders.py`. Run it locally with:

```bash
python -m pip install "great_expectations==1.24.0"
python 17_great_expectations_orders.py
```

The script prints the actual `success` value and the successful/evaluated Expectation counts from the returned Validation Result. Treat that local output as the authoritative lesson run until GX becomes available in this environment.

## When should you use custom pytest rules vs GX?

| Approach | Strength | Good fit |
|---|---|---|
| Plain Python + pytest | Transparent, flexible, easy to unit-test | Custom business logic and small engineering projects |
| Great Expectations | Declarative rules, Suites, structured results and broader quality workflow | Shared team standards and repeatable validation across data assets |
| Both | Custom logic plus framework-level expectations | Production systems where some rules are simple and some are domain-specific |

The tools are complementary. pytest can also test your GX configuration helpers or custom Expectations.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Treating GX as a replacement for understanding the data | Teams create many checks without knowing which ones protect business decisions | Start from the table grain and real failure modes |
| Adding dozens of low-value Expectations | Alert fatigue grows and important failures are ignored | Prioritize critical schema, key, domain and business rules |
| Pinning no version in a learning or production environment | Framework API changes can make examples irreproducible | Record and pin the verified GX version |
| Showing framework output that was never run | Learners cannot know whether the example actually works | Label owner-run/reference-only code honestly |
| Putting all rules at the same severity | Minor drift can block critical pipelines | Design severity and response with the data owner |

## Try it yourself

**Task:** Add an Expectation that `promised_days` stays between 3 and 6 inclusive. Then run the Validation Definition locally.

<details markdown="1">
<summary>Show a hint</summary>

Use another `ExpectColumnValuesToBeBetween` Expectation before creating the Validation Definition.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="promised_days", min_value=3, max_value=6
    )
)
```

Rerun the script and read the counts from the real Validation Result rather than hard-coding an expected message.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What is an Expectation Suite?

1. A collection of Expectations describing the desired state of data
2. A replacement for the source database
3. A Python virtual environment

<details markdown="1"><summary>Show answer</summary>
**A.** A Suite groups the assertions that should hold for a data asset.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does a Validation Definition link in this lesson?

1. A dashboard to a CSS file
2. A Batch Definition to an Expectation Suite
3. A pytest fixture to a Docker container

<details markdown="1"><summary>Show answer</summary>
**B.** The Validation Definition connects the data selection with the rules to evaluate.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why is there no GX output block in this lesson?

1. GX never returns validation output
2. The dataset contains no quality rules
3. GX could not be executed in this environment, so fabricated output would violate the verification rule

<details markdown="1"><summary>Show answer</summary>
**C.** Reference or owner-run code must be labelled honestly when it cannot be executed here.
</details>
</div>

## Summary

- GX expresses reusable assertions as **Expectations** and groups them in an **Expectation Suite**.
- A pandas Data Source, Data Asset and Batch Definition describe the data GX will validate.
- A Validation Definition connects that Batch Definition to the Suite.
- `17_great_expectations_orders.py` contains six rules for the 2025 orders.
- The script is **RUN-BY-OWNER** because GX 1.24.0 is unavailable in this execution environment; no validation output has been fabricated.

!!! job "Job-ready check"
    **Interview question:** *"Why might a data team use Great Expectations instead of only writing `if` statements?"*

    **Strong answer:** "Plain Python checks are useful and I still use them for custom business logic. Great Expectations adds a declarative quality vocabulary, reusable Expectation Suites, structured validation results and workflow components that are easier to standardize across assets. I would choose the framework when those team-level capabilities justify the dependency, and I would still unit-test critical custom logic."

    **Mini project:** Run `17_great_expectations_orders.py` locally, save the real Validation Result summary, then add one new business-relevant Expectation and document whether it should warn or block the pipeline.
