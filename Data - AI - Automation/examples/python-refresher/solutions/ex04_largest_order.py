"""Exercise 04 — add a largest() method to OrderBook."""

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


class OrderBook:
    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders

    def net(self) -> list[Order]:
        return [o for o in self.orders if o.status != "Cancelled"]

    def largest(self) -> Order:
        """The biggest non-cancelled order (new method)."""
        return max(self.net(), key=lambda o: o.value)


book = OrderBook(
    [
        Order(1, "Rahim Traders", "Dhaka", 120, 3.50, "Delivered"),
        Order(3, "Nova Apparel", "Dhaka", 300, 5.20, "Delivered"),
        Order(4, "Rahim Traders", "Dhaka", 800, 0.30, "Cancelled"),
        Order(7, "Nova Apparel", "Dhaka", 8000, 0.04, "Shipped"),
        Order(10, "Rahim Traders", "Dhaka", 300, 2.90, "Delivered"),
    ]
)
big = book.largest()
print(f"Largest order: {big.order_id} ({big.customer}) = {big.value:.2f}")
