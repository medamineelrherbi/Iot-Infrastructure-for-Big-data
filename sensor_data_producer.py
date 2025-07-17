from kafka import KafkaProducer
import json, time, random
from datetime import datetime


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(50):
    # Randomly choose message type
    msg_type = random.choice(['env', 'vibration'])

    if msg_type == 'env':
        msg = {
            "type": "env",
            "device_id": f"sensor_{random.randint(1, 10)}",
            "temperature": round(random.uniform(20, 40), 2),
            "humidity": round(random.uniform(30, 80), 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    else:  # vibration type
        msg = {
            "type": "vibration",
            "device_id": f"vib_sensor_{random.randint(1, 10)}",
            "vibration_level": round(random.uniform(0.1, 5.0), 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    producer.send("iot-data", msg)
    print("Sent:", msg)
    time.sleep(1)
