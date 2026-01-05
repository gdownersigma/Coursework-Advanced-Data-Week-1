import logging
import sys
import extract
import transform
import load
import argparse
from dotenv import load_dotenv
import os
from os import environ as ENV

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
        '--secret-key', type=str, default=ENV['AWS_SECRET_KEY'],
        help='AWS Secret Key'
    )
    parser.add_argument(
        '--access-key', type=str, default=ENV['AWS_ACCESS_KEY'],
        help='AWS Access Key'
    )
    parser.add_argument(
        '-p', '--push', action='store_true',
        help='Push data to the database after processing'
    )
    parser.add_argument(
        '-se', '--skip-extract', action='store_true',
        help='Skip the extraction step - pull straight from local files'
    )
    parser.add_argument(
        '-bucket', '--bucket-name', type=str, default='sigma-resources-museum',
        help='Name of the S3 bucket to extract data from'
    )

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


def extract_data(access_key: str, secret_key: str, logger: logging.Logger, bucket_name: str) -> None:
    """Extract data from S3 bucket."""
    s3_client = extract.get_s3_client({
        'AWS_ACCESS_KEY': access_key,
        'AWS_SECRET_KEY': secret_key
    })
    objects = extract.list_objects(s3_client, bucket_name)
    logger.info(f'Found {len(objects)} objects in bucket {bucket_name}')
    extract.download_objects(s3_client, bucket_name, objects)


def transform_json_data(logger: logging.Logger) -> None:
    """Transform JSON data by combining files and saving to CSV."""
    json_files = transform.find_json_files()
    logger.info(f'Found {len(json_files)} JSON files to process')
    combined_json_df = transform.combine_jsons(json_files)
    transform.save_to_csv(combined_json_df)


def transform_csv_data(logger: logging.Logger) -> None:
    """Transform CSV data by combining files into a single CSV."""
    all_files = os.listdir('./bucket_data')
    csv_files = transform.find_csv_files(all_files)
    logger.info(f'Found {len(csv_files)} CSV files to process')
    output_file = './combined_data/combined_museum_data.csv'
    transform.combine_csv_files(csv_files, output_file)


def transform_data(logger: logging.Logger) -> None:
    """Transform the data by combining JSON and returning to a CSV file,
    then combining CSV files into a single CSV file."""
    # Transform JSON files
    transform_json_data(logger)
    # Transform CSV files
    transform_csv_data(logger)


    # Call it early in your main script
if __name__ == '__main__':
    logger = setup_logging('INFO')
    logger.info('Pipeline started')
    args = parse_arguments()

    if not args.skip_extract:
        logger.info('Starting data extraction from S3 bucket')
        extract_data(args.access_key, args.secret_key,
                     logger, args.bucket_name)
        logger.info('Data extraction completed')
    else:
        logger.info('Skipping data extraction step as per argument')

    logger.info('Starting data transformation')
    transform_data(logger)
    logger.info('Data transformation completed')
    if args.push:
        load.load_data_to_db({
            'DB_NAME': args.db_name,
            'DB_USER': args.db_user,
            'DB_PASSWORD': args.db_password,
            'DB_HOST': args.db_host,
            'DB_PORT': args.db_port
        }, logger)
    else:
        logger.info('Skipping data push to database step as per argument')
