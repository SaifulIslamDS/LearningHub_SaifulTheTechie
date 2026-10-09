---
title: "Data Leakage & Scaling: Why Models Look Great, Then Fail"
order: 2
summary: "Recognise the two main kinds of data leakage — target leakage and train/test contamination — and prevent them with pipelines; then learn when feature scaling matters and how to do it safely."
level: Intermediate
time: "45 min"
topics: ["Leakage", "Scaling"]
prerequisites: ["phase-2/ml-foundations/01-sklearn-train-test-split"]
keywords: [data leakage, target leakage, train test contamination, too good to be true, future information, target encoding, aggregate leakage, feature scaling, standardization, standardscaler, minmaxscaler, normalization, knn, k-nearest neighbours, distance, pipeline, fit transform]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv]
resources:
  - title: "Common pitfalls and recommended practices (data leakage)"
    url: "https://scikit-learn.org/stable/common_pitfalls.html"
    source: "scikit-learn official docs"
    note: "Inconsistent preprocessing and data leakage, with code examples."
  - title: "Importance of feature scaling"
    url: "https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html"
    source: "scikit-learn official docs"
    note: "How scaling changes KNN and PCA results."
  - title: "Kaggle Learn: Intermediate Machine Learning — Data Leakage"
    url: "https://www.kaggle.com/learn/intermediate-machine-learning"
    source: "Kaggle (free course)"
    note: "Short, practical lesson on target leakage and train-test contamination."
---

## What is it?

- **Data leakage** = the model gets information during training that it won't have when it's used for real. Scores look excellent in testing, then collapse in production.
- **Feature scaling** = putting numeric features on comparable scales (e.g. mean 0, standard deviation 1), so that methods based on distances or penalties treat them fairly.

| Leakage type | What happens | Example |
|---|---|---|
| **Target leakage** | A feature is only known *after* the outcome, or is a consequence of it | Delivery days for predicting cancellation |
| **Train/test contamination** | Information from the test set influences training | Statistics computed on all data before the split |

!!! job "Why it matters at work"
    Leakage is the most common reason ML projects fail after a great demo: "98% accuracy" turns into a coin flip in production. Spotting a too-good-to-be-true result, and explaining why, is a skill interviewers probe directly.

The script is `18_ml_leakage_scaling.py`. The honest model from the previous lesson is the reference:

```text
honest model (order-time features only): ROC AUC 0.652
```

## Leak 1: a column filled in after the outcome

Delivered orders have `delivery_days`; cancelled orders never do. Someone adds "is delivery known?" as a feature:

```python
df["delivery_known"] = df["delivery_days"].notna().astype(int)
print(pd.crosstab(df["delivery_known"], df["cancelled"]))
```

```text
cancelled          0    1
delivery_known
0                 46  283
1               3872    0
```

```text
with delivery_known: ROC AUC 1.000  <- too good to be true
```

A **perfect** score. The feature *is* the answer: every order with a known delivery was not cancelled. But when a new order is placed, nobody knows its delivery days yet, so the model is useless in practice.

