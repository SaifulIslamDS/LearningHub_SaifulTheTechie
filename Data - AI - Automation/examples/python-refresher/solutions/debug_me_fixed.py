"""Debugging exercise — both bugs fixed."""

orders = [
    {"order_id": 1, "value": 420.0, "status": "Delivered"},
    {"order_id": 4, "value": 240.0, "status": "Cancelled"},
    {"order_id": 7, "value": 320.0, "status": "Shipped"},
    {"order_id": 9, "value": 810.0, "status": "Pending"},
]


def average_order_value(rows):
    # Bug 1 fixed: skip cancelled orders (the business rule in the comment)
    total = 0
    count = 0
    for row in rows:
        if row["status"] == "Cancelled":
            continue
        total += row["value"]
        count += 1
    return total / count


def open_orders(rows):
    # Bug 2 fixed: the key is "status", not "Status"
    return [r["order_id"] for r in rows if r["status"] in ("Shipped", "Pending")]


print("Average order value:", round(average_order_value(orders), 2))  # 516.67
print("Open orders:", open_orders(orders))  # [7, 9]
