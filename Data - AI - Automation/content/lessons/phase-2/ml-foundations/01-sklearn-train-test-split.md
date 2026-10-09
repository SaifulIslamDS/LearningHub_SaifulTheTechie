---
title: "scikit-learn & the Train/Test Split: Your First Honest Model"
order: 1
summary: "Frame a prediction problem, build a scikit-learn pipeline, hold out a test set, beat a baseline, and choose a metric and threshold that match the business — not just accuracy."
level: Intermediate
time: "55 min"
topics: ["scikit-learn", "Train/test split"]
prerequisites: ["phase-2/pandas/03-merge-groupby", "phase-2/statistics/02-correlation-confidence-intervals"]
keywords: [machine learning, scikit-learn, sklearn, classification, logistic regression, pipeline, columntransformer, onehotencoder, train test split, stratify, test set, baseline, dummyclassifier, accuracy, precision, recall, roc auc, threshold, time-based split, fit, predict, predict_proba]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv]
resources:
  - title: "Getting started with scikit-learn"
    url: "https://scikit-learn.org/stable/getting_started.html"
    source: "scikit-learn official docs"
    note: "Estimators, pipelines, fit/predict and model evaluation in one page."
  - title: "Metrics and scoring: quantifying the quality of predictions"
    url: "https://scikit-learn.org/stable/modules/model_evaluation.html"
    source: "scikit-learn official docs"
    note: "Accuracy, precision, recall, ROC AUC and when to use each."
  - title: "Machine Learning Crash Course"
    url: "https://developers.google.com/machine-learning/crash-course"
    source: "Google for Developers (free)"
    note: "Short modules on classification, thresholds and evaluation."
---

## What is it?

- **scikit-learn** (`sklearn`) is Python's standard library for classic machine learning. Every model has the same interface: `fit(X, y)` to learn, `predict(X)` / `predict_proba(X)` to use.
- The **train/test split** keeps part of the data hidden during training, so you can measure how the model does on **new** data, the only performance that matters.

| Word | In our problem |
|---|---|
| **Target (y)** | `cancelled`: 1 if the order was cancelled, else 0 |
| **Features (X)** | What we know when the order is placed: segment, region, channel, category, quantity, price, discount, revenue, promised days, credit terms, month |
| **Classification** | Predicting a category (cancelled or not) |
| **Model** | Logistic regression: a weighted sum of features turned into a probability |

!!! job "Why it matters at work"
    Most ML failures in companies aren't bad algorithms; they're bad evaluation: no baseline, a leaky feature, accuracy on unbalanced data, or a random split for a time problem. Getting these foundations right is what interviewers test in "walk me through how you'd build this model" questions.

The script is `17_ml_sklearn_split.py`. `ml_data.py` loads the orders, joins credit terms, drops 45 still-pending orders (their outcome is unknown) and defines which columns are allowed as features.

```text
4201 orders, 283 cancelled (6.7%)
```

## Step 1: split first

```python
X, y = df[ORDER_TIME_FEATURES], df["cancelled"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
```

```text
train 3150 (6.7% cancelled) | test 1051 (6.8% cancelled)
```

- **75% to train, 25% to test.** The test set is locked away until the end.
- `stratify=y` keeps the rare class (6.7%) at the same rate in both parts.
- `random_state=42` makes the split reproducible.

## Step 2: a baseline

```python
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
```

```text
baseline accuracy 0.932 | ROC AUC 0.500
```

A "model" that says **never cancelled** is right 93.2% of the time. That's why **accuracy is misleading** when one class is rare. **ROC AUC** is better here: it measures how well the model *ranks* cancelled orders above others (0.5 = random, 1.0 = perfect).

## Step 3: a real model in a pipeline

```python
prep = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),   # text categories -> 0/1 columns
    ("num", StandardScaler(), NUMERIC),                             # numbers -> comparable scale
])
model = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=1000))])
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
```

```text
logistic accuracy 0.932 | ROC AUC 0.652
```

A **Pipeline** chains preprocessing and the model, so `fit` learns everything (categories, scaling, weights) from the **training data only**, and `predict` applies the same steps to new data. It's the single most important habit in scikit-learn (the next lesson shows why).

**ROC AUC 0.652**: clearly better than random (0.5), but far from perfect. Cancellations are hard to predict from order details alone. That's an honest, useful finding.

## Step 4: why accuracy stayed at 0.932

```python
print(classification_report(y_test, model.predict(X_test), digits=3, zero_division=0))
```

```text
              precision    recall  f1-score   support

           0      0.932     1.000     0.965       980
           1      0.000     0.000     0.000        71
```

At the default **threshold of 0.5**, the model never predicts "cancelled" (no order reaches a 50% risk), so recall for cancellations is 0. The model still *ranks* orders usefully; we just need a threshold that fits the business.

