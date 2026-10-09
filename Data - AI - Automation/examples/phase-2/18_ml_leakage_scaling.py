"""Phase 2 · ML Foundations · Leakage and scaling."""

# %% 0. Setup
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml_data import CATEGORICAL, NUMERIC, ORDER_TIME_FEATURES, load

df = load()
y = df["cancelled"]
train_idx, test_idx = train_test_split(df.index, test_size=0.25, stratify=y, random_state=42)


def auc(features, numeric, model=None, data=df):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), [c for c in features if c in CATEGORICAL]),
                              ("num", StandardScaler(), numeric)])
    pipe = Pipeline([("prep", prep), ("clf", model or LogisticRegression(max_iter=1000))])
    pipe.fit(data.loc[train_idx, features], y[train_idx])
    return roc_auc_score(y[test_idx], pipe.predict_proba(data.loc[test_idx, features])[:, 1])


print(f"honest model (order-time features only): ROC AUC {auc(ORDER_TIME_FEATURES, NUMERIC):.3f}")

# %% 1. Target leakage: a column that is only filled in AFTER the outcome is known
df["delivery_known"] = df["delivery_days"].notna().astype(int)        # delivered orders have delivery days...
print(pd.crosstab(df["delivery_known"], df["cancelled"]))
leaky = ORDER_TIME_FEATURES + ["delivery_known"]
print(f"with delivery_known: ROC AUC {auc(leaky, NUMERIC + ['delivery_known']):.3f}  <- too good to be true")

# %% 2. Leakage through an aggregate: customer cancellation rate computed on ALL orders (incl. test)
rate_all = df.groupby("customer_id")["cancelled"].transform("mean")
df["cust_rate_leaky"] = rate_all
print(f"customer rate from all data: ROC AUC {auc(ORDER_TIME_FEATURES + ['cust_rate_leaky'], NUMERIC + ['cust_rate_leaky']):.3f}")

# the honest version: compute the rate from TRAINING orders only, then map it onto test orders
train_rate = df.loc[train_idx].groupby("customer_id")["cancelled"].mean()
df["cust_rate"] = df["customer_id"].map(train_rate).fillna(y[train_idx].mean())
print(f"customer rate from train only: ROC AUC {auc(ORDER_TIME_FEATURES + ['cust_rate'], NUMERIC + ['cust_rate']):.3f}")

# %% 3. Scaling: features on very different scales
print(df[["quantity", "unit_price", "discount", "credit_days"]].describe().loc[["mean", "std", "max"]].round(2))

# k-nearest neighbours measures distances, so unscaled big numbers (quantity) dominate
num_only = ["quantity", "unit_price", "discount", "revenue", "credit_days", "promised_days"]
X_tr, X_te = df.loc[train_idx, num_only], df.loc[test_idx, num_only]
knn_raw = KNeighborsClassifier(n_neighbors=50).fit(X_tr, y[train_idx])
knn_scaled = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=50))]).fit(X_tr, y[train_idx])
print(f"KNN without scaling: ROC AUC {roc_auc_score(y[test_idx], knn_raw.predict_proba(X_te)[:, 1]):.3f}")
print(f"KNN with scaling:    ROC AUC {roc_auc_score(y[test_idx], knn_scaled.predict_proba(X_te)[:, 1]):.3f}")

# %% 4. Scaling inside the pipeline = fitted on training data only
scaler = StandardScaler().fit(X_tr)
print("scaler learned from TRAIN:", {k: round(float(v), 2) for k, v in zip(num_only[:2], scaler.mean_[:2])})

# %% Try it yourself — solution: is `revenue` leakage? (No: it is known when the order is placed.)
print(f"without revenue: ROC AUC {auc([f for f in ORDER_TIME_FEATURES if f != 'revenue'], [n for n in NUMERIC if n != 'revenue']):.3f}")
