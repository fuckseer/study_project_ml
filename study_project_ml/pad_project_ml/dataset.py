import os
import boto3
from loguru import logger
from pathlib import Path

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

RAW_BUCKET = os.getenv("RAW_BUCKET", "study-project-data")
RAW_DATA_DIR = Path("data/raw")

def upload_raw_dataset():
    path = RAW_DATA_DIR / "titanic.csv"
    logger.info(f"Uploading {path} → s3://{RAW_BUCKET}")
    s3.upload_file(str(path), RAW_BUCKET, "titanic.csv")
    logger.success("Upload complete.")
