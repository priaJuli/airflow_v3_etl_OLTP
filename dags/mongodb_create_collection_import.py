from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime
import logging
import csv

def mongo_import_call():

    mongo_hook = MongoHook(
        mongo_conn_id='datasource_airflow_mongodb'
    )

    logging.info("MongoDB connection established successfully")

    CHUNK_SIZE = 250000

    CSV_FILE_PATH = '/opt/airflow/datasets/synthetic_healthcare_semantics.csv'

    INT_COLUMNS = {'year', 'month', 'hospital_id', 'time_index'}
    STR_COLUMNS = {'hospital_type', 'ownership', 'region', 'urban_rural', 'service_category', 'semantic_cluster_id'}

    def cast_value(col, val):
        val = val.strip() if val else ""
        if val == "": 
            return None
        
        if col in INT_COLUMNS: 
            return int(val)
        if col in STR_COLUMNS: 
            return str(val)
        
        try:
            return float(val.replace(',', '.'))
        except ValueError:
            return val

    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
        # DictReader uses the first line as dictionary keys automatically
        logging.info("Reading CSV Files")
        reader = csv.DictReader(csv_file, delimiter=',')
        
        chunk = []
        total_inserted = 0
        
        for row in reader:

            casted_row = {col: cast_value(col, val) for col, val in row.items()}
            chunk.append(casted_row)
            
            # Once our chunk array hits the threshold, send it over the wire
            if len(chunk) >= CHUNK_SIZE:
                # ordered=False allows MongoDB to process inserts in parallel on the server
                mongo_hook.insert_many(mongo_collection='raw_transactions', mongo_db='transactions_db',
                    docs=chunk, ordered=False )
                total_inserted += len(chunk)
                logging.info(f"Inserted batch: {total_inserted} rows processed...")
                
                chunk = [] # Instantly empty list memory allocation
        
        # 3. Handle any remaining trailing documents (last partial batch)
        if chunk:
            mongo_hook.insert_many(mongo_collection='raw_transactions', mongo_db='transactions_db',
                docs=chunk, ordered=False )
            total_inserted += len(chunk)

        logging.info(f"Migration completed successfully. Total rows inserted: {total_inserted}")

with DAG(

    dag_id='mongodb_create_collection',

    start_date=datetime(2024, 1, 1),
    tags=["create_collection", "mongodb", "etl"],
    schedule=None,

    catchup=False

) as dag:

    create_task = PythonOperator(
        task_id='mongo_import_call',
        python_callable=mongo_import_call
    )