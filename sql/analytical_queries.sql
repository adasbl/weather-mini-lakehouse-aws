-- Anomaly report: Identification of days with the highest recorded temperatures
SELECT * FROM "weather-lakehouse-aseied"."daily_weather_summary"
WHERE max_temperature > 20.0
ORDER BY max_temperature DESC;