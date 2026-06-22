import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WEATHER_API_TOKEN")
access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
access_key = ("AWS_SECRET_ACCESS_KEY")