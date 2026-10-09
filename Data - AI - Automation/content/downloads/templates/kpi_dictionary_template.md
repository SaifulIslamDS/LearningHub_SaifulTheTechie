# KPI Dictionary — <project name>

One row per published measure. Keep this file next to the model and update it whenever a measure changes.

| KPI | Business definition | DAX measure | Format | Owner | Last reviewed |
|---|---|---|---|---|---|
| Net Revenue | Value of all orders except status Cancelled | `CALCULATE([Revenue], Orders[status] <> "Cancelled")` | Whole number | Head of Sales | YYYY-MM-DD |
| Achievement % | Net Revenue ÷ Target, at region × month grain | `DIVIDE([Net Revenue], [Target])` | % (1 dp) | Head of Sales | YYYY-MM-DD |
| | | | | | |

## Rules
- Every report uses these measures. No implicit "Sum of" fields.
- Changes are agreed with the owner, logged below, and announced to report users.

## Change log
| Date | Measure | Change | Approved by |
|---|---|---|---|
| | | | |
