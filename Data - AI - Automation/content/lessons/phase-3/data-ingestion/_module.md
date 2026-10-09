**Data ingestion** is the first step of every pipeline: getting data out of other systems (APIs, websites, files, databases) and into yours, completely, repeatably and politely. Most real ingestion bugs are about the edges: tokens, pages, rate limits, changing formats and silently missing rows.

!!! tip "Setup for all of Phase 3A"
    - Download [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip) and unzip it. It contains every lesson script, a `data/` folder (the 2025 data from Phase 2) and `mock_api.py`, a **practice API and website that runs on your own computer**, so you can practise real HTTP without accounts or keys.
    - In that folder, once: `uv init --bare` then `uv add requests beautifulsoup4 pandas pyarrow`.
    - Start the practice API in one terminal: `uv run mock_api.py`, and leave it running. Run the lesson scripts in a second terminal.

**By the end of this module you can:** call a REST API with a token, follow pagination, retry politely on rate limits, scrape a web page responsibly, and choose between CSV, JSON and Parquet for storing what you collect.
