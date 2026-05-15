from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime

import logging

# ==========================================================
# DAG
# ==========================================================

with DAG(
    dag_id="split_data_region_mysql_table",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["table","region", "mysql", "etl"] 

) as dag:

    # ======================================================
    # TASK — IMPORT INTO MYSQL
    # ======================================================

    split_east = SQLExecuteQueryOperator(

        task_id="split_east_region",

        conn_id="datasource_airflow_mysql",

        sql="""
        CREATE TABLE transaction_east AS 
        SELECT * FROM transaction WHERE region = 'East';
        """
    )

    split_west = SQLExecuteQueryOperator(

        task_id="split_west_region",

        conn_id="datasource_airflow_mysql",

        sql="""
        CREATE TABLE transaction_west AS 
        SELECT * FROM transaction WHERE region = 'West';
        """
    )

    split_north = SQLExecuteQueryOperator(

        task_id="split_north_region",

        conn_id="datasource_airflow_mysql",

        sql="""
        CREATE TABLE transaction_north AS 
        SELECT * FROM transaction WHERE region = 'North';
        """
    )

    split_south = SQLExecuteQueryOperator(

        task_id="split_south_region",

        conn_id="datasource_airflow_mysql",

        sql="""
        CREATE TABLE transaction_south AS 
        SELECT * FROM transaction WHERE region = 'South';
        """
    )

    drop_all_table_regions = SQLExecuteQueryOperator(

        task_id="drop_all_table_regions",

        conn_id="datasource_airflow_mysql",

        sql="""
        DROP TABLE IF EXISTS transaction_east;
        DROP TABLE IF EXISTS transaction_west;
        DROP TABLE IF EXISTS transaction_north;
        DROP TABLE IF EXISTS transaction_south;
        """
    )


    create_all_index_regions = SQLExecuteQueryOperator(

        task_id="create_all_index_regions",

        conn_id="datasource_airflow_mysql",

        sql="""
        ALTER TABLE transaction_east ADD PRIMARY KEY (id);
        ALTER TABLE transaction_west ADD PRIMARY KEY (id);
        ALTER TABLE transaction_north ADD PRIMARY KEY (id);
        ALTER TABLE transaction_south ADD PRIMARY KEY (id);

        ALTER TABLE transaction_east ADD INDEX idx_transaction_east_year (year);
        ALTER TABLE transaction_west ADD INDEX idx_transaction_west_year (year);
        ALTER TABLE transaction_north ADD INDEX idx_transaction_north_year (year);
        ALTER TABLE transaction_south ADD INDEX idx_transaction_south_year (year);
        """
    )

    # ======================================================
    # TASK CHAIN
    # ======================================================

    drop_all_table_regions >> split_east >> split_west >> split_north >> split_south >> create_all_index_regions