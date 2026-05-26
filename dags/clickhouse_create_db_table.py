
from airflow import DAG

from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

import clickhouse_connect

import logging

client = clickhouse_connect.get_client(host='clickhouse_server', port=8123, username='airflow', 
                                       password='airflow', database='transaction_db')

def create_table():

    client.command('DROP TABLE IF EXISTS transaction_db.transaction_raw;');

    with open('/opt/airflow/dags/query/clickhouse_query_dir/create_table_transaction.sql', 'r') as f:
        create_sql = f.read()

    client.command(create_sql)
    f.close()

    logging.info("Executing CREATE TABLE")


with DAG(
        dag_id='clickhouse_create_transaction_table',
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
        tags=["clickhouse", "tablecreation", "etl"],
        template_searchpath=["/opt/airflow/datasets"]
) as dag:
    
    create_task = PythonOperator(

        task_id='create_transaction_table',

        python_callable=create_table
    )