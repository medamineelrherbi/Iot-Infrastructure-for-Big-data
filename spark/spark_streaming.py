from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.functions import window, avg
from pyspark.sql.functions import to_timestamp
from pyspark.sql.types import StructType, StringType, FloatType



# DANS spark_streaming.py

spark = SparkSession.builder \
    .appName("IoTStreamProcessor") \
    .master("spark://" \
    "spark-master:7077") \
    .getOrCreate()
# Schema with all possible fields and a "type" field
schema = StructType() \
    .add("type", StringType()) \
    .add("device_id", StringType()) \
    .add("temperature", FloatType()) \
    .add("humidity", FloatType()) \
    .add("vibration_level", FloatType()) \
    .add("timestamp", StringType())

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9093") \
    .option("subscribe", "iot-data") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json")
data_df = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

# Separate DataFrames for each type
env_df = data_df.filter(col("type") == "env").select("device_id", "temperature", "humidity", "timestamp")
vib_df = data_df.filter(col("type") == "vibration").select("device_id", "vibration_level", "timestamp")

# Example: Detect dangerous env data
danger_env_df = env_df.filter("temperature > 35 AND humidity > 70")

# Example: Detect high vibration
danger_vib_df = vib_df.filter("vibration_level > 4.0")

# Convert string timestamp to actual timestamp
env_df = env_df.withColumn("timestamp", to_timestamp("timestamp"))

# Add watermark to handle late data
aggregated_df = env_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("device_id")
    ).agg(
        avg("temperature").alias("avg_temp"),
        avg("humidity").alias("avg_humidity")
    )

# Write functions for each sink (ClickHouse tables)
def write_env(batch_df, epoch_id):
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
        .option("dbtable", "iot_env") \
        .mode("append") \
        .save()

def write_vib(batch_df, epoch_id):
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
        .option("dbtable", "iot_vibration") \
        .mode("append") \
        .save()

def write_danger_env(batch_df, epoch_id):
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
        .option("dbtable", "iot_env_danger") \
        .mode("append") \
        .save()

def write_danger_vib(batch_df, epoch_id): # the arguments (batch_id,epoch_id) are necessary to be passed to foreachBatch
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
        .option("dbtable", "iot_vib_danger") \
        .mode("append") \
        .save()

def write_avg(batch_df, epoch_id):
    batch_df.selectExpr(
        "device_id",
        "window.start as window_start",
        "window.end as window_end",
        "avg_temp",
        "avg_humidity"
    ).write.format("jdbc") \
      .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
      .option("dbtable", "iot_env_avg_1min") \
      .mode("append") \
      .save()

# Start streaming writes
env_df.writeStream.foreachBatch(write_env).start()
'''
writeStream : Starts defining how the stream should output the data.
foreachBatch : For each micro-batch of data, call the Python function write_env(batch_df, epoch_id).
start() : Starts the continuous streaming job. Without .start(), nothing runs.
'''
vib_df.writeStream.foreachBatch(write_vib).start()
danger_env_df.writeStream.foreachBatch(write_danger_env).start()
danger_vib_df.writeStream.foreachBatch(write_danger_vib).start()
aggregated_df.writeStream.foreachBatch(write_avg).outputMode("update").start()

spark.streams.awaitAnyTermination()