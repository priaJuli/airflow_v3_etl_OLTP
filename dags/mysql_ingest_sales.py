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
    dag_id="file_raw_to_mysql_table",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["csv_raw", "mysql", "etl"],
    template_searchpath=["/opt/airflow/datasets"]

) as dag:

    # ======================================================
    # TASK — IMPORT INTO MYSQL
    # ======================================================

    import_mysql = SQLExecuteQueryOperator(

        task_id="import_csv_to_mysql",

        conn_id="datasource_airflow_mysql",

        sql="""

        LOAD DATA INFILE '/tmp/spark_datasets/synthetic_healthcare_semantics.csv'

        INTO TABLE transaction

        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'

        LINES TERMINATED BY '\n'

        IGNORE 1 ROWS
        (
            year,
            month,
            @id,
            hospital_id ,
            hospital_type,
            ownership,
            region,
            urban_rural ,
            service_category ,
            patient_volume ,
            avg_daily_visits ,
            bed_occupancy_rate ,
            staff_to_patient_ratio ,
            resource_utilization_rate ,
            avg_wait_time_minutes ,
            service_delay_rate ,
            appointment_backlog ,
            avg_service_cost ,
            cost_per_patient ,
            operational_efficiency_index ,
            redmission_rate ,
            service_completion_rate ,
            complaint_rate ,
            followup_adherence_rate ,
            latent_accessibility_score ,
            latent_efficiency_score ,
            semantic_cluster_id ,
            semantic_cluster_level
        );

        """
    )

    # ======================================================
    # TASK CHAIN
    # ======================================================

    import_mysql