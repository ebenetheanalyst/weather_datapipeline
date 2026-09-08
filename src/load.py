import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """
    Create a PostgreSQL database connection.
    """

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "weather_db"),
        user=os.getenv("POSTGRES_USER", "weather_user"),
        password=os.getenv("POSTGRES_PASSWORD", "weather_password")
    )


def create_tables():
    """
    Create database tables from SQL file.
    """

    sql_path = (
        Path(__file__).resolve().parent.parent
        / "sql"
        / "create_tables.sql"
    )

    with open(sql_path, "r", encoding="utf-8") as file:
        sql = file.read()

    connection = get_connection()

    try:

        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

        print("Database tables created successfully.")

    finally:
        connection.close()


def load_weather_data(df):
    """
    Insert transformed weather data into PostgreSQL.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            for _, row in df.iterrows():

                # Insert location
                cursor.execute(
                    """
                    INSERT INTO locations (
                        city,
                        country,
                        latitude,
                        longitude
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (city, country)
                    DO UPDATE SET
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude
                    RETURNING location_id;
                    """,
                    (
                        row["city"],
                        row["country"],
                        row["latitude"],
                        row["longitude"]
                    )
                )

                location_id = cursor.fetchone()[0]

                # Insert weather observation
                cursor.execute(
                    """
                    INSERT INTO weather_observations (
                        location_id,
                        recorded_at,
                        temperature_c,
                        feels_like_c,
                        temperature_min_c,
                        temperature_max_c,
                        pressure_hpa,
                        humidity_pct,
                        wind_speed_ms,
                        wind_direction_deg,
                        cloud_cover_pct,
                        visibility_m,
                        weather_condition,
                        weather_description,
                        weather_icon,
                        ingested_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    );
                    """,
                    (
                        location_id,
                        row["recorded_at"],
                        row["temperature_c"],
                        row["feels_like_c"],
                        row["temperature_min_c"],
                        row["temperature_max_c"],
                        row["pressure_hpa"],
                        row["humidity_pct"],
                        row["wind_speed_ms"],
                        row["wind_direction_deg"],
                        row["cloud_cover_pct"],
                        row["visibility_m"],
                        row["weather_condition"],
                        row["weather_description"],
                        row["weather_icon"],
                        row["ingested_at"]
                    )
                )

        connection.commit()

        print(
            f"Successfully loaded {len(df)} weather records."
        )

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()