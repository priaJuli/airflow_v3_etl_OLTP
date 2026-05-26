from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import logging

def create_table():

    mysql_hook = MySqlHook(
        mysql_conn_id='datasource_airflow_mysql'
    )

    with open('/opt/airflow/dags/query/mysql_query_dir/healthcare_base_table_transaction.sql', 'r') as f:
        create_sql = f.read()

    conn = mysql_hook.get_conn()

    cursor = conn.cursor()

    logging.info("Executing CREATE TABLE")

    cursor.execute(create_sql)

    logging.info("Table created successfully")

    cursor.close()

    conn.close()

with DAG(

    dag_id='mysql_create_table_structure',

    start_date=datetime(2024, 1, 1),
    tags=["create_table", "mysql", "etl"],
    schedule=None,

    catchup=False

) as dag:

    create_task = PythonOperator(

        task_id='create_transaction_table',

        python_callable=create_table
    )