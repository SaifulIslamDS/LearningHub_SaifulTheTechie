select
    customer_id,
    customer_name,
    segment,
    region,
    cast(signup_date as date) as signup_date,
    cast(credit_days as integer) as credit_days
from {{ source('shop', 'customers_2025') }}
