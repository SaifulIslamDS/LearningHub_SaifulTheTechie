"""Phase 3 · Data Quality · Great Expectations on the 2025 orders data.

Requires Great Expectations 1.24.0. This script is intentionally self-contained
and uses an ephemeral Data Context plus an in-memory pandas DataFrame.

Install for this lesson:
    python -m pip install "great_expectations==1.24.0"
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import great_expectations as gx

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "orders_2025.csv"


def main() -> None:
    df = pd.read_csv(SOURCE)
    context = gx.get_context(mode="ephemeral")

    data_source = context.data_sources.add_pandas(name="orders_pandas")
    data_asset = data_source.add_dataframe_asset(name="orders_2025")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_orders")

    suite = gx.ExpectationSuite(name="orders_quality_suite")
    suite = context.suites.add(suite)
    suite.add_expectation(gx.expectations.ExpectTableRowCountToEqual(value=4246))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="status",
            value_set=["Delivered", "Cancelled", "Shipped", "Pending"],
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="quantity", min_value=1, strict_min=False
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="discount", min_value=0, max_value=0.08
        )
    )

    validation_definition = gx.ValidationDefinition(
        data=batch_definition,
        suite=suite,
        name="orders_2025_validation",
    )
    validation_definition = context.validation_definitions.add(validation_definition)
    result = validation_definition.run(batch_parameters={"dataframe": df})

    stats = result.statistics
    print(
        f"GX validation: success {bool(result.success)} | "
        f"expectations {stats['successful_expectations']}/{stats['evaluated_expectations']} passed | "
        f"rows {len(df)}"
    )


if __name__ == "__main__":
    main()
