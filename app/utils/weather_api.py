import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY", "22f9ea86b3c7d79c4a1df5b7a06da497")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()
