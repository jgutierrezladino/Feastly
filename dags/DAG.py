from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import storage

# Función para descargar y leer archivos desde GCS
def extract_data(bucket_name, file_path, **kwargs):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    with open("/tmp/temp.parquet", "wb") as temp_file:
        blob.download_to_file(temp_file)
    
    df = pd.read_parquet("/tmp/temp.parquet")
    return df.to_dict()  # Convertimos a dict para pasarlo por XCom

# Función para transformar los datos
def transform_data(**kwargs):
    ti = kwargs['ti']
    df_dict = ti.xcom_pull(task_ids='extract_data')  # Recuperar datos de XCom
    df = pd.DataFrame(df_dict)

    df = df.drop(columns=['categories'])
    df = df.explode('category')
    return df.to_dict()

# Función para cargar los datos a GCS
def load_data(bucket_name, destination_path, **kwargs):
    ti = kwargs['ti']
    df_dict = ti.xcom_pull(task_ids='transform_data')  # Recuperar datos de XCom
    df = pd.DataFrame(df_dict)

    df.to_csv("/tmp/transformed_data.csv", index=False)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    with open("/tmp/transformed_data.csv", "rb") as temp_file:
        blob.upload_from_file(temp_file)

# Definición del DAG
with DAG(
    'etl_parquet',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023, 1, 1),
        'email': ['your_email@example.com'],
        'email_on_failure': True,
        'email_on_retry': True,
    },
    schedule_interval="@daily",
    catchup=False
) as dag:

    # Tarea para extraer los datos
    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'bucket_name': 'us-central1-prueba-3b82ddb6-bucket',
            'file_path': 'data/business-metadatos-inner.parquet',
        },
    )

    # Tarea para transformar los datos
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
    )

    # Tarea para cargar los datos
    load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={
            'bucket_name': 'us-central1-prueba-3b82ddb6-bucket',
            'destination_path': 'output/transformed_data.csv',
        },
        provide_context=True,
    )

    # Dependencias entre las tareas
    extract >> transform >> load
