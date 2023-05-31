from dotenv import load_dotenv
import os
import requests
from rich.console import Console
from rich.table import Table
import datetime

load_dotenv()

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CELCIUS_CONVERTER = 273.15
ROUNDOFF = 2


# Get weather forecast for a city
def forecast(city):
    # call api to get weather forecast
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )

    if response.status_code == 200:
        formatOutput(response.json())
    else:
        print("City not found")


def formatOutput(response):
    weatherObject = response

    # Get the country name
    country = requests.get(
        f"https://restcountries.com/v3.1/alpha?codes={weatherObject['sys']['country']}"
    ).json()[0]["name"]["common"]

    # Latitude and Longitude
    longitude = str(weatherObject["coord"]["lon"])
    latitude = str(weatherObject["coord"]["lat"])

    # Weather Description
    main_weather = str(weatherObject["weather"][0]["main"])
    description = str(weatherObject["weather"][0]["description"])

    # Temperature
    temprature = str(round(weatherObject["main"]["temp"] - CELCIUS_CONVERTER, ROUNDOFF))
    feels_like = str(
        round(weatherObject["main"]["feels_like"] - CELCIUS_CONVERTER, ROUNDOFF)
    )
    minimal_temprature = str(
        round(weatherObject["main"]["temp_min"] - CELCIUS_CONVERTER, ROUNDOFF)
    )
    maximum_temprature = str(
        round(weatherObject["main"]["temp_max"] - CELCIUS_CONVERTER, ROUNDOFF)
    )
    preassure = str(weatherObject["main"]["pressure"])
    humidity = str(weatherObject["main"]["humidity"])

    # Visibility
    visibility = str(weatherObject["visibility"] / 1000)

    # Wind
    wind_speed = str(weatherObject["wind"]["speed"])
    wind_degree = str(weatherObject["wind"]["deg"])

    # Clouds
    clouds = str(weatherObject["clouds"]["all"])

    # Sunrise and Sunset
    sunrise = str(
        datetime.datetime.utcfromtimestamp(
            weatherObject["sys"]["sunrise"] + weatherObject["timezone"]
        )
    ).split(" ")[1]
    sunset = str(
        datetime.datetime.utcfromtimestamp(
            weatherObject["sys"]["sunset"] + weatherObject["timezone"]
        )
    ).split(" ")[1]

    # Table Formatting
    table = Table(
        title=f"[bold red]Weather forecast for {weatherObject['name']}, {country}[/bold red]"
    )
    table.add_column("Co-Ordinates")
    table.add_column("Weather")
    table.add_column("Temperature")
    table.add_column("Visibility")
    table.add_column("Wind")
    table.add_column("Clouds")
    table.add_column("Sunrise and Sunset")

    table.add_row(
        f"Longitude: {longitude}\nLatitude: {latitude}",
        f"{main_weather} - {description}",
        f"Temprature: {temprature}°C\nFeels like: {feels_like}°C\nMinimum Temprature: {minimal_temprature}°C\nMaximum Temprature: {maximum_temprature}°C\nPreassure: {preassure}hPa\nHumidity: {humidity}%",
        f"{visibility}km",
        f"Wind Speed: {wind_speed}m/s\nWind Degree: {wind_degree}°",
        f"{clouds}%",
        f"Sunrise: {sunrise}\nSunset:  {sunset}",
    )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    forecast(input())
