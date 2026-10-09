"""Exercise 02 — net revenue per customer, biggest first."""

orders = [
    # (order_id, customer, region, value, status)
    (1, "Rahim Traders", "Dhaka", 420.0, "Delivered"),
    (2, "Karim Garments", "Chattogram", 200.0, "Delivered"),
    (3, "Nova Apparel", "Dhaka", 1560.0, "Delivered"),
    (4, "Rahim Traders", "Dhaka", 240.0, "Cancelled"),
    (5, "Delta Knit", "Gazipur", 1260.0, "Delivered"),
    (6, "Karim Garments", "Chattogram", 680.0, "Delivered"),
    (7, "Nova Apparel", "Dhaka", 320.0, "Shipped"),
    (8, "Delta Knit", "Gazipur", 1260.0, "Delivered"),
    (9, "Sun Fashion", "Narayanganj", 810.0, "Pending"),
    (10, "Rahim Traders", "Dhaka", 870.0, "Delivered"),
    (11, "Sun Fashion", "Narayanganj", 420.0, "Delivered"),
    (12, "Karim Garments", "Chattogram", 1275.0, "Shipped"),
]

revenue: dict[str, float] = {}
for _, customer, _, value, status in orders:
    if status != "Cancelled":
        revenue[customer] = revenue.get(customer, 0) + value

for customer, total in sorted(revenue.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{customer:<16}{total:>8.2f}")
