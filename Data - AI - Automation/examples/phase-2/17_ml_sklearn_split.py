"""Phase 2 · ML Foundations · scikit-learn and the train/test split."""

# %% 0. Setup
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml_data import CATEGORICAL, NUMERIC, ORDER_TIME_FEATURES, load

df = load()
X, y = df[ORDER_TIME_FEATURES], df["cancelled"]
print(f"{len(df)} orders, {y.sum()} cancelled ({y.mean():.1%})")

# %% 1. Hold out a test set BEFORE doing anything else (stratify keeps the cancellation rate equal in both parts)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
print(f"train {len(X_train)} ({y_train.mean():.1%} cancelled) | test {len(X_test)} ({y_test.mean():.1%} cancelled)")

# %% 2. Baseline: always predict "not cancelled"
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(f"baseline accuracy {accuracy_score(y_test, dummy.predict(X_test)):.3f} "
      f"| ROC AUC {roc_auc_score(y_test, dummy.predict_proba(X_test)[:, 1]):.3f}")

# %% 3. A real model: preprocessing + logistic regression in ONE pipeline (fit on train only)
prep = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ("num", StandardScaler(), NUMERIC),
])
model = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=1000))])
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
print(f"logistic accuracy {accuracy_score(y_test, model.predict(X_test)):.3f} | ROC AUC {roc_auc_score(y_test, proba):.3f}")

# %% 4. Accuracy hides the problem: at the default 0.5 threshold, how many cancellations do we catch?
print(classification_report(y_test, model.predict(X_test), digits=3, zero_division=0))

# %% 5. A threshold that fits the business: flag the riskiest 10% of orders for a credit check
cut = np.quantile(proba, 0.90)
flag = proba >= cut
caught = (flag & (y_test == 1)).sum()
print(f"flag top 10% ({flag.sum()} orders): catches {caught} of {y_test.sum()} cancellations "
      f"({caught / y_test.sum():.0%}); precision {caught / flag.sum():.0%} vs base rate {y_test.mean():.0%}")

# %% 6. Time-based split: train on Jan–Sep, test on Oct–Dec (how the model will really be used)
is_train = df["order_date"] < "2025-10-01"
model.fit(X[is_train], y[is_train])
auc_time = roc_auc_score(y[~is_train], model.predict_proba(X[~is_train])[:, 1])
print(f"time-based split: train {is_train.sum()} orders, test {(~is_train).sum()} | ROC AUC {auc_time:.3f}")

# %% 7. What did the model learn? Largest coefficients (on standardised / one-hot features)
model.fit(X_train, y_train)
names = model.named_steps["prep"].get_feature_names_out()
coefs = pd.Series(model.named_steps["clf"].coef_[0], index=names).sort_values()
print(coefs.round(2).iloc[[0, 1, 2, -3, -2, -1]])

# %% Try it yourself — solution: a different random split gives a different score
for seed in [1, 2, 3]:
    Xa, Xb, ya, yb = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    print(seed, round(roc_auc_score(yb, model.fit(Xa, ya).predict_proba(Xb)[:, 1]), 3))
