from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

with DAG(
    'superstore_etl_pipeline',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['project', 'dbt'],
) as dag:
    
    create_staging_schema = PostgresOperator(
        task_id='create_staging_schema',
        postgres_conn_id='postgres_default',
        sql="CREATE SCHEMA IF NOT EXISTS staging;"
    )

    create_staging_table = PostgresOperator(
        task_id='create_staging_table',
        postgres_conn_id='postgres_default',
        sql="""
            DROP TABLE IF EXISTS staging.staging_orders;
            CREATE TABLE staging.staging_orders (
                row_id TEXT, order_id TEXT, order_date TEXT, ship_date TEXT, ship_mode TEXT,
                customer_id TEXT, customer_name TEXT, segment TEXT, country TEXT, city TEXT,
                state TEXT, postal_code TEXT, region TEXT, product_id TEXT,
                category TEXT, sub_category TEXT, product_name TEXT, sales TEXT,
                quantity TEXT, discount TEXT, profit TEXT
            );
        """
    )
    
    
    load_data_task = PostgresOperator(
        task_id='load_data_to_staging',
        postgres_conn_id='postgres_default',
        sql="""
            COPY staging.staging_orders (
                row_id,
                order_id,
                order_date,
                ship_date,
                ship_mode,
                customer_id,
                customer_name,
                segment,
                country,
                city,
                state,
                postal_code,
                region,
                product_id,
                category,
                sub_category,
                product_name,
                sales,
                quantity,
                discount,
                profit
            )
            FROM '/var/lib/postgresql/data_csv/GlobalSuperstore.csv'
            WITH (
                FORMAT csv,
                HEADER true,
                DELIMITER ',',
                ENCODING 'latin1',
                FORCE_NULL (postal_code)
            );
        """
    )

    trigger_dbt_run = BashOperator(
        task_id='trigger_dbt_run',
        bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt'
    )

    create_staging_schema >> create_staging_table >> load_data_task >> trigger_dbt_run