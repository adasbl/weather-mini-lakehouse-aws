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

def get_s3_client():
    """initializes and returns S3 client"""
    return boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_KEY,
        aws_session_token=SESSION_TOKEN
    )

def list_silver_files(s3_client):
    """Retrieves a list of all Parquet files in silver/ folder"""
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="silver/")
    files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.parquet'):
                files.append(obj['Key'])
    return files

def load_parquet_from_s3(s3_client, file_key):
    """Loads a single Parquet file from S3 into a DataFrame"""
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = response['Body'].read()
    
    return pd.read_parquet(io.BytesIO(file_content), engine='pyarrow')

def generate_daily_summary(df):
    """Aggregates silver data into gold daily metrics"""
    if df.empty:
        return df

    df['measurement_date'] = pd.to_datetime(df['timestamp']).dt.date

    agg_rules = {}
    if 'temperature' in df.columns:
        agg_rules['temperature'] = ['mean', 'max', 'min']
    if 'humidity' in df.columns:
        agg_rules['humidity'] = 'mean'
    if 'rain_mm' in df.columns:
        agg_rules['rain_mm'] = 'sum'

    if not agg_rules:
        return pd.DataFrame()

    grouped = df.groupby(['station_id', 'measurement_date']).agg(agg_rules)
    
    grouped.columns = [
        'avg_temperature' if c == ('temperature', 'mean') else
        'max_temperature' if c == ('temperature', 'max') else
        'min_temperature' if c == ('temperature', 'min') else
        'avg_humidity' if c == ('humidity', 'mean') else
        'total_rain_mm' if c == ('rain_mm', 'sum') else f'{c[0]}_{c[1]}'
        for c in grouped.columns
    ]
    
    grouped['total_measurements'] = df.groupby(['station_id', 'measurement_date']).size()
    
    for col in ['avg_temperature', 'avg_humidity', 'total_rain_mm']:
        if col in grouped.columns:
            grouped[col] = grouped[col].round(2)

    return grouped.reset_index()

def save_to_s3_gold(s3_client, df):
    """Saves the aggragated gold layer data back to s3"""
    if df.empty:
        print("Gold Dataframe is empty, nothing to save")
        return
    
    gold_key = "gold/local_daily_weather_summary.parquet"
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')

    print(f"Uploading data to {gold_key}")
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=gold_key,
        Body=parquet_buffer.getvalue(),
        ContentType="application/x-parquet"
    )
    print("Data succesfully saved")

if __name__ == "__main__":
    s3_client = get_s3_client()
    silver_files = list_silver_files(s3_client)

    print(f"Found {len(silver_files)} files in Silver layer")

    all_dfs = []
    for file_key in silver_files:
        try:
            print(f"Reading {file_key}...")
            df = load_parquet_from_s3(s3_client, file_key)
            all_dfs.append(df)
        except Exception as e:
            print(f"Error reading {file_key}: {e}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        gold_df = generate_daily_summary(combined_df)
        
        save_to_s3_gold(s3_client, gold_df)
    else:
        print("No data found in Silver layer to aggregate.")