-- dbt/models/staging/stg_orders.sql

SELECT
    order_id,
    customer_id,
    product_id,
    city,
    state,
    country,
    region,
    
    TO_DATE(order_date, 'YYYY-MM-DD') AS order_date,
    TO_DATE(ship_date, 'YYYY-MM-DD') AS ship_date,
    customer_name,
    segment,
    category AS product_category,
    sub_category AS product_sub_category,
    product_name,
    CAST(REPLACE(sales, ',', '') AS NUMERIC(10, 2)) AS sales,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(discount AS NUMERIC(10, 2)) AS discount,
    CAST(REPLACE(profit, ',', '') AS NUMERIC(10, 2)) AS profit
FROM {{ source('staging', 'staging_orders') }}