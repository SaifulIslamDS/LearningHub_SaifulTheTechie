"""Small business functions used in the pytest lesson."""


def size_band(order_value: float) -> str:
    if order_value >= 1000:
        return "Large"
    if order_value >= 500:
        return "Medium"
    return "Small"


def parse_quantity(text: str) -> int:
    """'5,000' -> 5000"""
    return int(text.replace(",", "").strip())


def net_revenue(orders: list[dict]) -> float:
    """Sum of value for all orders except Cancelled."""
    return sum(o["value"] for o in orders if o["status"] != "Cancelled")
