import pandas as pd
from pathlib import Path
from loguru import logger

def process_dataset(input_path: Path, output_path: Path) -> Path:
    logger.info(f"Обработка данных {input_path}")
    df = pd.read_csv(input_path)
    numeric = df.select_dtypes(include="number")
    df[numeric.columns] = (numeric - numeric.mean()) / numeric.std()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Обработанный файл сохранен: {output_path}")
    return output_path