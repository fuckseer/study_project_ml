from pathlib import Path
import typer
from loguru import logger

from study_project_ml.pad_project_ml.s3_utils import upload_to_s3, download_from_s3, RAW_BUCKET, PROCESSED_BUCKET
from study_project_ml.pad_project_ml.processing import process_dataset

app = typer.Typer(help="End-to-end pipeline → upload raw → download → process → upload processed.")

@app.command()
def main(
    raw_filename: str = "titanic.csv",
    processed_filename: str = "titanic_processed.csv",
) -> None:
    logger.info("🚀  Starting full pipeline")

    raw_local_path = Path("data/raw") / raw_filename

    upload_to_s3(raw_local_path, bucket=RAW_BUCKET)

    raw_file = download_from_s3(raw_filename, bucket=RAW_BUCKET, target_dir=Path("data/raw"))

    processed_path = Path("data/processed") / processed_filename
    processed_file = process_dataset(raw_file, processed_path)

    upload_to_s3(processed_file, bucket=PROCESSED_BUCKET)

    logger.success("🎯  Pipeline finished successfully!")

if __name__ == "__main__":
    app()