# ETL Mini Project: Global Superstore Sales Analysis

## 1. Project Objective

The goal of this project is to build a robust, automated ETL pipeline that processes raw sales data from a CSV file into a structured, analytics-ready format. This project provides hands-on experience with modern data engineering tools: **Apache Airflow** for orchestration, **PostgreSQL** for data warehousing, and **dbt (Data Build Tool)** for data transformation.

The final output is a **Star Schema** data model that enables efficient querying and business intelligence analysis.

### What Problem Does it Solve?

Raw sales data, often in flat files like CSVs, is difficult to analyze directly. It's slow to query, contains inconsistent data types, and lacks a clear structure for analytical questions. This project solves that problem by:
*   **Automating** the ingestion and cleaning process, reducing manual effort and errors.
*   **Structuring** the data into facts and dimensions, which is the industry standard for business intelligence.
*   **Creating** a single source of truth for sales analytics, allowing all users to work from the same reliable data.

## 2. Tech Stack

*   **Orchestration:** Apache Airflow
*   **Data Warehouse:** PostgreSQL
*   **Transformation:** dbt (Data Build Tool)
*   **Containerization:** Docker & Docker Compose
*   **Version Control:** Git & GitHub

## 3. Data Model: Star Schema

The final data model is a Star Schema, consisting of one central fact table (`fct_orders`) surrounded by three dimension tables (`dim_customers`, `dim_products`, `dim_locations`). This structure is optimized for fast analytical queries by minimizing complex joins.


## 4. How to Run the Project

### Prerequisites
*   Docker Desktop installed and running on your system.
*   A command-line terminal (like Git Bash, PowerShell, or Terminal).

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone <your-github-repo-url>
    cd <your-repo-name>
    ```

2.  **Start the Services:**
    Run the following command in the root of the project directory. This will build the Docker images and start all required services (PostgreSQL, Airflow Webserver, Airflow Scheduler) in the background.
    ```bash
    docker-compose up --build -d
    ```
    Please wait 2-3 minutes for all services to become healthy.

3.  **Access Airflow:**
    Open a web browser and navigate to `http://localhost:8080`.
    *   **Login:** `admin`
    *   **Password:** `admin`

4.  **Run the ETL Pipeline:**
    *   In the Airflow UI, find the DAG named `superstore_etl_pipeline`.
    *   Enable the DAG using the toggle switch on the left.
    *   Trigger a manual run by clicking the "play" button on the right. The pipeline will execute all tasks: creating schemas, loading the raw data, and triggering dbt to build the final analytics tables.

5.  **Verify the Results:**
    Once the DAG run is successful (all green), you can connect to the PostgreSQL database using a client like DBeaver or pgAdmin to see the final tables in the `analytics` schema.

## 5. Potential Insights from the Data Model

This structured data model allows for powerful analysis. A business user can now easily answer critical questions such as:

*   **Profitability Analysis:** What are the most profitable product sub-categories?
    ```sql
    SELECT
        p.product_sub_category,
        SUM(f.profit) as total_profit
    FROM analytics.fct_orders AS f
    JOIN analytics.dim_products AS p ON f.product_id = p.product_id
    GROUP BY 1
    ORDER BY 2 DESC;
    ```
*   **Customer Segmentation:** Who are the top 10 customers by total sales?
    ```sql
    SELECT
        c.customer_name,
        SUM(f.sales) as total_sales
    FROM analytics.fct_orders AS f
    JOIN analytics.dim_customers AS c ON f.customer_id = c.customer_id
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10;
    ```
*   **Regional Performance:** Which region has the highest quantity of items sold?
    ```sql
    SELECT
        l.region,
        SUM(f.quantity) as total_quantity_sold
    FROM analytics.fct_orders AS f
    JOIN analytics.dim_locations AS l ON f.location_id = l.location_id
    GROUP BY 1
    ORDER BY 2 DESC;
    ```