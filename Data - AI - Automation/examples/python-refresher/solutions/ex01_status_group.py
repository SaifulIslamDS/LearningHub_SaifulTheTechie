"""Exercise 01 — a function that groups statuses, and a loop that counts open orders."""


def status_group(status: str) -> str:
    if status in ("Delivered", "Cancelled"):
        return "Closed"
    return "Open"


statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled",
    "Delivered",
    "Delivered",
    "Shipped",
    "Delivered",
    "Pending",
    "Delivered",
    "Delivered",
    "Shipped",
]
open_count = 0
for s in statuses:
    if status_group(s) == "Open":
        open_count += 1
print("Open orders:", open_count)  # 3