**Defence:** for every feature, ask **"would I know this at the moment of prediction?"** Keep a written list of allowed features (that's what `ORDER_TIME_FEATURES` in `ml_data.py` is), and treat any big jump in score as a bug until proven otherwise.

## Leak 2: an aggregate that includes the test data

"Customers who cancelled before will cancel again" is a reasonable idea. But compute the customer's cancellation rate on **all** orders, and the test orders' own outcomes leak into their feature:

```python
rate_all = df.groupby("customer_id")["cancelled"].transform("mean")      # includes test orders!
```

```text
customer rate from all data: ROC AUC 0.684
```

The honest version learns the rate from **training orders only**, and gives unknown customers the overall training rate:

```python
train_rate = df.loc[train_idx].groupby("customer_id")["cancelled"].mean()
df["cust_rate"] = df["customer_id"].map(train_rate).fillna(y[train_idx].mean())
```

```text
customer rate from train only: ROC AUC 0.627
```

The leaky version scored 0.684; done correctly, the feature doesn't help at all (0.627, slightly *worse* than without it). This leak is subtle: no single column looks suspicious, and the score is only a little too good. In production you'd also compute it from **past** orders only, never including the current order.

## More places leakage hides

| Where | Leaky | Safe |
|---|---|---|
| Scaling / imputing | `scaler.fit(all_data)` before splitting | `Pipeline` fitted on the training split |
| Duplicates | The same order in train and test | De-duplicate before splitting |
| Time | Random split when predicting the future | Train on past, test on future |
| Groups | One customer's orders in both train and test, when you'll predict *new* customers | Group-based split (`GroupKFold`) |
| Target-derived features | Status, refund flags, "complaint logged" | Exclude anything created after the outcome |

## Scaling: when it matters

Our numeric features live on wildly different scales:

```text
       quantity  unit_price  discount  credit_days
mean    3169.25        2.12      0.03        21.92
std     6842.61        1.73      0.03        20.12
max   250160.00        5.61      0.08        60.00
```

**k-nearest neighbours (KNN)** predicts from the most similar past orders, measured by distance. Unscaled, a difference of 1,000 in quantity swamps every other feature:

```python
knn_raw = KNeighborsClassifier(n_neighbors=50).fit(X_tr, y[train_idx])
knn_scaled = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=50))]).fit(X_tr, y[train_idx])
```

```text
KNN without scaling: ROC AUC 0.516
KNN with scaling:    ROC AUC 0.621
```

Without scaling, KNN is barely better than random (0.516): it's effectively using quantity alone. Scaling lets credit days and discount count too.

| Method | Needs scaling? | Why |
|---|---|---|
| KNN, k-means, SVM, PCA | **Yes** | Based on distances |
| Linear/logistic regression with regularisation | **Yes** | The penalty treats all coefficients alike; also helps the solver converge |
| Decision trees, random forests, gradient boosting | No | Split on one feature at a time; scale doesn't matter |

`StandardScaler` (mean 0, std 1) is the usual default; `MinMaxScaler` maps to 0–1; for heavy outliers, take logs first or use `RobustScaler`.

### Scale inside the pipeline

```python
scaler = StandardScaler().fit(X_tr)
print("scaler learned from TRAIN:", {k: round(float(v), 2) for k, v in zip(num_only[:2], scaler.mean_[:2])})
```

```text
scaler learned from TRAIN: {'quantity': 3168.91, 'unit_price': 2.12}
```

The scaler's mean and std must come from **training data only**, then be applied unchanged to test and future data. A `Pipeline` does this automatically.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Celebrating a near-perfect score | Shipping a leaky model | Treat it as a bug; find the leaking feature |
| Features created after the outcome | Model useless in production | "Known at prediction time?" checklist |
| Aggregates or encodings on all data | Mildly inflated, hard-to-spot scores | Compute them inside the training fold only |
| `fit_transform` on the full dataset | Test information leaks into preprocessing | Pipelines; fit on train, transform test |
| Scaling for trees, not scaling for KNN | Wasted effort, or a broken model | Know which methods are distance/penalty-based |

## Try it yourself

**Task:** A colleague says `revenue` is leakage because revenue is "the result". Is it? Retrain without `revenue` and compare.

<details markdown="1">
<summary>Show the solution</summary>

```python
print(f"without revenue: ROC AUC {auc([f for f in ORDER_TIME_FEATURES if f != 'revenue'], [n for n in NUMERIC if n != 'revenue']):.3f}")
```

```text
without revenue: ROC AUC 0.650
```

It's **not** leakage: order revenue (quantity × price × (1 − discount)) is known the moment the order is placed. Removing it barely changes the score (0.652 → 0.650). The test for leakage is about **timing** (is it known at prediction time?), not about whether a column sounds like an outcome.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A new feature raises ROC AUC from 0.65 to 1.00. What's your first reaction?

1. Ship it
2. Suspect leakage and check whether the feature is known at prediction time
3. Add more features

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which model is most affected by unscaled features?

1. Decision tree
2. k-nearest neighbours
3. Random forest

<details markdown="1"><summary>Show answer</summary>
**B.** It's based on distances.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Where should a `StandardScaler` learn its mean and standard deviation?

1. From all the data
2. From the training data only
3. From the test data

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Leakage** = information at training time that won't exist at prediction time. Too-good scores are a warning sign.
- Guard against **target leakage** (features created after the outcome) and **contamination** (statistics using test data).
- **Scale** for distance- and penalty-based models (KNN, SVM, PCA, regularised regression); trees don't need it.
- Put all preprocessing in a **Pipeline** fitted on training data only.

!!! job "Job-ready check"
    **Interview question:** *"Your model scores 99% in testing but performs poorly in production. What happened?"*

    **Strong answer:** "Most likely leakage: a feature that's only known after the outcome, preprocessing or encodings fitted on all the data, duplicates across train and test, or a random split on time-dependent data. I'd audit each feature for 'known at prediction time?', rebuild preprocessing in a pipeline, use a time-based split, and compare the new score with a simple baseline."

    **Mini project:** Write a "feature audit" table for the cancellation model: each column in `orders_2025.csv`, when it becomes known, and whether it's allowed as a feature, with a reason.
