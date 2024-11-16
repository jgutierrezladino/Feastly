from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSUploadFileOperator
from airflow.decorators import task
import pandas as pd
import logging
from google.cloud import storage

# Configuración del DAG
TAGS = ['ETL']
DAG_ID = 'ETL_DAG'
DAG_DESCRIPTION = 'Un DAG para realizar ETL de archivos parquet'
DAG_SCHEDULE = '@daily'  # Puedes ajustar esto según necesites
default_args = {
    'start_date': datetime(2024, 11, 1),
    'retries': 1,  # Ajusta esto según lo que necesites
    'retry_delay': timedelta(minutes=5)
}

# Mi código de funciones ETL

def extract():
    logging.info("Iniciando tarea de extracción.")
    try:
        # Cambiar la ruta a un archivo en GCS
        client = storage.Client.from_service_account_json("/opt/airflow/gcp/credentials/hazel-framing-413123-cf4127d45f7e.json")
        bucket = client.get_bucket('your-gcs-bucket-name')  # Reemplaza con tu bucket de GCS
        blob = bucket.blob('datasets/bussiness.parquet')  # Ruta en GCS
        blob.download_to_filename('/opt/airflow/dags/datasets/bussiness.parquet')

        df = pd.read_parquet('/opt/airflow/dags/datasets/bussiness.parquet')
        logging.info("Datos cargados en extract:\n%s", df.head())
    except Exception as e:
        logging.error("Error en la tarea de extracción: %s", str(e))
        raise
    return df


def transform(df):
    logging.info("Iniciando tarea de transformación.")
    try:
        df_transformed = df[df['state'] == 'MA']  # Solo un ejemplo
        logging.info("Datos después de la transformación:\n%s", df_transformed.head())
    except Exception as e:
        logging.error("Error en la tarea de transformación: %s", str(e))
        raise
    return df_transformed


def load(df):
    logging.info("Iniciando tarea de carga.")
    try:
        logging.info("Primeras filas de los datos a cargar:\n%s", df.head())
        logging.info("Número de filas: %d", len(df))  # Verifica que no esté vacío
        output_file = '/opt/airflow/dags/datasets/salida.parquet'
        df.to_parquet(output_file)
        
        # Subir el archivo transformado a GCS
        client = storage.Client.from_service_account_json("/opt/airflow/gcp/credentials/hazel-framing-413123-cf4127d45f7e.json")
        bucket = client.get_bucket('your-gcs-bucket-name')  # Reemplaza con tu bucket de GCS
        blob = bucket.blob('datasets/salida.parquet')  # Ruta en GCS
        blob.upload_from_filename(output_file)

        logging.info("Datos cargados correctamente en GCS en salida.parquet.")
    except Exception as e:
        logging.error("Error en la tarea de carga: %s", str(e))
        raise


# Definición del DAG
dag = DAG(
    dag_id=DAG_ID,
    description=DAG_DESCRIPTION,
    catchup=False,
    schedule_interval=DAG_SCHEDULE,
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=200000),
    default_args=default_args,
    tags=TAGS
)

with dag as dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        op_kwargs={'df': "{{ task_instance.xcom_pull(task_ids='extract') }}"},  # Se pasan los datos desde 'extract'
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        op_kwargs={'df': '{{ task_instance.xcom_pull(task_ids="transform") }}'},  # Se pasan los datos desde 'transform'
    )

    extract_task >> transform_task >> load_task
