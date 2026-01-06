"""Realtime ETL pipeline consuming from Kafka and loading to database."""

import logging
import json
import sys
from consumer import validate_message, clean_message
from load import get_db_connection, insert_kiosk_data
import argparse
from dotenv import load_dotenv
from os import environ as ENV
from confluent_kafka import Consumer

load_dotenv()

# Configure logging at the top of script.


def setup_logging(log_level='INFO'):
    """Set up logging to file and console"""

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler - logs to file
    file_handler = logging.FileHandler('pipeline.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler - logs to terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def parse_arguments():
    """Parse command-line arguments for the pipeline."""

    parser = argparse.ArgumentParser(
        description='ETL Pipeline for Museum Data')

    parser.add_argument(
        '--db-name', type=str, default=ENV.get('DB_NAME', 'museum'),
        help='Database name'
    )
    parser.add_argument(
        '--db-user', type=str, default=ENV.get('DB_USER', ''),
        help='Database user'
    )
    parser.add_argument(
        '--db-password', type=str, default=ENV.get('DB_PASSWORD', ''),
        help='Database password'
    )
    parser.add_argument(
        '--db-host', type=str, default=ENV.get('DB_HOST', 'localhost'),
        help='Database host (default: localhost)'
    )
    parser.add_argument(
        '--db-port', type=str, default=ENV.get('DB_PORT', '5432'),
        help='Database port (default: 5432)'
    )
    return parser.parse_args()


def run_kafka_consumer(db_connection, logger):
    """Consume messages from Kafka, validate, clean, and load to database."""

    kafka_consumer = Consumer({
        "bootstrap.servers": ENV["BOOTSTRAP_SERVERS"],
        "security.protocol": ENV["SECURITY_PROTOCOL"],
        "sasl.mechanisms": ENV["SASL_MECHANISM"],
        "sasl.username": ENV["USERNAME"],
        "sasl.password": ENV["PASSWORD"],
        "group.id": ENV["USER_GROUP"]
    })

    kafka_consumer.subscribe(["lmnh"])
    logger.info("Starting Kafka consumer for topic 'lmnh'")

    try:
        while True:
            msg = kafka_consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            logger.info(f"Received message: {msg.value().decode('utf-8')}")
            data = json.loads(msg.value().decode("utf-8"))

            if validate_message(data):
                cleaned_data = clean_message(data)
                logger.info(f"Cleaned Data... inserting data...")
                insert_kiosk_data(db_connection, cleaned_data, logger)
                logger.info(f"Data inserted successfully.")
            else:
                logger.warning(f"Invalid message skipped: {data}")

    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        logger.info("Closing Kafka consumer")
        kafka_consumer.close()


# Call it early in your main script
if __name__ == '__main__':
    logger = setup_logging('INFO')
    logger.info('Pipeline started')
    args = parse_arguments()

    conn = get_db_connection({
        'DB_NAME': args.db_name,
        'DB_USER': args.db_user,
        'DB_PASSWORD': args.db_password,
        'DB_HOST': args.db_host,
        'DB_PORT': args.db_port
    })
    logger.info('Database connection established')

    run_kafka_consumer(conn, logger)
