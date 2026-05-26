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
    dag_id="psql_split_data_region",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["table","region", "postgre", "etl"] 

) as dag:

    # ======================================================
    # TASK — IMPORT INTO POSTGRE
    # ======================================================

    split_east = SQLExecuteQueryOperator(

        task_id="split_east_region",

        conn_id="datasource_airflow_psql",

        sql="""
        CREATE TABLE public.transaction_east AS 
        SELECT * FROM public.transaction WHERE region = 'East';

        BEGIN;

        ALTER TABLE public.transaction_east ALTER COLUMN id TYPE BIGINT;

        CREATE SEQUENCE IF NOT EXISTS public.transaction_east_id_seq;
        ALTER TABLE public.transaction_east ALTER COLUMN id SET DEFAULT nextval('public.transaction_east_id_seq');
        ALTER SEQUENCE public.transaction_east_id_seq OWNED BY public.transaction_east.id;

        SELECT setval('public.transaction_east_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM public.transaction_east;

        ALTER TABLE public.transaction_east ADD PRIMARY KEY (id);

        CREATE INDEX IF NOT EXISTS idx_transaction_year ON public.transaction_east (year);

        COMMIT;
        """
    )

    split_west = SQLExecuteQueryOperator(

        task_id="split_west_region",

        conn_id="datasource_airflow_psql",

        sql="""
        CREATE TABLE public.transaction_west AS 
        SELECT * FROM public.transaction WHERE region = 'West';

        BEGIN;

        ALTER TABLE public.transaction_west ALTER COLUMN id TYPE BIGINT;

        CREATE SEQUENCE IF NOT EXISTS public.transaction_west_id_seq;
        ALTER TABLE public.transaction_west ALTER COLUMN id SET DEFAULT nextval('public.transaction_west_id_seq');
        ALTER SEQUENCE public.transaction_west_id_seq OWNED BY public.transaction_west.id;

        SELECT setval('public.transaction_west_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM public.transaction_west;

        ALTER TABLE public.transaction_west ADD PRIMARY KEY (id);

        CREATE INDEX IF NOT EXISTS idx_transaction_year ON public.transaction_west (year);

        COMMIT;
        """
    )

    split_north = SQLExecuteQueryOperator(

        task_id="split_north_region",

        conn_id="datasource_airflow_psql",

        sql="""
        CREATE TABLE public.transaction_north AS 
        SELECT * FROM public.transaction WHERE region = 'North';

        BEGIN;

        ALTER TABLE public.transaction_north ALTER COLUMN id TYPE BIGINT;

        CREATE SEQUENCE IF NOT EXISTS public.transaction_north_id_seq;
        ALTER TABLE public.transaction_north ALTER COLUMN id SET DEFAULT nextval('public.transaction_north_id_seq');
        ALTER SEQUENCE public.transaction_north_id_seq OWNED BY public.transaction_north.id;

        SELECT setval('public.transaction_north_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM public.transaction_north;

        ALTER TABLE public.transaction_north ADD PRIMARY KEY (id);

        CREATE INDEX IF NOT EXISTS idx_transaction_year ON public.transaction_north (year);

        COMMIT;
        """
    )

    split_south = SQLExecuteQueryOperator(

        task_id="split_south_region",

        conn_id="datasource_airflow_psql",

        sql="""
        CREATE TABLE public.transaction_south AS 
        SELECT * FROM public.transaction WHERE region = 'South';

        BEGIN;

        ALTER TABLE public.transaction_south ALTER COLUMN id TYPE BIGINT;

        CREATE SEQUENCE IF NOT EXISTS public.transaction_south_id_seq;
        ALTER TABLE public.transaction_south ALTER COLUMN id SET DEFAULT nextval('public.transaction_south_id_seq');
        ALTER SEQUENCE public.transaction_south_id_seq OWNED BY public.transaction_south.id;

        SELECT setval('public.transaction_south_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM public.transaction_south;

        ALTER TABLE public.transaction_south ADD PRIMARY KEY (id);

        CREATE INDEX IF NOT EXISTS idx_transaction_year ON public.transaction_south (year);

        COMMIT;
        """
    )

    drop_all_table_regions = SQLExecuteQueryOperator(

        task_id="drop_all_table_regions",

        conn_id="datasource_airflow_psql",

        sql="""
        DROP TABLE IF EXISTS public.transaction_east;   
        DROP TABLE IF EXISTS public.transaction_west;
        DROP TABLE IF EXISTS public.transaction_north;
        DROP TABLE IF EXISTS public.transaction_south;
        """
    )

    # ======================================================
    # TASK CHAIN
    # ======================================================

    drop_all_table_regions >> split_east >> split_west >> split_north >> split_south 