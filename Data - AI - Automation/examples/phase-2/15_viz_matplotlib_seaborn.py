"""Phase 2 · Visualization · Matplotlib and seaborn."""

# %% 0. Setup
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from chart_style import INK_2, PALETTE, apply_style, save

apply_style()
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
net = orders[orders["status"] != "Cancelled"].copy()
net["month"] = net["order_date"].dt.to_period("M").dt.to_timestamp()

# %% 1. Matplotlib anatomy: one Figure, one or more Axes, then methods on each Axes
monthly = net.groupby("month")["revenue"].sum() / 1000
fig, ax = plt.subplots(figsize=(8, 3.6))                 # Figure = the canvas, Axes = one chart
ax.plot(monthly.index, monthly.values, marker="o", color=PALETTE[0])
ax.set_title("Revenue climbs into the Sep–Nov export season")
ax.set_ylabel("Net revenue (thousands)")
ax.set_ylim(0, None)                                     # bars and totals start at zero
peak = monthly.idxmax()
ax.annotate(f"Peak: {monthly.max():.0f}k in {peak:%B}", (peak, monthly.max()), xytext=(0, -85), ha="center",
            textcoords="offset points", arrowprops={"arrowstyle": "->", "color": INK_2}, color=INK_2)
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
save(fig, "viz_monthly_line.png")
print(monthly.round(1).tail(3))

# %% 2. Small multiples with subplots: one panel per region, shared y-axis
regions = net.groupby("region")["revenue"].sum().sort_values(ascending=False).index
fig, axes = plt.subplots(1, len(regions), figsize=(12, 2.8), sharey=True)
for ax, region in zip(axes, regions):
    m = net[net["region"] == region].groupby("month")["revenue"].sum() / 1000
    ax.bar(m.index, m.values, width=20, color=PALETTE[0])
    ax.set_title(region, fontsize=11)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
    ax.tick_params(axis="x", labelsize=8, rotation=90)
axes[0].set_ylabel("Revenue (k)")
fig.suptitle("Every region peaks in the export season; Chattogram and Dhaka are the largest", x=0.01, y=1.06,
             ha="left", fontweight="bold")
save(fig, "viz_small_multiples.png")

# %% 3. Seaborn: statistical charts from a DataFrame in one call
delivered = net[net["status"] == "Delivered"].copy()
delivered["late"] = delivered["delivery_days"] > delivered["promised_days"]
order_regions = delivered.groupby("region")["late"].mean().sort_values().index

fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
sns.barplot(data=delivered, x="late", y="region", order=order_regions, errorbar=("ci", 95), color=PALETTE[0],
            ax=axes[0])                                          # mean of True/False = late rate, with 95% CI
axes[0].set_title("Late-delivery rate by region (95% CI)")
axes[0].set_xlabel("Share of deliveries later than promised")
axes[0].set_ylabel("")
sns.boxplot(data=delivered, x="delivery_days", y="region", order=order_regions, color=PALETTE[0],
            fliersize=2, ax=axes[1])
axes[1].set_title("Delivery days: Khulna is slowest and least predictable")
axes[1].set_xlabel("Delivery days")
axes[1].set_ylabel("")
save(fig, "viz_seaborn_late.png")

# %% 4. Seaborn heatmap: revenue by weekday and month
net["weekday"] = net["order_date"].dt.day_name().str[:3]
grid = net.pivot_table(index="weekday", columns=net["order_date"].dt.month, values="revenue", aggfunc="sum") / 1000
grid.columns = pd.to_datetime(grid.columns.astype(str), format="%m").strftime("%b")
grid = grid.reindex(["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"])
fig, ax = plt.subplots(figsize=(10, 3.4))
sns.heatmap(grid, cmap="Blues", annot=True, fmt=".0f", annot_kws={"size": 8}, cbar_kws={"label": "Revenue (k)"},
            linewidths=0.5, linecolor="#fcfcfb", ax=ax)
ax.set_title("Fridays are empty and Saturdays quieter (Nov Sat: one 44k bulk order)")
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(axis="y", rotation=0)
ax.grid(False)
save(fig, "viz_heatmap_weekday.png")
print(grid.round(0).loc[["Fri", "Sat", "Sun"], ["Sep", "Oct", "Nov"]])

# %% Try it yourself — solution: revenue share by category per month, as a 100% stacked bar
share = net.pivot_table(index="month", columns="category", values="revenue", aggfunc="sum")
share = share.div(share.sum(axis=1), axis=0) * 100
fig, ax = plt.subplots(figsize=(9, 3.4))
bottom = 0
for i, cat in enumerate(["Fabric", "Yarn", "Trims"]):
    ax.bar(share.index, share[cat], bottom=bottom, width=20, color=PALETTE[i], label=cat)
    bottom = bottom + share[cat]
ax.set_title("The product mix is stable all year")
ax.set_ylabel("Share of revenue (%)")
ax.legend(ncol=3, loc="upper left", bbox_to_anchor=(0, -0.12))
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
save(fig, "viz_mix_stacked.png")
print(share.round(1).agg(["min", "max"]))
