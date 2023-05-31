from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


def forecast(city):
    """Get weather forecast for a city"""
    # call api to get weather forecast
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )
    # print weather forecast
    print(response.json())


if __name__ == "__main__":
    forecast(input())