| Metric | Question it answers |
|---|---|
| **Precision** | Of the orders we flag, how many really cancel? |
| **Recall** | Of the orders that cancel, how many did we flag? |
| **ROC AUC** | How well are cancellations ranked above non-cancellations, across all thresholds? |

## Step 5: a business threshold

Suppose the credit team can check **10% of orders**. Flag the riskiest 10%:

```python
cut = np.quantile(proba, 0.90)
flag = proba >= cut
caught = (flag & (y_test == 1)).sum()
```

```text
flag top 10% (106 orders): catches 16 of 71 cancellations (23%); precision 15% vs base rate 7%
```

Checking 10% of orders catches 23% of cancellations, and a flagged order is **twice as likely** to cancel as a random one (15% vs 7%). Whether that's worth it is a **business** decision: the cost of a credit check vs the cost of a cancelled order.

## Step 6: respect time

In real use, the model is trained on the past and used on the future. A **time-based split** mimics that:

```python
is_train = df["order_date"] < "2025-10-01"
model.fit(X[is_train], y[is_train])
auc_time = roc_auc_score(y[~is_train], model.predict_proba(X[~is_train])[:, 1])
```

```text
time-based split: train 2899 orders, test 1302 | ROC AUC 0.634
```

Slightly lower than the random split (0.652): the future is a bit different from the past (October–December is the busy season). The time-based number is the more honest estimate.

## Step 7: what did it learn?

```text
cat__segment_Garment Factory   -0.22
cat__segment_Knitting Mill     -0.16
num__unit_price                -0.15
cat__channel_Phone              0.23
cat__segment_Retailer           0.49
num__credit_days                0.56
dtype: float64
```

Positive coefficients raise the cancellation risk: **long credit terms, retailers and phone orders**, the same drivers the EDA found. When a model agrees with careful EDA, trust it more; when it doesn't, investigate.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| No test set, or peeking at it while tuning | Over-optimistic scores | Split first; touch the test set once, at the end |
| Reporting accuracy on rare outcomes | 93% "accuracy" from a useless model | Baseline + ROC AUC, precision and recall |
| Default 0.5 threshold | Model never flags anything | Choose the threshold from business capacity and costs |
| Random split for time-dependent data | Scores that won't hold in production | Train on the past, test on the future |
| Preprocessing outside a pipeline | Leakage from test into train | `Pipeline` + `ColumnTransformer` |

## Try it yourself

**Task:** Re-run the random split with `random_state` 1, 2 and 3 and fit the same pipeline each time. How much does the test ROC AUC move? What does that tell you about a single score?

<details markdown="1">
<summary>Show the solution</summary>

```python
for seed in [1, 2, 3]:
    Xa, Xb, ya, yb = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    print(seed, round(roc_auc_score(yb, model.fit(Xa, ya).predict_proba(Xb)[:, 1]), 3))
```

```text
1 0.69
2 0.638
3 0.686
```

The score ranges from 0.64 to 0.69 depending only on **which** orders land in the test set. With about 70 cancellations in a test set, one score is noisy. That's why the next lessons use **cross-validation** (several splits, averaged) and report a ± range.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. 6.7% of orders are cancelled. A model has 93% accuracy. What can you conclude?

1. It's an excellent model
2. Nothing yet: predicting "never cancelled" also gets about 93%
3. It has 93% recall

<details markdown="1"><summary>Show answer</summary>
**B.** Compare with a baseline and use ROC AUC, precision and recall.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why put preprocessing and the model in one `Pipeline`?

1. It runs faster
2. Everything is learned from the training data only and applied the same way to new data
3. It's required for logistic regression

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A model will predict next month's cancellations. Which split best estimates its real performance?

1. A random 75/25 split
2. Train on earlier months, test on later months
3. Train and test on all data

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Define the **target**, and use only features known **at prediction time**.
- **Split first** (stratified; time-based for time problems), compare with a **baseline**.
- Use a **Pipeline** so preprocessing is learned from training data only.
- For rare outcomes, use **ROC AUC, precision and recall**, and pick a **threshold** from business capacity.

!!! job "Job-ready check"
    **Interview question:** *"How would you build a model to flag orders likely to be cancelled?"*

    **Strong answer:** "I'd define the target and restrict features to what's known at order time. I'd split by time (train on earlier months, test on later), start with a baseline and a simple, interpretable model in a scikit-learn pipeline, and evaluate with ROC AUC plus precision and recall at a threshold set by how many orders the credit team can review. Then I'd check that the drivers make business sense and agree with the EDA."

    **Mini project:** Train the same pipeline to predict **late delivery** (delivered orders, `delivery_days > promised_days`) using order-time features. Report baseline, ROC AUC with a time-based split, and the top drivers.
