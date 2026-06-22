import os
import json
from datetime import datetime
import requests
import boto3
from dotenv import load_dotenv

load_dotenv()

STATION = "GDN_01"
STATION_ID = "GHCND:GDN_01"

WEATHER_API_TOKEN = os.getenv("WEATHER_API_TOKEN")
BASE_URL = ""

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

def fetch_weather_data(station_id, limit=100):
    """downloads weather data from the weather API for a given station"""
    url = f"{BASE_URL}/weather/batch?station_id={station_id}&limit={limit}"
    headers = {"Authorization": WEATHER_API_TOKEN}

    print(f"Fetching weather data from {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

def save_to_s3_bronze(data):
    pass

if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data(STATION_ID)
        save_to_s3_bronze(weather_data)
    except Exception as e:
        print(f"Error: {e}")