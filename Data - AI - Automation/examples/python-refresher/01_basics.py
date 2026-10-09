"""Lesson: Variables, conditions, loops and functions."""

# Variables: a name pointing at a value
region = "Dhaka"
quantity = 300
unit_price = 5.20
value = quantity * unit_price
print(f"{region}: {quantity} x {unit_price:.2f} = {value:.2f}")


# A function with a condition (same rule as the SQL CASE lesson)
def size_band(order_value: float) -> str:
    if order_value >= 1000:
        return "Large"
    elif order_value >= 500:
        return "Medium"
    else:
        return "Small"


print(size_band(value), size_band(680), size_band(200))

# A loop over a few order values
values = [420, 200, 1560, 240, 1260]
total = 0
for v in values:
    total += v
    print(f"{v:>6} -> {size_band(v)}")
print("Total:", total)

# A loop with a condition: count large orders
large = 0
for v in values:
    if v >= 1000:
        large += 1
print("Large orders:", large)
