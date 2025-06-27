-- dbt/models/marts/dim_customers.sql
SELECT DISTINCT
    customer_id,
    customer_name,
    segment
FROM {{ ref('stg_orders') }}