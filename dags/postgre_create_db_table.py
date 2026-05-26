from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import logging

def create_table():

    postgres_hook = PostgresHook(
        postgres_conn_id='datasource_airflow_psql'
    )

    with open('/opt/airflow/dags/query/postgre_query_dir/healthcare_base_table_transaction.sql', 'r') as f:
        create_sql = f.read()

    postgres_hook.run(create_sql)

    logging.info("Executing CREATE TABLE")


with DAG(

    dag_id='psql_create_table_structure',

    start_date=datetime(2024, 1, 1),
    tags=["create_table", "postgres", "etl"],
    schedule=None,

    catchup=False

) as dag:

    create_task = PythonOperator(

        task_id='create_transaction_table_psql',

        python_callable=create_table
    )

    create_task