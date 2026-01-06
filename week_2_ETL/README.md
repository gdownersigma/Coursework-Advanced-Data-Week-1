# Realtime Museum Kiosk Pipeline

A Python ETL pipeline that consumes live kiosk interaction data from a Kafka stream and loads it into a PostgreSQL database in realtime.

## Overview

This pipeline connects to a Kafka topic (`lmnh`) containing museum kiosk interactions, validates and cleans each message, then inserts it into the appropriate database table:
- **Reviews** (ratings 0-4) → `review` table
- **Incidents** (help requests/emergencies) → `incident` table

## Prerequisites

- Python 3.8+
- PostgreSQL database with schema already set up
- Access to the Kafka cluster
- Required Python packages: `confluent-kafka`, `psycopg2`, `python-dotenv`

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project directory:

```env
# Kafka configuration
BOOTSTRAP_SERVERS=your_kafka_server:9092
SECURITY_PROTOCOL=SASL_SSL
SASL_MECHANISM=PLAIN
USERNAME=your_kafka_username
PASSWORD=your_kafka_password
USER_GROUP=your_consumer_group

# Database configuration
DB_NAME=museum
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

## Usage

### Basic usage

```bash
python realtime_pipeline.py
```

### With command line arguments

```bash
python realtime_pipeline.py --db-name museum --db-host localhost --db-port 5432
```

### Available arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--db-name` | `DB_NAME` env var | Database name |
| `--db-user` | `DB_USER` env var | Database user |
| `--db-password` | `DB_PASSWORD` env var | Database password |
| `--db-host` | `localhost` | Database host |
| `--db-port` | `5432` | Database port |

## Data Validation

Messages are validated against the following rules:

- Must contain `site` and `val` fields
- `site` must be 0-5 (valid exhibition kiosks)
- `val` must be -1 to 4 (ratings or incident flag)
- `type` must be 0 or 1 if present (incident type)
- Timestamp must be within operating hours (08:45 - 18:15)

Invalid messages are logged and skipped.

## Logging

Logs are written to both the console and `pipeline.log`. Log entries include:
- Pipeline start/stop events
- Database connection status
- Each received message
- Validation failures
- Successful inserts
- Any errors encountered

## Stopping the Pipeline

Press `Ctrl+C` to gracefully shut down. The pipeline will:
1. Stop consuming messages
2. Close the Kafka consumer (committing offsets)
3. Close the database connection

## Project Structure

```
├── realtime_pipeline.py   # Main pipeline script
├── consumer.py            # Kafka consumer, validation, cleaning functions
├── load.py                # Database connection and insert functions
├── schema.sql             # Database schema
├── ../.env                   # Configuration (not in version control)
└── pipeline.log           # Log output
```

## Troubleshooting

**No messages being consumed**
- Check your `USER_GROUP` — try a new group ID to read from the beginning
- Verify Kafka credentials in `.env`

**Database insert failures**
- Ensure the schema has been run first
- Check that exhibition data exists (foreign key constraint)

**All messages marked invalid**
- Verify the current time is within operating hours (08:45 - 18:15)
- Check the validation logic matches your data format

### README Creation
This was generated using AI but checked and updated to ensure validity.