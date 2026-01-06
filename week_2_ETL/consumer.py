"""A small script to consume messages from the lmnh kafka topic"""

import logging
from os import environ
from dotenv import load_dotenv
from confluent_kafka import Consumer
import json
from datetime import datetime, time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kiosk_consumer.log'),
        logging.StreamHandler()
    ]
)


def validate_message(data: dict) -> bool:
    """Returns True if message is valid and should be processed."""

    # Must have val & site
    if "val" not in data or "site" not in data:
        return False
    if data['val'] not in [-1, 0, 1, 2, 3, 4]:
        return False
    if data['site'] not in ['0', '1', '2', '3', '4', '5']:
        return False

    if "type" in data:
        if data['val'] != '-1' and data['type'] not in [0, 1]:
            return False

    if "at" not in data:
        data["at"] = datetime.now().isoformat()

    if data["at"]:
        timestamp = datetime.fromisoformat(data["at"].replace("+00:00", ""))

    if not (time(8, 45) <= timestamp.time() <= time(18, 15)):
        return False

    return True


def clean_message(data: dict):
    """Returns a cleaned version of the message."""
    data_to_send = {
        "at": data["at"],
        "site": int(data["site"]),
        "val": data["val"]
    }
    if "type" in data:
        data_to_send["type"] = data["type"]
    return data_to_send


if __name__ == "__main__":
    load_dotenv()

    kafka_consumer = Consumer({
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        'security.protocol': environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': environ["SASL_MECHANISM"],
        'sasl.username': environ["USERNAME"],
        'sasl.password': environ["PASSWORD"],
        'group.id': environ["USER_GROUP"]
    })
    kafka_consumer.subscribe(["lmnh"])  # add this
    logging.info("Starting Kafka consumer for topic 'lmnh'")
    try:
        while True:
            msg = kafka_consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Kafka error: {msg.error()}")
            else:
                logging.info(
                    f"Received message: {msg.timestamp()} {msg.value().decode('utf-8')}")
                data = json.loads(msg.value().decode("utf-8"))
                if validate_message(data):
                    cleaned_data = clean_message(data)
                    logging.info(f"Cleaned data: {cleaned_data}")

                else:
                    logging.warning(f"Invalid message skipped: {data}")

    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing Kafka consumer")
        kafka_consumer.close()  # commits offsets and cleans up
