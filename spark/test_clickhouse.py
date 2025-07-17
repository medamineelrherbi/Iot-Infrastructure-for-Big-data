from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestClickHouseJDBC") \
    .master("local[*]") \
    .getOrCreate()

try:
    df = spark.read.format("jdbc") \
        .option("url", "jdbc:clickhouse://clickhouse:8123/iot_data?user=admin&password=admin") \
        .option("dbtable", "iot_env") \
        .load()

    df.show(5)
    print("Connexion JDBC réussie !")
except Exception as e:
    print("Erreur lors de la connexion JDBC :", e)
