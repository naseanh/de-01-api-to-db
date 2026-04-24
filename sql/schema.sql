-- Table: weather_observations
-- Purpose:
--   Stores normalized weather observation data ingested from the Open-Meteo API.

-- Description:
--   Each row represents a single weather observation for a specific location
--   at a given point in time. Data is used for analytics, time-series queries,
--   and downstream processing.

-- Design Notes:
--   - Enforces uniqueness per (location, observed_at) to prevent duplicate ingestion
--   - Uses TIMESTAMPTZ for timezone-safe operations
--   - Optimized for time-based and location-based queries
CREATE TABLE IF NOT EXISTS weather_observations (
    id SERIAL PRIMARY KEY, -- Unique identifier for each observation
    location VARCHAR(100) NOT NULL, -- Human-readable location name (e.g., 'Baltimore')
    latitude DOUBLE PRECISION NOT NULL, -- Geographic latitude coordinate
    longitude DOUBLE PRECISION NOT NULL, -- Geographic longitude coordinate
    temperature_c DOUBLE PRECISION NOT NULL, -- Temperature in Celsius
    wind_speed_kmh DOUBLE PRECISION NOT NULL, -- Wind speed in kilometers per hour
    observed_at TIMESTAMPTZ NOT NULL, -- Timestamp when the observation was recorded (source time)
    ingested_at TIMESTAMPTZ DEFAULT NOW(), -- Timestamp when the record was inserted into DB
    CONSTRAINT unique_observation UNIQUE (location, observed_at) -- Prevent duplicate observations
);

-- Index: idx_weather_location_time
-- Purpose:
--   Optimizes queries filtering by location and ordering by most recent observations
--   (common pattern for dashboards and APIs)
CREATE INDEX IF NOT EXISTS idx_weather_location_time
ON weather_observations (location, observed_at DESC);