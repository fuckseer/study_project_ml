import os
import tempfile

import joblib
import typer
import mlflow
import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from pathlib import Path

from study_project_ml.pad_project_ml.s3_utils import download_from_s3

app = typer.Typer()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

@app.command()
def train(
    experiment_name: str = typer.Option("Titanic_Classification", help="Name of the MLflow experiment."),
    dataset_name: str = typer.Option("titanic_processed.csv", help="Name of the processed dataset in S3."),
    c_param: float = typer.Option(1.0, help="Inverse of regularization strength for Logistic Regression."),
    penalty: str = typer.Option("l2", help="Penalty norm for Logistic Regression ('l1', 'l2', 'elasticnet', 'none')."),
    solver: str = typer.Option("lbfgs", help="Algorithm to use in the optimization problem.")
) -> None:
    """Обучает модель, логирует метрики и артефакты в MLflow."""
    logger.info("🚀 Запуск эксперимента по обучению модели...")
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        mlflow.log_param("C", c_param)
        mlflow.log_param("penalty", penalty)
        mlflow.log_param("solver", solver)
        logger.info(f"Гиперпараметры: C={c_param}, penalty={penalty}, solver={solver}")

        logger.info(f"Загрузка данных: {dataset_name} из S3...")
        local_path = download_from_s3(dataset_name, target_dir=Path("data/processed"))
        df = pd.read_csv(local_path)

        df = df.select_dtypes(include='number').dropna()
        X = df.drop("Survived", axis=1)
        y = df["Survived"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        logger.info("Обучение модели LogisticRegression...")
        model = LogisticRegression(C=c_param, penalty=penalty, solver=solver, max_iter=200)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("roc_auc", roc_auc)
        logger.info(f"Метрики: Accuracy={accuracy:.4f}, ROC-AUC={roc_auc:.4f}")

        logger.info("Сохранение модели в MLflow...")
        logger.info("Сохраняем модель вручную, без Model Registry...")

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.pkl"
            joblib.dump(model, model_path)
            mlflow.log_artifact(str(model_path), artifact_path="model")

        logger.success("Модель сохранена в MLflow как артефакт!")

    logger.success("✅ Эксперимент завершен успешно!")

if __name__ == "__main__":
    app()