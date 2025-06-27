-- dbt/models/marts/fct_orders.sql

SELECT
    order_id || '-' || product_id as order_line_id,
    order_id,
    customer_id,
    product_id,
    md5(city || state || country) as location_id,
    order_date,
    ship_date,
    sales,
    quantity,
    discount,
    profit
FROM {{ ref('stg_orders') }}