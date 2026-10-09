select
    product,
    category,
    cast(list_price as decimal(12, 4)) as list_price,
    cast(unit_cost as decimal(12, 4)) as unit_cost
from {{ source('shop', 'products_2025') }}
