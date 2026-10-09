**Data Quality & Contracts** is where a pipeline stops asking only *“Did the job run?”* and starts asking *“Can we trust what it produced?”* This module turns assumptions about the textile-wholesaler orders into executable checks, framework-based expectations, a machine-readable data contract, and freshness rules that can stop stale or broken data before it reaches a dashboard or AI system.

!!! tip "Setup"
    - Download [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip) and unzip it.
    - The module reuses `data/orders_2025.csv`: 4,246 orders with the established Phase 3 known answers.
    - Run `python 16_data_quality_validation.py`, then `pytest -q test_16_data_quality_validation.py`.
    - `17_great_expectations_orders.py` uses Great Expectations 1.24.0 and is marked **RUN-BY-OWNER** in this build environment.
    - Run `python 18_data_contract_freshness.py` for the contract and freshness exercise. The downloadable contract is [orders_contract.schema.json](../../../downloads/phase-3/orders_contract.schema.json).

**By the end of this module you can:** translate business assumptions into validation rules, test data with pytest, explain Expectations and Expectation Suites, define a machine-readable data contract, measure source freshness, and decide when a failed check should warn, alert, or stop downstream publishing.
