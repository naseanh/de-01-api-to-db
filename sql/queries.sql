-- ============================================================
-- Purpose: Common queries for the weather_observations table
-- Scope: Phase 1 (basic validation + analytics queries)
-- ============================================================


-- ============================================================
-- Query 1: Latest Observations
-- Purpose:
--   Retrieve the most recent weather observations across all locations.
-- ============================================================

SELECT
    location,
    temperature_c,
    temperature_f,
    wind_speed_kmh,
    wind_speed_mph,
    observed_at
FROM weather_observations
ORDER BY observed_at DESC
LIMIT 5;


-- ============================================================
-- Query 2: Filter by Location
-- Purpose:
--   Retrieve recent observations for a specific location.
-- Notes:
--   Update the location value as needed.
-- ============================================================

SELECT
    location,
    temperature_c,
    temperature_f,
    wind_speed_kmh,
    wind_speed_mph,
    observed_at
FROM weather_observations
WHERE location = 'Augusta, GA'
ORDER BY observed_at DESC;


-- ============================================================
-- Query 3: Recent Time Window
-- Purpose:
--   Retrieve observations from the last 1 hour.
-- ============================================================

SELECT
    location,
    temperature_c,
    temperature_f,
    wind_speed_kmh,
    wind_speed_mph,
    observed_at
FROM weather_observations
WHERE observed_at >= NOW() - INTERVAL '1 hour'
ORDER BY observed_at DESC;


-- ============================================================
-- Query 4: Aggregation (Average Metrics by Location)
-- Purpose:
--   Compute average temperature and wind speed per location.
-- ============================================================

SELECT
    location,
    ROUND(AVG(temperature_c)::numeric, 2) AS avg_temp_c,
    ROUND(AVG(temperature_f)::numeric, 2) AS avg_temp_f,
    ROUND(AVG(wind_speed_kmh)::numeric, 2) AS avg_wind_kmh,
    ROUND(AVG(wind_speed_mph)::numeric, 2) AS avg_wind_mph
FROM weather_observations
GROUP BY location;


-- ============================================================
-- Query 5: Record Count
-- Purpose:
--   Validate how many records exist in the table.
-- ============================================================

SELECT COUNT(*) AS total_records
FROM weather_observations;


-- ============================================================
-- Query 6: Raw Table Inspection
-- Purpose:
--   Debugging / full table view (use cautiously for large datasets).
-- ============================================================

SELECT *
FROM weather_observations
ORDER BY observed_at DESC;