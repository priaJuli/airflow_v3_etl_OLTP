from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime

import clickhouse_connect
from clickhouse_connect.driver.tools import insert_file

import logging

client = clickhouse_connect.get_client(host='clickhouse_server', port=8123, username='airflow', 
                                       password='airflow', database='transaction_db')

def load_data():

    insert_file(client, table='transaction_raw', file_path='/opt/airflow/datasets/synthetic_healthcare_semantics.csv',  fmt='CSVWithNames'  )
    logging.info("Executing LOAD DATA INFILE")
# ==========================================================
# DAG
# ==========================================================

with DAG(
    dag_id="clickhouse_file_raw_load",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["csv_raw", "clickhouse", "etl"],
    template_searchpath=["/opt/airflow/datasets"]

) as dag:

    # ======================================================
    # TASK — IMPORT INTO CLICKHOUSE
    # ======================================================

    import_clickhouse = PythonOperator(

        task_id='load_data_to_clickhouse',

        python_callable=load_data
    )

    # ======================================================
    # TASK CHAIN
    # ======================================================

    import_clickhouse