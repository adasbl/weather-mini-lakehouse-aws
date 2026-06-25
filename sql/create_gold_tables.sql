-- Creating an analytical table in the Gold layer using Amazon Athena
-- Before running, replace <your-bucket-name> with the actual name of your S3 bucket

CREATE TABLE "weather-lakehouse-aseied"."daily_weather_summary"
WITH (
  format = 'PARQUET',
  external_location = 's3://<your-bucket-name>/gold/daily_weather_summary/'
) AS
SELECT 
    station_id,
    CAST(timestamp AS DATE) AS measurement_date,
    COUNT(*) AS total_measurements,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    MAX(temperature) AS max_temperature,
    MIN(temperature) AS min_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(SUM(rain_mm), 2) AS total_rain_mm
FROM 
    "weather-lakehouse-aseied"."silver"
GROUP BY 
    station_id, 
    CAST(timestamp AS DATE);