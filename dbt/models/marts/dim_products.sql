-- dbt/models/marts/dim_products.sql
SELECT DISTINCT
    product_id,
    product_name,
    product_category,
    product_sub_category
FROM {{ ref('stg_orders') }}