CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(10) NOT NULL,
    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,

    CONSTRAINT unique_location
        UNIQUE (city, country)
);


CREATE TABLE IF NOT EXISTS weather_observations (
    observation_id BIGSERIAL PRIMARY KEY,

    location_id INTEGER NOT NULL,

    recorded_at TIMESTAMPTZ NOT NULL,

    temperature_c NUMERIC(6, 2),
    feels_like_c NUMERIC(6, 2),
    temperature_min_c NUMERIC(6, 2),
    temperature_max_c NUMERIC(6, 2),

    pressure_hpa INTEGER,
    humidity_pct INTEGER,

    wind_speed_ms NUMERIC(8, 2),
    wind_direction_deg INTEGER,

    cloud_cover_pct INTEGER,
    visibility_m INTEGER,

    weather_condition VARCHAR(100),
    weather_description VARCHAR(255),
    weather_icon VARCHAR(20),

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
        REFERENCES locations(location_id)
);


CREATE INDEX IF NOT EXISTS idx_weather_recorded_at
ON weather_observations(recorded_at);


CREATE INDEX IF NOT EXISTS idx_weather_location
ON weather_observations(location_id);