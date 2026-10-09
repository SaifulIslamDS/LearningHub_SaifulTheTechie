Real data arrives messy: extra spaces, mixed capitals, dates in the wrong format, duplicates, and one file per month. **Power Query** cleans and combines it with recorded steps that you set up **once** and then refresh every month, with no manual copy-pasting.

!!! tip "Where to find Power Query"
    - **Excel (Windows):** **Data → Get Data**, or **Data → From Text/CSV**. The editor opens with **Transform Data**.
    - **Power BI Desktop:** **Home → Get data**, then **Transform data**. It is the same Power Query engine and the same M language.
    - **Excel for Mac** also includes Power Query, with fewer options. The steps in these lessons are shown for Windows.

!!! note "Practice files for this module"
    - [orders_raw.csv](../../../downloads/orders_raw.csv): a messy export of the same 12 orders (14 rows).
    - [customers.csv](../../../downloads/customers.csv) and [orders.csv](../../../downloads/orders.csv): for merging.
    - [orders_2026-01.csv](../../../downloads/monthly/orders_2026-01.csv), [orders_2026-02.csv](../../../downloads/monthly/orders_2026-02.csv), [orders_2026-03.csv](../../../downloads/monthly/orders_2026-03.csv): one file per month. Put them in one folder, e.g. `C:\Practice\monthly\`.
    - [targets_wide.csv](../../../downloads/targets_wide.csv): sales targets with one column per month.

**By the end of this module you can:** clean a messy export into a tidy table, combine tables side by side (merge) and on top of each other (append), turn wide tables into long ones (unpivot), and load a whole folder of monthly files with one refresh.
