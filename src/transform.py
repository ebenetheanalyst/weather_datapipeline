from datetime import datetime, timezone

import pandas as pd


def transform_weather_data(raw_data):
    """
    Transform raw OpenWeather API responses
    into a clean pandas DataFrame.
    """

    records = []

    for data in raw_data:

        weather = data["weather"][0]
        main = data["main"]
        wind = data.get("wind", {})
        clouds = data.get("clouds", {})

        record = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            "recorded_at": datetime.fromtimestamp(
                data["dt"],
                tz=timezone.utc
            ),
            "temperature_c": main.get("temp"),
            "feels_like_c": main.get("feels_like"),
            "temperature_min_c": main.get("temp_min"),
            "temperature_max_c": main.get("temp_max"),
            "pressure_hpa": main.get("pressure"),
            "humidity_pct": main.get("humidity"),
            "wind_speed_ms": wind.get("speed"),
            "wind_direction_deg": wind.get("deg"),
            "cloud_cover_pct": clouds.get("all"),
            "visibility_m": data.get("visibility"),
            "weather_condition": weather.get("main"),
            "weather_description": weather.get("description"),
            "weather_icon": weather.get("icon"),
            "ingested_at": datetime.now(timezone.utc)
        }

        records.append(record)

    df = pd.DataFrame(records)

    df["recorded_at"] = df["recorded_at"].astype(str)
    df["ingested_at"] = df["ingested_at"].astype(str)

    return df


def validate_weather_data(df):
    """
    Basic data validation.
    """

    required_columns = [
        "city",
        "country",
        "recorded_at",
        "temperature_c",
        "humidity_pct"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Weather DataFrame is empty.")

    return True


if __name__ == "__main__":
    print("Transformation module loaded successfully.")