-- Crée la base de données si elle n'existe pas déjà
CREATE DATABASE IF NOT EXISTS iot_data;

-- Utiliser la base
USE iot_data;

CREATE TABLE IF NOT EXISTS iot_env (
  device_id String,
  temperature Float32,
  humidity Float32,
  timestamp String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS iot_env_danger (
  device_id String,
  temperature Float32,
  humidity Float32,
  timestamp String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS iot_vibration (
  device_id String,
  vibration_level Float32,
  timestamp String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS iot_vib_danger (
  device_id String,
  vibration_level Float32,
  timestamp String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS iot_env_avg_1min (
  device_id String,
  window_start DateTime,
  window_end DateTime,
  avg_temp Float32,
  avg_humidity Float32
) ENGINE = MergeTree()
ORDER BY window_start;

