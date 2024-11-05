from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import pandas as pd

# Configuración del DAG
TAGS = ['ETL']
DAG_ID = 'ETL_DAG'
DAG_DESCRIPTION = 'Un DAG para realizar ETL de archivos parquet'
DAG_SCHEDULE = '@daily'  # Puedes ajustar esto según necesites
default_args = {
    'start_date': datetime(2024, 11, 1),
    'retries': 1,  # Ajusta esto según lo que necesites
    'retry_delay': timedelta(minutes=5),
}

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

def extract():
    # Leer el archivo .parquet
    df = pd.read_parquet('C:\\Users\\User\\OneDrive\\Escritorio\\Proyecto Final\\Feastly\\metadatos2.parquet')
    return df

def transform(df):
    # Realizar transformaciones en los datos
    df_transformed = df[df['state'] == 'MA']  # Solo un ejemplo
    return df_transformed

def load(df):
    print(df.head())  # Para ver los primeros registros
    print(f"Número de filas: {len(df)}")  # Verifica que no esté vacío
    df.to_parquet('C:\\Users\\User\\OneDrive\\Escritorio\\Proyecto Final\\Feastly\\prueba.parquet')

with dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        op_kwargs={'df': '{{ task_instance.xcom_pull(task_ids="extract") }}'},
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        op_kwargs={'df': '{{ task_instance.xcom_pull(task_ids="transform") }}'},
    )

    extract_task >> transform_task >> load_task