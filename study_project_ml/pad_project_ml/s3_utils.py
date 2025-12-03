import os
from pathlib import Path
import boto3
from loguru import logger

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://localhost:9000"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

RAW_BUCKET = os.getenv("RAW_BUCKET", "study-project-data")
PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", RAW_BUCKET)

def upload_to_s3(file_path: Path, bucket: str = RAW_BUCKET, key: str | None = None) -> None:
    key = key or file_path.name
    logger.info(f"⬆️  Upload {file_path} →  s3://{bucket}/{key}")
    s3.upload_file(str(file_path), bucket, key)
    logger.success("✅  Upload complete")


def download_from_s3(key: str, bucket: str = RAW_BUCKET, target_dir: Path = RAW_DIR) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    local_path = target_dir / key
    logger.info(f"⬇️  Download s3://{bucket}/{key} →  {local_path}")
    s3.download_file(bucket, key, str(local_path))
    logger.success("✅  Download complete")
    return local_path