import pandas as pd
from pathlib import Path
from loguru import logger

def process_dataset(input_path: Path, output_path: Path) -> Path:
    logger.info(f"🔧 Обработка данных: {input_path}")
    df = pd.read_csv(input_path)
    target = df["Survived"]
    feature_df = df.drop(columns=["Survived"])
    numeric = feature_df.select_dtypes(include="number")
    feature_df[numeric.columns] = (numeric - numeric.mean()) / numeric.std()
    feature_df["Survived"] = target
    output_path.parent.mkdir(parents=True, exist_ok=True)
    feature_df.to_csv(output_path, index=False)
    logger.success(f"💾 Обработанный файл сохранён: {output_path}")
    return output_path