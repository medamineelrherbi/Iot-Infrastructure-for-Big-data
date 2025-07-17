FROM bitnami/spark:3.4.1

WORKDIR /opt/bitnami/spark

# Installer curl
USER root
RUN install_packages curl

# Télécharger les JARs nécessaires pour Kafka
RUN curl -L -o jars/spark-sql-kafka-0-10_2.12-3.4.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar && \
    curl -L -o jars/kafka-clients-3.2.0.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.2.0/kafka-clients-3.2.0.jar && \
    curl -L -o jars/spark-token-provider-kafka-0-10_2.12-3.4.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.4.1/spark-token-provider-kafka-0-10_2.12-3.4.1.jar

# Copier ton script Spark
COPY spark/spark_streaming.py /opt/bitnami/spark/work-dir/spark_streaming.py
