"""Phase 2 · Research thinking · Reproducibility, evaluation and reporting."""

# %% 0. Setup
import hashlib
import json
import platform
from importlib.metadata import version
from pathlib import Path

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml_data import load

SEED = 2025
RESULTS = Path("results")


# %% 1. Record the environment and fingerprint the data
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


env = {"python": platform.python_version(), **{p: version(p) for p in ["numpy", "pandas", "scikit-learn"]}}
data_files = {p.name: sha256(p) for p in sorted(Path("data").glob("*_2025.csv"))}
print("environment:", env)
print("data fingerprints:", data_files)


# %% 2. The whole analysis as ONE function: inputs in, results out, randomness controlled by a seed
def analysis(seed: int) -> dict:
    df = load()
    train, test = df[df["order_date"] < "2025-10-01"], df[df["order_date"] >= "2025-10-01"]   # time-based split
    cat, num = ["segment", "channel"], ["credit_days"]
    model = Pipeline([
        ("prep", ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat), ("num", StandardScaler(), num)])),
        ("clf", LogisticRegression(max_iter=1000)),
    ]).fit(train[cat + num], train["cancelled"])
    proba = model.predict_proba(test[cat + num])[:, 1]
    y = test["cancelled"].to_numpy()

    rng = np.random.default_rng(seed)                       # bootstrap CI for the test ROC AUC
    boots = []
    for _ in range(1000):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() != y[i].max():
            boots.append(roc_auc_score(y[i], proba[i]))
    return {
        "question": "Can order-time data rank orders by cancellation risk (Oct-Dec 2025)?",
        "n_train": int(len(train)), "n_test": int(len(test)), "test_cancel_rate": round(float(y.mean()), 4),
        "baseline_auc": 0.5,
        "model_auc": round(float(roc_auc_score(y, proba)), 3),
        "auc_ci95": [round(float(np.percentile(boots, 2.5)), 3), round(float(np.percentile(boots, 97.5)), 3)],
        "seed": seed,
    }


# %% 3. Same seed -> identical results; different seed -> slightly different CI (that's the bootstrap noise)
r1, r2, r3 = analysis(SEED), analysis(SEED), analysis(SEED + 1)
print("run 1 == run 2:", r1 == r2)
print("seed 2025 CI:", r1["auc_ci95"], "| seed 2026 CI:", r3["auc_ci95"])

# %% 4. Save results WITH their provenance (what code, data and versions produced them)
RESULTS.mkdir(exist_ok=True)
report = {"results": r1, "data_sha256": data_files, "environment": env, "script": Path(__file__).name}
(RESULTS / "cancellation_model.json").write_text(json.dumps(report, indent=2))
print(json.dumps(r1, indent=2))

# %% Try it yourself — solution: how much does the result depend on the split date?
for cut in ["2025-09-01", "2025-10-01", "2025-11-01"]:
    df = load()
    tr, te = df[df["order_date"] < cut], df[df["order_date"] >= cut]
    m = Pipeline([("prep", ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["segment", "channel"]),
                                                ("num", StandardScaler(), ["credit_days"])])),
                  ("clf", LogisticRegression(max_iter=1000))]).fit(tr, tr["cancelled"])
    print(cut, len(te), round(roc_auc_score(te["cancelled"], m.predict_proba(te)[:, 1]), 3))
