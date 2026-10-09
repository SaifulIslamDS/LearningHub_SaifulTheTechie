select
    cast(date_trunc('month', order_date) as date) as order_month,
    count(*) as order_count,
    sum(case when status <> 'Cancelled' then 1 else 0 end) as active_order_count,
    round(sum(net_revenue), 2) as net_revenue,
    round(sum(estimated_margin), 2) as estimated_margin
from {{ ref('fct_orders') }}
group by 1
order by 1
