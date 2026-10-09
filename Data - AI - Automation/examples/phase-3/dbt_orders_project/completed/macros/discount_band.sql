{% macro discount_band(discount_column) -%}
case
    when {{ discount_column }} = 0 then 'none'
    when {{ discount_column }} <= 0.03 then 'low'
    else 'high'
end
{%- endmacro %}
