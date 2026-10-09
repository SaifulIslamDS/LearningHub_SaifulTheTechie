**NumPy** is the engine under almost every Python data tool: pandas, scikit-learn, SciPy and many AI libraries store their numbers in NumPy arrays. You'll rarely write pure NumPy at work, but understanding arrays, vectorized maths and indexing makes everything that follows faster to learn and easier to debug.

!!! tip "Setup for all of Phase 2"
    - Download [data-science-scripts.zip](../../../downloads/phase-2/data-science-scripts.zip) and unzip it. It contains every lesson script (`01_numpy_arrays.py` …) and a `data/` folder with the 2025 practice data.
    - In that folder, create an environment once:

    ```bash
    uv init --bare
    uv add numpy pandas matplotlib seaborn scipy statsmodels scikit-learn polars duckdb plotly pyarrow
    ```

    - Run any script with `uv run 01_numpy_arrays.py`, or open it in VS Code and run it cell by cell (each `# %%` marks a cell, like a notebook).

**The Phase 2 data** is a synthetic but realistic year (2025) of the same textile-supplies wholesaler: 4,246 orders, 60 customers, 12 products and a checkout A/B test with 10,836 sessions. Patterns are planted on purpose, so there is something real to discover. See [Practice files](../../../practice-files.html#phase-2-data-science).

**By the end of this module you can:** create and reshape arrays, select data with indexes and boolean masks, and replace slow loops with fast vectorized calculations.
