from pathlib import Path

from study_project_ml.pad_project_ml.s3_utils import upload_to_s3

RAW_DATA_DIR = Path("data/raw")

def upload_raw_dataset() -> None:
    file_path = RAW_DATA_DIR / "titanic.csv"
    upload_to_s3(file_path, "titanic.csv")
