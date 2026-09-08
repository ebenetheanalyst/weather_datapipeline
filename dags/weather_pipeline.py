from datetime import datetime, timedelta

from airflow.sdk import dag, task


@dag(
    dag_id="weather_data_pipeline",

    schedule="0 * * * *",

    start_date=datetime(2026, 9, 1),

    catchup=False,

    default_args={
        "owner": "weather-project",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },

    tags=["weather", "api", "postgresql", "data-engineering"],

    description="Extract weather data from OpenWeather, transform it and load it into PostgreSQL."
)
def weather_data_pipeline():

    @task
    def extract():

        import sys

        sys.path.append("/opt/airflow")

        from src.extract import extract_weather_data

        data = extract_weather_data()

        return data


    @task
    def transform(raw_data):

        import sys

        sys.path.append("/opt/airflow")

        from src.transform import (
            transform_weather_data,
            validate_weather_data
        )

        df = transform_weather_data(raw_data)

        validate_weather_data(df)

        return df.to_dict(orient="records")


    @task
    def load(transformed_data):

        import sys

        import pandas as pd

        sys.path.append("/opt/airflow")

        from src.load import load_weather_data

        df = pd.DataFrame(transformed_data)

        load_weather_data(df)

        return f"Loaded {len(df)} records."


    raw_data = extract()

    transformed_data = transform(raw_data)

    load(transformed_data)


weather_data_pipeline()