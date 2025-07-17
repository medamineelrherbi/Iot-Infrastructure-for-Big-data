FROM apache/spark:3.4.1-python3

# Copier les jars Kafka + ClickHouse dans le dossier jars de Spark
COPY spark_jars/*.jar /opt/spark/jars/

# Copier le script PySpark dans le dossier de travail Spark
COPY spark/spark_streaming.py /opt/spark/work-dir/

# Mettre le dossier de travail par défaut
WORKDIR /opt/spark/work-dir

# Par défaut, lancer le master (tu peux overrider dans docker-compose)
CMD ["/opt/spark/sbin/start-master.sh", "&&", "tail", "-f", "/opt/spark/logs/*master*.out"]
