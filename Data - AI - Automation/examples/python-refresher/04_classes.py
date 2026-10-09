"""Lesson: classes (OOP) with dataclasses and type hints."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    customer: str
    region: str
    quantity: int
    unit_price: float
    status: str

    @property
    def value(self) -> float:
        return self.quantity * self.unit_price

    def is_open(self) -> bool:
        return self.status in {"Shipped", "Pending"}


class OrderBook:
    """A collection of orders with business calculations."""

    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders

    def net(self) -> list[Order]:
        return [o for o in self.orders if o.status != "Cancelled"]

    def net_revenue(self) -> float:
        return sum(o.value for o in self.net())

    def open_value(self) -> float:
        return sum(o.value for o in self.orders if o.is_open())

    def revenue_by(self, attr: str) -> dict[str, float]:
        result: dict[str, float] = {}
        for o in self.net():
            key = getattr(o, attr)
            result[key] = result.get(key, 0) + o.value
        return result


book = OrderBook(
    [
        Order(1, "Rahim Traders", "Dhaka", 120, 3.50, "Delivered"),
        Order(3, "Nova Apparel", "Dhaka", 300, 5.20, "Delivered"),
        Order(4, "Rahim Traders", "Dhaka", 800, 0.30, "Cancelled"),
        Order(7, "Nova Apparel", "Dhaka", 8000, 0.04, "Shipped"),
        Order(10, "Rahim Traders", "Dhaka", 300, 2.90, "Delivered"),
    ]
)
first = book.orders[0]
print(first)
print(f"Order {first.order_id} value: {first.value:.2f}")
print(f"Net revenue: {book.net_revenue():.2f}")
print(f"Open value: {book.open_value():.2f}")
print(book.revenue_by("customer"))
