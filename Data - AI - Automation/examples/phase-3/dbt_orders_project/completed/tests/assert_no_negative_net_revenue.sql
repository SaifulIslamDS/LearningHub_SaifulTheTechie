select order_id, net_revenue
from {{ ref('fct_orders') }}
where net_revenue < 0
