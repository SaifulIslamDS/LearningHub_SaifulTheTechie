"""Debugging lesson: this script has TWO bugs. Find them with the debugger."""

orders = [
    {"order_id": 1, "value": 420.0, "status": "Delivered"},
    {"order_id": 4, "value": 240.0, "status": "Cancelled"},
    {"order_id": 7, "value": 320.0, "status": "Shipped"},
    {"order_id": 9, "value": 810.0, "status": "Pending"},
]


def average_order_value(rows):
    # Business rule: cancelled orders don't count
    total = 0
    count = 0
    for row in rows:
        total += row["value"]
        count += 1
    return total / count


def open_orders(rows):
    return [r["order_id"] for r in rows if r["Status"] in ("Shipped", "Pending")]


print("Average order value:", average_order_value(orders))
print("Open orders:", open_orders(orders))
