"""Lesson: lists, dictionaries, sets and tuples — with the 12 practice orders."""

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

# List comprehension: keep non-cancelled orders
net = [o for o in orders if o[4] != "Cancelled"]
print("Net orders:", len(net))

# Tuple unpacking
order_id, customer, region, value, status = orders[0]
print(order_id, customer, value)

# Dictionary: revenue per region (like SQL GROUP BY)
revenue_by_region: dict[str, float] = {}
for _, _, region, value, _ in net:
    revenue_by_region[region] = revenue_by_region.get(region, 0) + value
print(revenue_by_region)

# Sort the dictionary by value, biggest first
for region, rev in sorted(
    revenue_by_region.items(), key=lambda kv: kv[1], reverse=True
):
    print(f"{region:<12}{rev:>8.2f}")

# Set: unique customers
customers = {o[1] for o in orders}
print(len(customers), "customers:", sorted(customers))

# Dict comprehension: customer -> number of orders
counts = {c: sum(1 for o in orders if o[1] == c) for c in sorted(customers)}
print(counts)
