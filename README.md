# Healthcare ETL Orchestration with Apache Airflow

This repository demonstrates an ETL (Extract, Transform, Load) pipeline using **Apache Airflow** to process healthcare service semantics data. The project utilizes Docker to containerize the orchestration environment, source databases, and target warehouses.

---

## 1. Why Apache Airflow for ETL Orchestration?

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. For this project, it serves as the backbone for moving data from raw sources into structured relational databases.

### Key Advantages:
- **Dynamic Pipeline Generation**: Pipelines are defined as Python code, allowing for dynamic task generation and complex logic.
- **Extensible Framework**: With a vast library of operators (MySQLOperator, PostgresOperator, etc.), it connects seamlessly to various database technologies.
- **Scalability**: Airflow can scale from a single machine to a large cluster via the Celery or Kubernetes executors.
- **Rich UI**: Provides a clear visualization of DAGs (Directed Acyclic Graphs), task dependencies, and execution logs, making debugging straightforward.

### Data Source
The pipeline processes the **Healthcare Service Semantics** dataset available on [Kaggle](https://www.kaggle.com/datasets/firozemaliha/healthcare-service-semantics). This dataset includes healthcare facility information, services, and locations, which are transformed into structured tables for analysis.

---

## 2. Infrastructure: Docker Compose Services

The project environment is managed via `docker-compose.yml`, which spins up the following interconnected services:

| Service | Description |
| :--- | :--- |
| **Airflow Webserver** | The GUI for managing and monitoring DAGs. |
| **Airflow Scheduler** | The engine that monitors tasks and triggers them when dependencies are met. |
| **Postgres (Metadata)** | Internal database used by Airflow to store task states and configurations. |
| **MySQL (Source)** | Acts as a source database where raw healthcare data is initially ingested. |
| **PostgreSQL (Target)** | Acts as the data warehouse where transformed and indexed data is stored. |
| **Redis** | The message broker used for communication between the scheduler and workers. |

---

## 3. Managing Connections via External Files

To maintain a clean main `README.md` and keep configuration logic separate, you can reference specific setup guides for Docker connections.

### Referencing Connection Documentation
For detailed steps on how to configure Airflow Hooks and Connections (e.g., setting up `mysql_conn_id` or `postgres_conn_id` within the Airflow UI to point to Docker containers), please refer to:

- [**Docker Connection Configuration Guide (How to create airflow connections.md)**](./How to create airflow connections.md)

- [**Docker Connection Test Guide (Debug Airflow Connection.md)**](./Debug Airflow Connection.md)

*Tip: In Docker, when Airflow needs to connect to the MySQL container, use the service name `mysql` as the host instead of `localhost`.*

---

## 4. Project Features (DAGs)

This project contains two primary DAG workflows designed to handle data lifecycle management in different SQL environments.

### A. MySQL Pipeline
The MySQL DAG automates the following steps:
1. **Create Table**: Initializes the schema for raw healthcare records.
2. **Load Raw CSV**: Uses the `LOAD DATA INFILE` command (or local Python processing) to ingest the Kaggle dataset into the table.
3. **Create Regions Table**: Normalizes the data by extracting unique region/location information into a separate table.
4. **Create Index**: Adds performance-optimizing indexes on frequently queried columns like `service_id` and `location_code`.

### B. PostgreSQL Pipeline
The PostgreSQL DAG focuses on building the analytics layer:
1. **Create Table**: Defines the structured schema for healthcare semantics.
2. **Load Raw CSV**: Utilizes the `COPY` command for high-speed data ingestion from the source file.
3. **Create Regions Table**: Generates a dimension table for regional analysis, ensuring data integrity through foreign keys.
4. **Create Index**: Implements B-Tree indexes on semantic tags and facility names to accelerate complex filtering queries.

---

## Getting Started
1. Clone the repository.
2. Place the Kaggle dataset CSV in the `/data` directory.
3. Run `docker-compose up -d`.
4. Access the Airflow UI at `http://localhost:8080`.
