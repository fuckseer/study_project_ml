import json
import os
import tempfile
from pathlib import Path

import joblib
import mlflow
import pandas as pd
import typer
from loguru import logger
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from study_project_ml.pad_project_ml.s3_utils import download_from_s3, upload_to_s3

app = typer.Typer()

MLFLOW_TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

RAW_BUCKET = os.getenv("RAW_BUCKET", "mlflow-artifacts")
PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", RAW_BUCKET)


@app.command()
def train(
    experiment_name: str = typer.Option("Titanic_Classification", help="MLflow experiment name"),
    dataset_name: str = typer.Option("titanic_processed.csv", help="Processed dataset in S3"),
    c_param: float = typer.Option(1.0, help="C parameter for LogisticRegression"),
    penalty: str = typer.Option("l2", help="Penalty type for LogisticRegression"),
    solver: str = typer.Option("lbfgs", help="Solver for LogisticRegression")
) -> None:

    logger.info("🚀 Starting ML experiment")
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        mlflow.log_param("C", c_param)
        mlflow.log_param("penalty", penalty)
        mlflow.log_param("solver", solver)

        logger.info(f"Downloading dataset from S3: {dataset_name}")
        local_path = download_from_s3(
            key=dataset_name,
            bucket=PROCESSED_BUCKET,
            target_dir=Path("data/processed")
        )

        df = pd.read_csv(local_path)
        df = df.select_dtypes(include="number").dropna()

        X = df.drop("Survived", axis=1)
        y = df["Survived"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        logger.info("Training Logistic Regression model...")
        model = LogisticRegression(
            C=c_param,
            penalty=penalty,
            solver=solver,
            max_iter=200
        )
        model.fit(X_train, y_train)

        #
        # Metrics
        #
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("roc_auc", roc_auc)

        logger.info(f"Metrics: accuracy={accuracy:.4f}, roc_auc={roc_auc:.4f}")

        #
        # Save model + metrics JSON locally and upload both to MLflow & S3
        #
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Local temporary files
            model_path = tmpdir_path / "model.pkl"
            metrics_path = tmpdir_path / "metrics.json"

            joblib.dump(model, model_path)
            with metrics_path.open("w") as f:
                json.dump({"accuracy": accuracy, "roc_auc": roc_auc}, f)

            mlflow.log_artifact(str(model_path), artifact_path="model")
            mlflow.log_artifact(str(metrics_path), artifact_path="metrics")

            logger.info("Model & metrics saved to MLflow artifacts")

            s3_model_key = (
                f"{experiment_name}/"
                f"model_C={c_param}_penalty={penalty}_solver={solver}.pkl"
            )
            s3_metrics_key = (
                f"{experiment_name}/"
                f"metrics_C={c_param}_penalty={penalty}_solver={solver}.json"
            )

            upload_to_s3(model_path, bucket=PROCESSED_BUCKET, key=s3_model_key)
            upload_to_s3(metrics_path, bucket=PROCESSED_BUCKET, key=s3_metrics_key)

            logger.success(
                f"Uploaded model & metrics to S3 folder '{experiment_name}'"
            )

    logger.success("✅ Experiment finished successfully!")


if __name__ == "__main__":
    app()