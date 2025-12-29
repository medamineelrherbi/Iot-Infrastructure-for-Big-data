# 🚀 Real-Time IoT Data Infrastructure with Kafka, Spark, ClickHouse & Superset

![Architecture](./assets/architecture.png)
## Demo Video

🎥 Watch the demonstration:  


<p align="center">
  <video src="https://github.com/user-attachments/assets/adac1090-fbc7-4a49-a51f-723df3db1098" width="100%" controls>
    Your browser does not support the video tag.
  </video>
</p>

---

## 📌 Project Overview

This project builds a real-time Big Data pipeline that ingests, processes, stores, and visualizes data from IoT sensors. The architecture leverages containerized technologies orchestrated with Docker Compose, making it portable and reproducible.

### 🎯 Objectives:

- Simulate IoT sensor data (temperature, humidity, vibration)
- Ingest data through Apache Kafka
- Process data in real-time using Apache Spark Structured Streaming
- Persist both **normal** and **dangerous** data into ClickHouse
- Visualize insights and alerts using Apache Superset

---

## 🧱 Architecture

- **Kafka**: Ingests IoT data streams
- **Spark**: Consumes Kafka topics, applies logic, and writes data to ClickHouse
- **ClickHouse**: Serves as a fast OLAP database for storing and querying time-series data
- **Superset**: Builds interactive dashboards for business intelligence

---

## ⚙️ Services (Docker Compose)

```yaml
# (Only summarized here – see full docker-compose.yml in this repo)
- kafka: Bitnami Kafka with Kraft mode enabled
- spark-master & spark-worker: Custom Spark image to enable batch/streaming jobs
- clickhouse: Lightweight columnar DB for analytics
- superset: Data visualization and dashboarding tool
All services are configured to communicate internally in the Docker network, with external ports exposed as needed.
```

🚀 Getting Started
1. Clone the repo:
```
git clone https://github.com/medamineelrherbi/Iot-Infrastructure-for-Big-data
```
2. Run the stack:
```
docker-compose up --build
```
Wait for all services (especially Spark & ClickHouse) to start. Superset may take ~30 seconds on the first run.

3. Access UIs:
```
Service	URL	Credentials
Superset	http://localhost:8088	admin / admin
Spark UI	http://localhost:8080	-
ClickHouse	http://localhost:8123	admin / admin
```
4. to create a kafka topic (iot-data) execute the following
``` 
docker exec -it kafka kafka-topics.sh --create --topic iot-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
5. to run the spark job execute the following in the cmd
```
docker exec -it spark-master /bin/bash -c "spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/work-dir/spark_streaming.py"
```
📊 Dashboards (Apache Superset)
Once the pipeline is running, Superset dashboards will present:

Real-Time Temperature & Humidity Monitoring

Vibration Levels per Device

Alert Count and Trend over Time

Device-specific Analysis

📷 Sample Visualizations:
![Architecture](./assets/Capture1.PNG)
![Architecture](./assets/Capture2.PNG)
![Architecture](./assets/Capture3.PNG)
![Architecture](./assets/Capture4.PNG)
![Architecture](./assets/Capture5.PNG)
![Architecture](./assets/Capture6.PNG)
![Architecture](./assets/Capture7.PNG)


💻 Tech Stack
Tool	Purpose
Kafka	Stream ingestion
Spark	Stream processing
ClickHouse	Fast time-series database
Superset	Dashboards and BI
Docker Compose	Orchestration of services
```
🧠 How it Works
A Python IoT simulator (run locally) sends JSON messages to Kafka

Spark reads messages using Structured Streaming

It filters “dangerous” combinations and aggregates the data by one-minute intervals. (e.g. high vibration, a dangerous combination between temperature and humidity "temp > 70 & humidity > 35")

Writes 4   ClickHouse tables: iot_env, iot_env_danger, iot_vibration, iot_vib_danger, iot_env_avg_1min

Superset queries ClickHouse directly using SQLAlchemy to visualize trends
```
📁 Project Structure
```
.
├── docker-compose.yml
├── Dockerfile
├── sensor_data_producer.py
├── spark/
│   └── spark_streaming.py
│   └── test_clickhouse.py
├── clickhouse/
│   ├── init.sql
│   └── users.xml
├── assets/
│   ├── architecture.png
│   ├── pictures and videos
├── spark_jars/
│   ├── clickhouse-jdbc-0.3.2.jar
│   ├── kafka-clients-3.4.1.jar
│   ├── spark-sql-kafka...
└── README.md

👨‍💻 Author
Mohamed Amine El Rherbi

📧 medamineelrherbi@gmail.com

💼 LinkedIn

🧠 Passionate about Big Data, Cloud, and AI

📝 License
This project is licensed under the MIT License.
```


---
