import os
import json
from datetime import datetime
import requests
import boto3
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_TOKEN = os.getenv("WEATHER_API_TOKEN")

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

with open("config/stations_config.json") as f:
    config = json.load(f)

BASE_URL = config["api"]["base_url"]
STATIONS_TO_FETCH = config["monitoring"]["stations"]

default_limit = config["api"]["default_limit"]

def fetch_weather_data(station_id, limit):
    """downloads weather data from the weather API for a given station"""
    url = f"{BASE_URL}/weather/batch?station_id={station_id}&limit={limit}"
    headers = {"Authorization": WEATHER_API_TOKEN}

    print(f"Fetching weather data from {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

def save_to_s3_bronze(data, station_id):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_KEY,
        aws_session_token=SESSION_TOKEN
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"bronze/weather_{station_id}_{timestamp}.json"

    json_data = json.dumps(data, indent=4)

    print(f"Uploading {file_name} to bucket {BUCKET_NAME}...")

    s3_client.put_object(
        Bucket = BUCKET_NAME,
        Key = file_name,
        Body = json_data,
        ContentType = "application/json"
    )

    print(f"Successfully saved data from {station_id}")

if __name__ == "__main__":
    for station_id in STATIONS_TO_FETCH:
        try:
            weather_data = fetch_weather_data(station_id, default_limit)
            save_to_s3_bronze(weather_data, station_id)
        except Exception as e:
            print(f"Error: {e}")    