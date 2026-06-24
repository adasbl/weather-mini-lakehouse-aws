import os
import json
import io
import pandas as pd
import boto3
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

with open("config/stations_config.json") as f:
    config = json.load(f)

VALIDATION_RULES = config.get("validation_rules", {})

def get_s3_client():
    """initializes and returns S3 client"""
    return boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_KEY,
        aws_session_token=SESSION_TOKEN
    )

def list_bronze_files(s3_client):
    """Retrieves a list of all JSON files located in the bronze/ folder"""
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="bronze/")
    files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.json'):
                files.append(obj['Key'])
    return files

def load_json_from_s3(s3_client, file_key):
    """Loads a single JSON file from S3 and converts it into a DataFrame"""
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)

    if isinstance(data, dict):
        for key in ['data', 'measurements', 'weather', 'records']:
            if key in data and isinstance(data[key], list):
                return pd.DataFrame(data[key])
        return pd.DataFrame([data])

    return pd.DataFrame(data)

def clean_and_validate(df):
    if df.empty:
        return df
    
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    df = df.drop_duplicates(subset=['station_id', 'timestamp'])

    if 'temperature' in df.columns and 'temperature' in VALIDATION_RULES:
        t_min = VALIDATION_RULES['temperature']['min']
        t_max = VALIDATION_RULES['temperature']['max']
        df = df[(df['temperature'] >= t_min) & (df['temperature'] <= t_max)]

    if 'humidity' in df.columns and 'humidity' in VALIDATION_RULES:
        h_min = VALIDATION_RULES['humidity']['min']
        h_max = VALIDATION_RULES['humidity']['max']
        df = df[(df['humidity'] >= h_min) & (df['humidity'] <= h_max)]

    return df

def save_to_s3_silver(s3_client, df, original_key):
    if df.empty:
        print(f"DataFrame: {original_key} is empty, skipping save")
        return
    
    base_name = os.path.basename(original_key).replace('.json', '.parquet')
    silver_key = f"silver/{base_name}"

    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')

    print(f"Uploadig clean data to {silver_key}...")
    s3_client.put_object(
        Bucket = BUCKET_NAME,
        Key = silver_key,
        Body = parquet_buffer.getvalue(),
        ContentType = "application/x-parquet"
    )
    print("Succesfully saved in silver layer")

if __name__ == "__main__":
    s3_client = get_s3_client()

    bronze_files = list_bronze_files(s3_client)
    print(f"Found {len(bronze_files)} files in Bronze layer")

    for file_key in bronze_files:
        try:
            print(f"\n Processing file {file_key}")
            raw_df = load_json_from_s3(s3_client, file_key)

            clean_df = clean_and_validate(raw_df)

            save_to_s3_silver(s3_client, clean_df, file_key)
        except Exception as e:
            print(f"Error during transformation of file {file_key}: {e}")
