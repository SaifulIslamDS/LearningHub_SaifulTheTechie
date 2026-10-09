---
title: "pandas Pivot & Datetime: Analyse Data Over Time"
order: 4
summary: "Parse dates, extract months and weekdays, resample to monthly totals with month-on-month growth, build pivot tables, smooth with rolling averages and do date arithmetic."
level: Beginner
time: "50 min"
topics: ["Pivot", "Datetime"]
prerequisites: ["phase-2/pandas/03-merge-groupby"]
keywords: [datetime, to_datetime, parse_dates, dt accessor, dt.month, day_name, resample, month end, pct_change, rolling, rolling average, pivot_table, margins, melt, timedelta, time series, seasonality]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv]
resources:
  - title: "Time series / date functionality"
    url: "https://pandas.pydata.org/docs/user_guide/timeseries.html"
    source: "pandas official docs"
    note: "Parsing, resampling, offsets such as ME (month end) and rolling windows."
  - title: "Reshaping and pivot tables"
    url: "https://pandas.pydata.org/docs/user_guide/reshaping.html"
    source: "pandas official docs"
    note: "pivot_table, melt, stack and unstack."
  - title: "Windowing operations"
    url: "https://pandas.pydata.org/docs/user_guide/window.html"
    source: "pandas official docs"
    note: "Rolling and expanding calculations."
---

## What is it?

- **Datetime** tools turn text like `"2025-01-01"` into real dates, so you can extract parts (month, weekday), add days, and group by time.
- **`resample`** groups a time-indexed series into periods (days, weeks, month ends).
- **`pivot_table`** is Excel's PivotTable in code: rows × columns × an aggregate. **`melt`** does the reverse (wide → long), like Power Query's *Unpivot*.

!!! job "Why it matters at work"
    Almost every business question has a time dimension: "how did we do this month?", "is this a seasonal dip?", "are deliveries getting slower?". Forecasting (Phase 4) and dashboards (Phase 1) both start from clean monthly and daily series built exactly like this.

The script is `06_pandas_pivot_datetime.py`.

## Example 1: parse dates and extract parts

```python
import pandas as pd

orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
print(orders["order_date"].dtype, orders["order_date"].min().date(), orders["order_date"].max().date())
net = orders[orders["status"] != "Cancelled"].copy()
net["month"] = net["order_date"].dt.month
net["weekday"] = net["order_date"].dt.day_name()
net["quarter"] = net["order_date"].dt.quarter
print(net[["order_date", "month", "weekday", "quarter"]].head(3))
```

```text
datetime64[us] 2025-01-01 2025-12-31
  order_date  month    weekday  quarter
0 2025-01-01      1  Wednesday        1
2 2025-01-01      1  Wednesday        1
3 2025-01-01      1  Wednesday        1
```

`parse_dates` converts while reading (`datetime64`); `.dt` gives access to date parts. (Row 1 is missing because it was a cancelled order.)

## Example 2: a weekly pattern

```python
days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
print(net["weekday"].value_counts().reindex(days))
```

```text
weekday
Saturday     399
Sunday       707
Monday       712
Tuesday      700
Wednesday    732
Thursday     673
Friday        40
Name: count, dtype: int64
```

Friday is the weekend in Bangladesh and Saturday is a half day. `reindex(days)` puts the days in business order instead of by count.

## Example 3: monthly revenue and month-on-month growth

```python
monthly = net.set_index("order_date")["revenue"].resample("ME").sum()
mom = monthly.pct_change() * 100
print(pd.DataFrame({"revenue": monthly.round(0), "mom_pct": mom.round(1)}).to_string())
```

```text
             revenue  mom_pct
order_date
2025-01-31  330192.0      NaN
2025-02-28  335736.0      1.7
2025-03-31  324249.0     -3.4
2025-04-30  336682.0      3.8
2025-05-31  444538.0     32.0
2025-06-30  324326.0    -27.0
2025-07-31  547579.0     68.8
2025-08-31  499336.0     -8.8
2025-09-30  606666.0     21.5
2025-10-31  637897.0      5.1
2025-11-30  614879.0     -3.6
2025-12-31  476277.0    -22.5
```

- `"ME"` = month end (each row is labelled with the last day of its month).
- `pct_change()` compares each month with the previous one: the same MoM measure you built in DAX.
- The story: a slow first half, dips in **April and June** (Eid holidays), and a **September–November peak** (export season).

## Example 4: pivot table

```python
pt = net.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="sum",
                     margins=True, margins_name="Total")
print((pt / 1000).round(0))
```

```text
quarter          1       2       3       4   Total
region
Chattogram   359.0   409.0   618.0   671.0  2057.0
Dhaka        313.0   382.0   562.0   579.0  1835.0
Gazipur      111.0   121.0   157.0   183.0   572.0
Khulna       118.0    80.0   125.0   107.0   430.0
Narayanganj   90.0   113.0   192.0   189.0   584.0
Total        990.0  1106.0  1654.0  1729.0  5478.0
```

Revenue in thousands. `margins=True` adds totals (5,478 thousand = the known 5,478,357.79). Khulna is the only region that doesn't grow in the second half.

## Example 5: rolling averages smooth the noise

Daily orders around Eid al-Fitr 2025 (about 31 March):

```python
daily = net.set_index("order_date").resample("D")["order_id"].count()
roll = daily.rolling(7).mean()
print(daily.loc["2025-03-27":"2025-04-09"].to_string())
print(roll.loc["2025-04-05":"2025-04-09"].round(1).to_string())
```

