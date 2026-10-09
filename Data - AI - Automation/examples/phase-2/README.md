# Data, AI & Automation Path — Phase 2 scripts (Data Science)

One script per lesson. Each script is split into cells (`# %%`), so you can run it top to bottom or cell by cell in VS Code / Jupyter. The `data/` folder holds the 2025 practice data (synthetic, fixed seed: your numbers should match the lessons exactly).

## Set up once

```bash
uv init --bare
uv add numpy pandas matplotlib seaborn scipy statsmodels scikit-learn polars duckdb plotly pyarrow
uv run 01_numpy_arrays.py
```

Charts are saved to `charts/`; results of script 21 to `results/`.

| Script | Module · lesson |
|---|---|
| `01_numpy_arrays.py`, `02_numpy_vectorized.py` | NumPy |
| `03`–`06_pandas_*.py` | pandas: basics, cleaning, merge & groupby, pivot & datetime |
| `07_polars.py`, `08_duckdb_larger_data.py`, `make_big_data.py` | Polars & DuckDB (make_big_data creates a large local file) |
| `09`–`10_eda_*.py` | EDA |
| `11`–`12_stats_*.py` | Statistics |
| `13`–`14_ab_*.py` | Experimentation & A/B testing |
| `15`–`16_viz_*.py` | Visualization (`chart_style.py` = shared colours and helpers) |
| `17`–`19_ml_*.py` | ML foundations (`ml_data.py` = shared data preparation) |
| `20`–`21_research_*.py` / `_reproducibility_*.py` | Research thinking |

Every script ends with the solution to the lesson's *Try it yourself* exercise. Try it first!
