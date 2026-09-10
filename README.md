# Weather Data Pipeline

An end-to-end data pipeline that extracts live weather data from the OpenWeather API, transforms it, and loads it into PostgreSQL — orchestrated with Apache Airflow and fully containerized with Docker. Data can be queried directly via pgAdmin or visualized in Metabase.

## Architecture

```
OpenWeather API
      │
      ▼  (Extract)
 Airflow DAG
      │  (Transform)
      ▼
 PostgreSQL DB
      │
      ├──────────────┐
      ▼              ▼
   pgAdmin      Metabase Dashboard
 (SQL Query)   (Visualize Data)
```
<p align="center">
      <image src="image/Weather-architecture.png" alt="Weather Data Pipeline Architecture" width="600"/>
</p>

All services run as Docker containers on a shared network, orchestrated via `docker-compose.yml`.

## Tech Stack

- **Orchestration:** Apache Airflow 3 (LocalExecutor)
- **Data source:** OpenWeather API
- **Database:** PostgreSQL 16
- **Visualization:** Metabase
- **DB Admin:** pgAdmin 4
- **Language:** Python (pandas, psycopg2, requests)
- **Containerization:** Docker & Docker Compose

## Pipeline Overview

The DAG (`dags/weather_pipeline.py`) runs three tasks in sequence:

1. **Extract** (`src/extract.py`) — Fetches current weather data for a configurable list of cities (`config/cities.json`) from the OpenWeather API.
2. **Transform** (`src/transform.py`) — Cleans and reshapes the raw JSON responses into a structured pandas DataFrame (temperature, humidity, wind, cloud cover, etc.).
3. **Load** (`src/load.py`) — Upserts location data and inserts weather observations into PostgreSQL (`locations` and `weather_observations` tables).

The pipeline currently runs on an hourly schedule and can also be triggered manually from the Airflow UI.

## Getting Started

### Prerequisites
- Docker Desktop
- An [OpenWeather API key](https://openweathermap.org/api)

### Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd weather_datapipeline
   ```

2. Copy the example environment file and fill in your values:
   ```bash
   cp .env.example .env
   ```
   Required variables include `OPENWEATHER_API_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and `AIRFLOW_UID`.

3. Start all services:
   ```bash
   docker compose up -d
   ```

4. Access the services:
   | Service | URL | Notes |
   |---|---|---|
   | Airflow UI | http://localhost:8080 | Trigger and monitor the DAG |
   | pgAdmin | http://localhost:5050 | Query the database directly |
   | Metabase | http://localhost:3000 | Build dashboards |
   | PostgreSQL | localhost:5432 | Accessible from any local DB client |

5. In the Airflow UI, unpause and trigger `weather_data_pipeline` to run the pipeline manually, or let it run on its hourly schedule.

## Cities Tracked

Configured in `config/cities.json` — currently includes Abuja, Lagos, Ibadan, Kano, Port Harcourt, and Enugu. Add or remove cities by editing this file.

## Challenges Solved

Building this surfaced several real infrastructure issues beyond the ETL logic itself:

- **Metadata DB mismatch** — The Postgres volume had been initialized with different credentials than Airflow's connection string expected (env vars only apply on first init, not existing volumes). Resolved by creating the `airflow` database against the actual running Postgres user.
- **Airflow 3 internal networking** — Task subprocesses couldn't reach Airflow's own execution API, defaulting to `localhost` inside their own containers. Fixed by explicitly setting `AIRFLOW__CORE__EXECUTION_API_SERVER_URL` to point at the API server's container address.
- **Config path mismatch** — A volume mount pointed to `/opt/airflow/config_project`, while the extraction code expected `/opt/airflow/config`, causing a `FileNotFoundError`.
- **XCom serialization** — Airflow's inter-task data passing doesn't support pandas `Timestamp` objects natively; resolved by converting datetime fields to strings before task handoff.

## Project Structure

```
weather_datapipeline/
├── dags/               # Airflow DAG definitions
├── src/                # Extract, transform, load logic
├── config/             # City list and other config
├── sql/                # Database schema (create_tables.sql)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Roadmap

- [ ] Metabase dashboard for temperature/humidity trends by city
- [ ] Data quality checks / validation task in the DAG
- [ ] Deploy to a cloud VM for continuous (non-local) operation
- [ ] Historical trend analysis once enough data accumulates

## Author

Built by Sanya Ajibola Ebenezer as part of an ongoing data engineering learning project.