```text
order_date
2025-03-27    13
2025-03-28     1
2025-03-29     0
2025-03-30     1
2025-03-31     2
2025-04-01     1
2025-04-02     0
2025-04-03     2
2025-04-04     0
2025-04-05     1
2025-04-06     2
2025-04-07    16
2025-04-08    16
2025-04-09     5
Freq: D
order_date
2025-04-05    1.0
2025-04-06    1.1
2025-04-07    3.1
2025-04-08    5.3
2025-04-09    6.0
Freq: D
```

A 7-day rolling mean averages each day with the 6 before it, so the holiday shows as a smooth dip and recovery rather than a jagged line. Days with no orders appear as 0 because `resample("D")` creates every calendar day.

## Example 6: date arithmetic

```python
delivered = net[net["status"] == "Delivered"].copy()
delivered["delivered_on"] = delivered["order_date"] + pd.to_timedelta(delivered["delivery_days"], unit="D")
delivered["late"] = delivered["delivery_days"] > delivered["promised_days"]
print(delivered[["order_date", "delivery_days", "delivered_on", "promised_days", "late"]].head(3))
print(delivered.groupby(delivered["order_date"].dt.month)["late"].mean().mul(100).round(1).to_dict())
```

```text
  order_date  delivery_days delivered_on  promised_days   late
0 2025-01-01            3.0   2025-01-04              5  False
2 2025-01-01            2.0   2025-01-03              3  False
3 2025-01-01            6.0   2025-01-07              6  False
{1: 13.3, 2: 13.7, 3: 15.4, 4: 19.1, 5: 16.7, 6: 18.2, 7: 18.6, 8: 13.0, 9: 16.7, 10: 50.5, 11: 48.4, 12: 14.2}
```

About **half of all deliveries were late in October and November**, compared with 13–19% in other months. The peak season strains logistics: a finding worth more than any chart of revenue.

## Example 7: melt (wide → long)

```python
wide = pt.drop(index="Total", columns="Total")
long = wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="revenue")
print(long.head(4))
```

```text
       region quarter    revenue
0  Chattogram       1  359125.38
1       Dhaka       1  312600.21
2     Gazipur       1  111065.46
3      Khulna       1  117816.62
```

Long format (one row per region–quarter) is what plotting libraries, databases and models prefer.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Dates left as text | `.dt` fails; months sort as text | `parse_dates=` or `pd.to_datetime` |
| Day-first dates read as month-first | 05/01 becomes 1 May | `pd.to_datetime(s, format="%d/%m/%Y")` |
| `groupby(month)` across several years | January 2024 and 2025 merged | Group by `dt.to_period("M")`, or resample |
| Rolling over missing days | A "7-day" window covers 9 calendar days | `resample("D")` first, so every day exists |
| Reading a pivot's `NaN` as zero | Wrong conclusions | `fill_value=0` only when "none" really means zero |

## Try it yourself

**Task:** Build a pivot of the **late-delivery rate (%)** by region (rows) and quarter (columns). Which region–quarter is worst, and which region is most reliable?

<details markdown="1">
<summary>Show a hint</summary>

`late` is True/False; the mean of True/False is the share of True. Use `aggfunc="mean"` and multiply by 100.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
late_pt = delivered.pivot_table(index="region", columns="quarter", values="late", aggfunc="mean") * 100
print(late_pt.round(1))
```

```text
quarter         1     2     3     4
region
Chattogram   15.7  23.3  22.9  39.5
Dhaka         7.2   9.7   7.7  36.5
Gazipur      19.4  17.2  17.2  49.7
Khulna       28.8  18.3  19.2  39.7
Narayanganj  11.0  25.3  16.2  51.6
```

Narayanganj in Q4 is worst (51.6% late), followed by Gazipur Q4. Dhaka is the most reliable for most of the year, but even Dhaka jumps to 36.5% in Q4: the peak-season problem affects every region.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `series.resample("ME").sum()` do?

1. Sorts the series by month
2. Totals the values for each calendar month, labelled by month end
3. Calculates a rolling sum

<details markdown="1"><summary>Show answer</summary>
**B.** The series needs a datetime index first.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. `monthly.pct_change()` for October shows 5.1. What does it mean?

1. October revenue was 5.1% of the year
2. October revenue was 5.1% higher than September
3. October had 5.1% more orders than average

<details markdown="1"><summary>Show answer</summary>
**B.** Month-on-month growth.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which function turns a wide table (one column per quarter) into a long table?

1. `pivot_table`
2. `melt`
3. `resample`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Convert dates on load (`parse_dates`), then use `.dt` for month, weekday and quarter.
- `resample("ME")` + `pct_change()` gives monthly totals and MoM growth; `rolling(7)` smooths daily noise.
- `pivot_table(index, columns, values, aggfunc, margins=True)` = an Excel pivot; `melt` reverses it.
- Date arithmetic with `to_timedelta` answers operational questions such as late deliveries.

!!! job "Job-ready check"
    **Interview question:** *"Monthly revenue dropped 27% in June. How would you investigate?"*

    **Strong answer:** "First check it's real: same data cut-off, no missing days, cancellations excluded. Then look at daily orders with a rolling average to see whether it's a short gap or a trend. Here the dip lines up with the Eid holiday week, so I'd compare with last year's Eid period and check whether the lost orders came back in July before calling it a problem."

    **Mini project:** Produce a one-page "2025 time review": monthly revenue with MoM %, the Eid dips, the Q4 late-delivery problem by region, and one recommendation for logistics planning in next year's peak season.
