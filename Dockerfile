FROM apache/airflow:3.0.6-python3.12

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libldap2-dev

USER airflow

RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    apache-airflow-providers-google \
    apache-airflow-providers-ssh \
    apache-airflow-providers-sftp \
    apache-airflow-providers-mongo \
    apache-airflow-providers-mysql \
    apache-airflow-providers-fab \
    apache-airflow-providers-apache-spark
