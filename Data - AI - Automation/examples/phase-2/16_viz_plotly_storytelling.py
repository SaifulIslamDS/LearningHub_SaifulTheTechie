"""Phase 2 · Visualization · Plotly (interactive) and analytical storytelling."""

# %% 0. Setup
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from chart_style import CHARTS, INK_2, MUTED, PALETTE, apply_style, save

orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
net = orders[orders["status"] != "Cancelled"].copy()
net["month"] = net["order_date"].dt.to_period("M").dt.to_timestamp()

# %% 1. Plotly Express: an interactive chart in one call (hover, zoom, click legend to hide)
monthly = net.groupby(["month", "segment"], as_index=False)["revenue"].sum()
fig = px.line(monthly, x="month", y="revenue", color="segment", markers=True,
              color_discrete_sequence=PALETTE,
              labels={"month": "", "revenue": "Net revenue", "segment": "Segment"},
              title="Garment factories drive the export-season peak")
fig.update_layout(template="simple_white", hovermode="x unified", legend_title_text="")
fig.update_yaxes(rangemode="tozero", tickformat=",.0f")
fig.update_xaxes(hoverformat="%B %Y", dtick="M2", tickformat="%b")
fig.update_traces(hovertemplate="%{y:,.0f}")                   # clean hover text: just the value
CHARTS.mkdir(exist_ok=True)
fig.write_html(CHARTS / "viz_plotly_monthly.html", include_plotlyjs="cdn")   # small file; needs internet to view
print("wrote charts/viz_plotly_monthly.html")

# %% 2. Plotly: scatter with hover details for exploring customers
cust = net.groupby(["customer_id", "segment", "region"], as_index=False).agg(
    orders=("order_id", "size"), revenue=("revenue", "sum"))
fig2 = px.scatter(cust, x="orders", y="revenue", color="segment", size="revenue", hover_name="customer_id",
                  hover_data={"region": True, "revenue": ":,.0f"}, log_y=True, color_discrete_sequence=PALETTE,
                  title="Customers: number of orders vs total revenue (hover for details)")
fig2.update_layout(template="simple_white")
fig2.write_html(CHARTS / "viz_plotly_customers.html", include_plotlyjs="cdn")
print("wrote charts/viz_plotly_customers.html")
print(cust.nlargest(3, "revenue").round(0).to_string(index=False))

# %% 3. Storytelling: the same data, before and after
apply_style()
reg = net.pivot_table(index="month", columns="region", values="revenue", aggfunc="sum") / 1000
q4 = reg.loc["2025-10-01":"2025-12-01"].sum()
h1 = reg.loc["2025-01-01":"2025-06-01"].sum()
growth = (q4 / 3) / (h1 / 6) - 1                 # monthly average Q4 vs first half
print((growth * 100).round(0).sort_values(ascending=False))

# BEFORE: default-style chart — every series coloured, legend, descriptive title
fig, ax = plt.subplots(figsize=(8, 3.6))
for i, col in enumerate(reg.columns):
    ax.plot(reg.index, reg[col], marker="o", label=col, color=["red", "green", "blue", "orange", "purple"][i])
ax.set_title("Monthly Revenue by Region 2025", loc="center")
ax.legend(loc="upper left", fontsize=8)
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
save(fig, "story_before.png")

# AFTER: one message, one highlight, direct labels, an action title
focus = growth.idxmin()
fig, ax = plt.subplots(figsize=(8, 3.6))
label_y = reg.iloc[-1].sort_values()                       # end values, low to high
for i in range(1, len(label_y)):                            # keep direct labels at least 14k apart
    label_y.iloc[i] = max(label_y.iloc[i], label_y.iloc[i - 1] + 14)
for col in reg.columns:
    is_focus = col == focus
    ax.plot(reg.index, reg[col], color=PALETTE[1] if is_focus else MUTED, linewidth=2.6 if is_focus else 1.2,
            zorder=3 if is_focus else 2)
    ax.text(reg.index[-1] + pd.Timedelta(days=8), label_y[col], col, va="center", fontsize=9,
            color=PALETTE[1] if is_focus else INK_2, fontweight="bold" if is_focus else "normal")
ax.set_title(f"{focus} missed the export-season boom: Q4 only {growth[focus]:+.0%} vs H1")
ax.set_ylabel("Net revenue (thousands)")
ax.set_ylim(0, None)
ax.set_xlim(reg.index[0] - pd.Timedelta(days=10), reg.index[-1] + pd.Timedelta(days=60))
ax.set_xticks(reg.index[::2])
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
ax.grid(axis="x", visible=False)
save(fig, "story_after.png")

# %% Try it yourself — solution: an interactive bar chart of revenue by product, sorted
prod = net.groupby(["product", "category"], as_index=False)["revenue"].sum().sort_values("revenue")
fig3 = px.bar(prod, x="revenue", y="product", color="category", orientation="h", color_discrete_sequence=PALETTE,
              title="Revenue by product, 2025")
fig3.update_layout(template="simple_white", yaxis={"categoryorder": "total ascending"})
fig3.write_html(CHARTS / "viz_plotly_products.html", include_plotlyjs="cdn")
print(prod.tail(3).round(0).to_string(index=False))
