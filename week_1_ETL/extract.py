"""Script to download museum data from S3 bucket"""

from os import environ as ENV, _Environ
from dotenv import load_dotenv
from boto3 import client


def get_s3_client(config: dict) -> client:
    """Return an S3 client using provided configuration"""
    s3 = client(service_name='s3',
                aws_access_key_id=config['AWS_ACCESS_KEY'],
                aws_secret_access_key=config["AWS_SECRET_KEY"])
    return s3


def list_buckets(s3_client: client):
    """Return a list of bucket names"""
    buckets = s3_client.list_buckets()["Buckets"]
    return [b["Name"] for b in buckets]


def list_objects(s3_client: client, bucket_name: str):
    """Return a list of bucket object names"""
    objects = s3_client.list_objects(Bucket=bucket_name)['Contents']
    return [o["Key"] for o in objects]


def download_objects(s3_client: client, bucket_name: str, objects: list[str]):
    """Download objects from S3 bucket if the name begins with 'lmnh'"""
    for o in objects:
        if o.startswith('lmnh'):
            s3_client.download_file(
                Bucket=bucket_name, Key=o, Filename=f'./bucket_data/{o}')


if __name__ == "__main__":
    load_dotenv()
    s3 = get_s3_client(ENV)
    objects = list_objects(s3, 'sigma-resources-museum')

    download_objects(s3, "sigma-resources-museum", objects)
