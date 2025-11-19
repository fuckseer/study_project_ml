from pathlib import Path
import typer
from loguru import logger

from study_project_ml.pad_project_ml.s3_utils import download_from_s3, upload_to_s3
from study_project_ml.pad_project_ml.processing import process_dataset

app = typer.Typer(help="загрузка-обработка-загрузка")

@app.command()
def main(
    raw_filename: str = "titanic.csv",
    processed_filename: str = "titanic_processed.csv"
) -> None:
    logger.info("запуск пайплайна данных")
    raw_file = download_from_s3(raw_filename)

    processed_path = Path("data/processed") / processed_filename
    processed_file = process_dataset(raw_file, processed_path)

    upload_to_s3(processed_file, processed_filename)

    logger.success("пайплайн завершен успешно")

if __name__ == "__main__":
    app()