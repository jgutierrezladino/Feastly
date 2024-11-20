from google.cloud import storage, bigquery
import pandas as pd
import logging
import os
import functions_framework

# Establecer el proyecto manualmente si es necesario
os.environ["GOOGLE_CLOUD_PROJECT"] = "hazel-framing-413123"

# Configuración global
BUCKET_NAME = "us-central1-prueba-3b82ddb6-bucket"
FILES = {
    "business": "data/bussiness.parquet",
    "metadatos": "data/metadatos2.parquet",
    "tip": "data/tip.csv",  
    "checkin": "data/checkin.parquet"
}
PROJECT_ID = "hazel-framing-413123"
DATASET_ID = "datosfeastly"
TABLE_ID = "tablaproyecto"

def download_file(bucket_name, blob_name, local_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_path)
    logging.info(f"Archivo descargado: gs://{bucket_name}/{blob_name}")
    return local_path

def process_etl():
    temp_dir = "/tmp/"
    
    # Descargar y procesar `business.parquet`
    business_path = download_file(BUCKET_NAME, FILES["business"], os.path.join(temp_dir, "business.parquet"))
    df1 = pd.read_parquet(business_path)
    df1 = df1.drop(columns='attributes')
    df1_clean = df1[df1['state'].str.contains('NY|NJ|PA|DE|MD|MA|ME|VA', case=False, na=False)]
    data_filtrada = df1_clean[df1_clean['state'].isin(['PA', 'DE', 'NJ'])]
    
    # Descargar y procesar `metadatos2.parquet`
    metadatos_path = download_file(BUCKET_NAME, FILES["metadatos"], os.path.join(temp_dir, "metadatos.parquet"))
    df2 = pd.read_parquet(metadatos_path)
    df2 = df2.drop(columns=['address', 'price', 'MISC', 'latitude', 'longitude'])
    
    # Unir `business` con `metadatos`
    df_merged = pd.merge(data_filtrada, df2, how='inner', on=['name', 'state'])
    df_merged2 = pd.merge(data_filtrada, df2, how='right', on=['name', 'state'])
    
    # Descargar y procesar `tip.csv`
    tip_path = download_file(BUCKET_NAME, FILES["tip"], os.path.join(temp_dir, "tip.csv"))
    df_tip = pd.read_csv(tip_path)
    df_merged3 = pd.merge(df_merged2, df_tip, how='left', on='business_id')
    
    # Descargar y procesar `checkin.parquet`
    checkin_path = download_file(BUCKET_NAME, FILES["checkin"], os.path.join(temp_dir, "checkin.parquet"))
    df_checkin = pd.read_parquet(checkin_path)
    df_merged4 = pd.merge(df_merged3, df_checkin, how='left', on='business_id')
    
    # Limpiar columnas finales
    df_merged4 = df_merged4.drop(columns=['date_y', 'categories'])
    df_final = df_merged4.explode('category')
    
    logging.info("ETL completado. Datos procesados.")
    return df_final

def upload_to_bigquery(dataframe, project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    job = client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
    job.result()
    logging.info(f"Datos cargados exitosamente en BigQuery: {table_ref}")

@functions_framework.http
def hello_pubsub(request):
    """
    Función principal para ejecutar el ETL desde un evento de Pub/Sub.
    """
    try:
        logging.info("Inicio del ETL desde Cloud Function.")
        df_final = process_etl()
        upload_to_bigquery(df_final, PROJECT_ID, DATASET_ID, TABLE_ID)
        logging.info("ETL finalizado y cargado en BigQuery.")
        return "ETL ejecutado exitosamente", 200
    except Exception as e:
        logging.error(f"Error en la ejecución del ETL: {str(e)}")
        return f"Error en el ETL: {str(e)}", 500
