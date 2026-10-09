import pytest
from sales import net_revenue, parse_quantity, size_band


def test_size_band_large():
    assert size_band(1560) == "Large"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(1000, "Large"), (999.99, "Medium"), (500, "Medium"), (499, "Small")],
)
def test_size_band_boundaries(value, expected):
    assert size_band(value) == expected


def test_parse_quantity_removes_commas():
    assert parse_quantity("5,000") == 5000


def test_parse_quantity_rejects_text():
    with pytest.raises(ValueError):
        parse_quantity("lots")


def test_net_revenue_excludes_cancelled():
    orders = [
        {"value": 420.0, "status": "Delivered"},
        {"value": 240.0, "status": "Cancelled"},
        {"value": 320.0, "status": "Shipped"},
    ]
    assert net_revenue(orders) == 740.0
