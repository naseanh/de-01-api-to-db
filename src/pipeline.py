"""
pipeline.py — Phase 1: Basic API-to-PostgreSQL ETL Pipeline

Purpose:
    Extract current weather data from the Open-Meteo API, transform it into
    a normalized record, and load it into PostgreSQL.

Source:
    Open-Meteo API, no API key required.

Destination:
    PostgreSQL table: weather_observations

Pipeline Flow:
    Extract → Transform → Load

Notes:
    - Uses environment variables for configuration.
    - Supports default + override location configuration.
    - Uses parameterized SQL to prevent SQL injection.
    - Uses context managers to safely manage database connections/cursors.
"""

import os
from datetime import datetime
import time
import logging

import psycopg2
import requests
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


# Load environment variables from .env into the Python runtime.
load_dotenv()


# =========================
# DATABASE CONFIGURATION
# =========================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "dbname": os.getenv("DB_NAME", "pipeline_db"),
    "user": os.getenv("DB_USER", "pipeline_user"),
    "password": os.getenv("DB_PASSWORD"),
    # Note: If DB_PASSWORD is wrong or missing, the pipeline will fail
    # with an authentication error when trying to connect to PostgreSQL.
    # Expected: psycopg2.OperationalError: FATAL: password authentication failed
}


# =========================
# LOCATION CONFIGURATION
# =========================

# Defaults (fallback)
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Baltimore, MD")
DEFAULT_LATITUDE = os.getenv("DEFAULT_LATITUDE", "39.2904")
DEFAULT_LONGITUDE = os.getenv("DEFAULT_LONGITUDE", "-76.6122")

# Overrides (runtime)
WEATHER_LOCATION = os.getenv("WEATHER_LOCATION") or DEFAULT_LOCATION
WEATHER_LATITUDE = os.getenv("WEATHER_LATITUDE") or DEFAULT_LATITUDE
WEATHER_LONGITUDE = os.getenv("WEATHER_LONGITUDE") or DEFAULT_LONGITUDE


# =========================
# API CONFIGURATION
# =========================
# Open-Meteo API endpoint and parameters for current weather data.

# Bad URL test1:
# API_URL = "https://api.open-meteo.com/v1/forecas"
# Missing 't' at the end of 'forecast'
# Will return a requests.exceptions.ConnectionError
# Bad URL test2:
# API_URL = "https://api.open-meteo.com/v1/forecast/notapath
# Will return a 404 Not Found error, which raises a
# requests.exceptions.HTTPError when .raise_for_status() is called.
# Good URL test:
API_URL = "https://api.open-meteo.com/v1/forecast"

API_PARAMS = {
    "latitude": WEATHER_LATITUDE,
    "longitude": WEATHER_LONGITUDE,
    "current_weather": "true",
    "wind_speed_unit": "kmh",
}


# =========================
# EXTRACT
# =========================
def extract():
    """
    Extract current weather data from the Open-Meteo API with timeout and retry handling.

    Returns:
        dict: Raw JSON response from the API.

    Raises:
        RuntimeError: If the API request fails after all retry attempts.
    """
    last_exception = None
    max_api_retries = 3
    base_retry_delay_seconds = 1

    for attempt in range(1, max_api_retries + 1):
        try:
            api_response = requests.get(
                API_URL,
                params=API_PARAMS,
                timeout=10,
            )

            api_response.raise_for_status()

            return api_response.json()

        except requests.exceptions.Timeout as exc:
            last_exception = exc

        except requests.exceptions.RequestException as exc:
            last_exception = exc

        if attempt < max_api_retries:
            delay = base_retry_delay_seconds * (2 ** (attempt - 1))
            logger.warning(
                "API request failed on attempt %s. Retrying in %s seconds.",
                attempt,
                delay
            )
            time.sleep(delay)

    raise RuntimeError(
        f"API request failed after {max_api_retries} attempts."
    ) from last_exception



# =========================
# TRANSFORM
# =========================
def transform(raw_data):
    """
    Transform raw API data into the database record format.

    Args:
        raw_data (dict): Raw weather data returned from Open-Meteo.

    Returns:
        dict: Normalized weather observation record.
    """
    current = raw_data["current_weather"]

    temp_c = current["temperature"]
    wind_kmh = current["windspeed"]

    # Unit conversions
    temp_f = (temp_c * 9 / 5) + 32
    wind_mph = wind_kmh * 0.621371

    return {
        "location": WEATHER_LOCATION,
        "latitude": raw_data["latitude"],
        "longitude": raw_data["longitude"],
        "temperature_c": temp_c,
        "temperature_f": temp_f,
        "wind_speed_kmh": wind_kmh,
        "wind_speed_mph": wind_mph,
        "observed_at": datetime.fromisoformat(current["time"]),
    }


# =========================
# LOAD
# =========================
def load(record):
    """
    Load one transformed weather observation into PostgreSQL.

    Args:
        record (dict): Normalized weather observation record.
    """
    sql = """
        INSERT INTO weather_observations
        (
            location,
            latitude,
            longitude,
            temperature_c,
            temperature_f,
            wind_speed_kmh,
            wind_speed_mph,
            observed_at
        )
        VALUES
        (
            %(location)s,
            %(latitude)s,
            %(longitude)s,
            %(temperature_c)s,
            %(temperature_f)s,
            %(wind_speed_kmh)s,
            %(wind_speed_mph)s,
            %(observed_at)s
        )
        ON CONFLICT (location, observed_at) DO NOTHING;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, record)

            # Intentionally discard transaction which will
            # cause the data not to be saved in the database.
            # Expected: Script runs with no error — but no data in DB.
            # Missing commits are a silent failure.
            # conn.rollback()


# =========================
# PIPELINE ORCHESTRATION
# =========================
def run_pipeline():
    """
    Run the full ETL pipeline: Extract → Transform → Load.
    """
    logger.info("Starting pipeline...")

    raw_data = extract()
    clean = transform(raw_data)
    load(clean)

    logger.info(
        "Pipeline complete. Location: %s | "
        "Temp: %s C / %s F | "
        "Wind: %s km/h / %s mph | "
        "Observed: %s",
        clean["location"],
        clean["temperature_c"],
        clean["temperature_f"],
        clean["wind_speed_kmh"],
        clean["wind_speed_mph"],
        clean["observed_at"],
    )


if __name__ == "__main__":
    run_pipeline()
