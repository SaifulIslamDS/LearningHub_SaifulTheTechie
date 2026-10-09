select
    o.*,
    c.customer_name,
    p.list_price,
    {{ discount_band('o.discount') }} as discount_band,
    case when o.status = 'Cancelled' then cast(0 as decimal(18, 2)) else o.revenue end as net_revenue,
    case
        when o.status = 'Cancelled' then cast(0 as decimal(18, 2))
        else round(o.revenue - (o.quantity * o.unit_cost), 2)
    end as estimated_margin
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_customers') }} as c using (customer_id)
left join {{ ref('stg_products') }} as p using (product)
