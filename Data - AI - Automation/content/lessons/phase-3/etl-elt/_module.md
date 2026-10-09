**ETL / ELT** is how a data team turns raw source data into trustworthy tables that can be reused every day. The hard part is not copying data once. The hard part is making the pipeline **modular, incremental, idempotent and replayable** so retries, late data and source changes do not create duplicates or silent gaps.

!!! tip "Setup"
    - Download [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip) and unzip it.
    - This module uses the existing `data/orders_2025.csv` plus a tiny deterministic CDC event log, `data/orders_cdc_events.jsonl`.
    - Run: `python 14_modular_incremental_pipeline.py`, then `python 15_cdc_replay.py`.
    - Only `pandas` is required for these two scripts. Generated demo state is written under `results/`, which you can delete and rebuild at any time.

**By the end of this module you can:** split a pipeline into extract/transform/load functions, choose ETL vs ELT, track a watermark, load only new data, make retries safe with an upsert, explain CDC events, replay an ordered change log, and resume from a checkpoint after a failure.
