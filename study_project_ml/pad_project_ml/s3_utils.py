import os
from pathlib import Path
import boto3
from loguru import logger

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

RAW_BUCKET = os.getenv("RAW_BUCKET", "study-project-data")
PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", RAW_BUCKET)

def download_from_s3(filename: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    local_path = RAW_DIR / filename
    logger.info(f"⬇ Завантажение {filename} из S3 → {local_path}")
    s3.download_file(RAW_BUCKET, filename, str(local_path))
    logger.success("✅ Файл скачан")
    return local_path

def upload_to_s3(local_path: Path, key: str) -> None:
    logger.info(f"⬆ Отправка {local_path} → s3://{PROCESSED_BUCKET}/{key}")
    s3.upload_file(str(local_path), PROCESSED_BUCKET, key)
    logger.success("✅ Файл загружен")