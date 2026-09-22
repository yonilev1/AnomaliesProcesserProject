import json
import logging
import os
import pandas as pd
from confluent_kafka import Producer
import time

logging.basicConfig(
    filename='/app/logs/project_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id':'python-producer'
}

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to topic {msg.topic()} partition: [{msg.partition()}]")

def main():
    #logger.info("Waiting 15 seconds for Kafka to start...")
    #time.sleep(15)

    #logger.info("Connecting to Kafka...")
    producer = Producer(config)

    csv_file_path = "/app/activity_readings.csv"
    if os.path.exists(csv_file_path):
        csv_data = pd.read_csv(csv_file_path)
        csv_data = csv_data.sort_values('timestamp')
        for line in csv_data.to_dict(orient='records'):
            message = json.dumps(line)
            producer.produce('activity-readings', value=message, callback=delivery_report)
            producer.poll(0)
        producer.flush()
        logger.info("Finished sending messages to Kafka.")
    else:
        logger.warning(f"File {csv_file_path} not found.")

if __name__ == "__main__":
    main()