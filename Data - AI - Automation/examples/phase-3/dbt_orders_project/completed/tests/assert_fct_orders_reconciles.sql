with totals as (
    select
        count(*) as row_count,
        round(sum(net_revenue), 2) as net_revenue
    from {{ ref('fct_orders') }}
)
select *
from totals
where row_count <> 4246
   or abs(net_revenue - 5478357.79) > 0.01
