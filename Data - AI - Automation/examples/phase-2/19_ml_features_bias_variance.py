"""Phase 2 · ML Foundations · Feature engineering and the bias/variance trade-off."""

# %% 0. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from chart_style import INK_2, PALETTE, apply_style, save
from ml_data import CATEGORICAL, NUMERIC, load

apply_style()
df = load()
y = df["cancelled"]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def logistic(cat, num):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat), ("num", StandardScaler(), num)])
    return Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=2000))])


# %% 1. Feature engineering: turn raw columns into signals the model can use
df["log_revenue"] = np.log10(df["revenue"])                      # tame the long tail
df["large_order"] = (df["revenue"] > 3000).astype(int)            # business rule: big orders behave differently
df["credit_band"] = df["credit_days"].map({0: "cash", 15: "15d", 30: "30d", 60: "60d"})   # non-linear effect
df["peak_season"] = df["month"].isin([9, 10, 11]).astype(int)
df["weekday"] = df["order_date"].dt.day_name()

base_cols = CATEGORICAL + NUMERIC
eng_cat = CATEGORICAL + ["credit_band"]
eng_num = ["log_revenue", "large_order", "discount", "promised_days", "peak_season"]

variants = [
    ("11 raw features", CATEGORICAL, NUMERIC),
    ("engineered set", eng_cat, eng_num),
    ("3 domain features", ["segment", "channel"], ["credit_days"]),      # what the EDA pointed to
]
for name, cat, num in variants:
    scores = cross_val_score(logistic(cat, num), df[cat + num], y, cv=cv, scoring="roc_auc")
    print(f"{name:18s} 5-fold ROC AUC {scores.mean():.3f} ± {scores.std():.3f}")
print(df.groupby("large_order")["cancelled"].agg(["mean", "size"]).round(3))

# %% 2. Which engineered features carry the signal?
m = logistic(eng_cat, eng_num).fit(df[eng_cat + eng_num], y)
coef = pd.Series(m.named_steps["clf"].coef_[0], index=m.named_steps["prep"].get_feature_names_out())
print(coef.loc[["cat__credit_band_cash", "cat__credit_band_60d", "num__large_order", "cat__segment_Retailer",
                "cat__channel_Phone"]].round(2))

# %% 3. Bias vs variance: decision trees of increasing depth
X = pd.get_dummies(df[eng_cat + eng_num], columns=eng_cat, dtype=int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
rows = []
for depth in [1, 2, 3, 4, 5, 6, 8, 10, 14, 20]:
    tree = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=1, random_state=0).fit(X_tr, y_tr)
    rows.append({"depth": depth,
                 "train_auc": roc_auc_score(y_tr, tree.predict_proba(X_tr)[:, 1]),
                 "test_auc": roc_auc_score(y_te, tree.predict_proba(X_te)[:, 1])})
curve = pd.DataFrame(rows).round(3)
print(curve.to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(curve["depth"], curve["train_auc"], marker="o", color=PALETTE[0], label="Training data")
ax.plot(curve["depth"], curve["test_auc"], marker="o", color=PALETTE[1], label="Test data (unseen)")
best = curve.loc[curve["test_auc"].idxmax()]
ax.axvline(best["depth"], color=INK_2, linestyle="--", linewidth=1)
ax.text(best["depth"] + 0.3, 0.545, "best test score", color=INK_2, fontsize=9)
ax.text(0.8, 0.475, "underfitting\n(high bias)", color=INK_2, fontsize=9)
ax.text(13, 0.80, "overfitting\n(high variance)", color=INK_2, fontsize=9)
ax.set_title("Deeper trees memorise the training data and do worse on new orders")
ax.set_xlabel("Tree depth (model complexity)")
ax.set_xticks([1, 2, 4, 6, 8, 10, 14, 20])
ax.set_ylabel("ROC AUC")
ax.set_ylim(0.45, 1.02)
ax.legend(loc="lower right")
save(fig, "ml_bias_variance.png")

# %% 4. Same complexity knob, chosen properly with cross-validation on the training data only
for depth in [2, 3, 4, 8]:
    s = cross_val_score(DecisionTreeClassifier(max_depth=depth, random_state=0), X_tr, y_tr, cv=cv, scoring="roc_auc")
    print(f"depth {depth}: CV ROC AUC {s.mean():.3f} ± {s.std():.3f}")

# %% Try it yourself — solution: does min_samples_leaf tame a deep tree?
for leaf in [1, 20, 50]:
    t = DecisionTreeClassifier(max_depth=14, min_samples_leaf=leaf, random_state=0).fit(X_tr, y_tr)
    print(f"depth 14, min_samples_leaf={leaf:>2}: train {roc_auc_score(y_tr, t.predict_proba(X_tr)[:, 1]):.3f}"
          f" | test {roc_auc_score(y_te, t.predict_proba(X_te)[:, 1]):.3f}")
