import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def load_cities():
    """
    Load the list of cities from config/cities.json.
    """

    config_path = Path(__file__).resolve().parent.parent / "config" / "cities.json"

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_weather(city, country):
    """
    Fetch current weather data for a city.
    """

    if not API_KEY:
        raise ValueError(
            "OPENWEATHER_API_KEY is not set."
        )

    params = {
        "q": f"{city},{country}",
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def extract_weather_data():
    """
    Extract weather data for all configured cities.
    """

    cities = load_cities()

    weather_data = []

    for location in cities:

        city = location["city"]
        country = location["country"]

        print(f"Fetching weather for {city}, {country}...")

        data = fetch_weather(city, country)

        weather_data.append(data)

    return weather_data


if __name__ == "__main__":

    data = extract_weather_data()

    print(f"Successfully extracted {len(data)} records.")

    for record in data:
        print(
            record["name"],
            record["main"]["temp"],
            record["weather"][0]["description"]
        )