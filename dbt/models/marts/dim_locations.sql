-- dbt/models/marts/dim_locations.sql

SELECT DISTINCT
    md5(city || state || country) as location_id,
    city,
    state,
    country,
    region
FROM {{ ref('stg_orders') }}