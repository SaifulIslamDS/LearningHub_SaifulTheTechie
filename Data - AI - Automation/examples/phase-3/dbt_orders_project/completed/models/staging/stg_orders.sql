select
    cast(order_id as bigint) as order_id,
    cast(order_date as date) as order_date,
    customer_id,
    region,
    segment,
    channel,
    category,
    product,
    cast(quantity as bigint) as quantity,
    cast(unit_price as decimal(12, 4)) as unit_price,
    cast(discount as decimal(8, 4)) as discount,
    cast(unit_cost as decimal(12, 4)) as unit_cost,
    status,
    cast(promised_days as integer) as promised_days,
    cast(delivery_days as integer) as delivery_days,
    cast(revenue as decimal(18, 2)) as revenue
from {{ source('shop', 'orders_2025') }}
