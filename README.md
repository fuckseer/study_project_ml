# pad_ml_project

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

for uni  homeworks
Шаблон проекта для ML‑домашек (DS‑cookiecutter + S3 + MLflow + Docker)

Проект содержит:
- локальный S3 (MinIO)
- MLflow трекинг + PostgreSQL
- пайплайн загрузки/обработки данных
- запуск ML‑экспериментов с логированием
- поддержку линтинга и mypy
- запуск экспериментов в контейнере

---

## 1️⃣ Установка окружения

Клонирование и создание окружения:

```bash
git clone https://github.com/fuckseer/study_project_ml.git
cd study_project_ml

uv venv --python 3.12
uv pip install -r requirements.txt
```

ИЛИ одной командой:

```bash
bash setup_project.sh
```

---

## 2️⃣ Запуск инфраструктуры (MinIO, PostgreSQL, MLflow, Training)

Используется `docker-compose`:

```bash
docker compose up -d --build
```

Проверить статус контейнеров:

```bash
docker compose ps
```

Должны подняться 4 сервиса:

- `minio` — локальный S3  
- `db` — PostgreSQL для MLflow  
- `mlflow` — MLflow Tracking Server  
- `training` — контейнер для запуска обучения  

---

## 3️⃣ Настройка MinIO (локальный S3)

Открой:

http://localhost:9001  
логин: **admin**  
пароль: **admin123**

Создай 2 bucket‑а:

```
study-project-data
mlflow-artifacts
```

Помести в `study-project-data` сырой датасет, например:

```
titanic.csv
```

---

## 4️⃣ Создание файла переменных окружения

Создай `.env` в корне проекта:

```
AWS_ACCESS_KEY_ID=admin
AWS_SECRET_ACCESS_KEY=admin123
S3_ENDPOINT_URL=http://minio:9000

RAW_BUCKET=study-project-data
PROCESSED_BUCKET=study-project-data

MLFLOW_TRACKING_URI=http://mlflow:5000
```

---

## 5️⃣ Запуск пайплайна обработки данных

Скрипт выполнит:

1. загрузку сырого датасета → S3  
2. скачивание в `data/raw/`  
3. обработку и сохранение в `data/processed/`  
4. загрузку обработанных данных обратно в S3  

Запуск:

```bash
docker compose exec training python -m study_project_ml.pad_project_ml.pipeline_s3
```

Ожидаемый лог:

```
⬇️  Download s3://study-project-data/titanic.csv
🔧 Processing dataset...
⬆️  Upload ... → s3://study-project-data/titanic_processed.csv
🎯 Pipeline finished successfully
```

---

## 6️⃣ Запуск ML‑экспериментов (MLflow + S3)

Сетка гиперпараметров описана в:

```
config/experiments.yml
```

Запуск всех экспериментов:

```bash
bash run_experiments.sh
```

Каждый эксперимент:

- скачивает обработанный датасет из S3  
- обучает LogisticRegression  
- логирует параметры + метрики в MLflow  
- сохраняет model.pkl и metrics.json  
  - в MLflow артефакты  
  - в MinIO по пути:

```
s3://study-project-data/<experiment_name>/model_*.pkl
s3://study-project-data/<experiment_name>/metrics_*.json
```

---

## 7️⃣ Просмотр экспериментов в MLflow

Открой интерфейс:

```
http://localhost:5001
```

Здесь отображаются:
- эксперименты  
- параметры  
- метрики (accuracy, roc_auc)  
- артефакты (модели, метрики)  

---

## 8️⃣ Проверка стиля кода

Перед коммитами работает `pre-commit`, но можно запустить вручную:

```bash
uv run flake8 study_project_ml
uv run mypy study_project_ml
```

---

## 9️⃣ Полезные команды Docker

Остановить всю инфраструктуру:

```bash
docker compose down
```

Очистить с томами:

```bash
docker compose down -v
```

Пересобрать проект:

```bash
docker compose build training
```

Посмотреть логи MLflow:

```bash
docker compose logs -f mlflow
```

Посмотреть содержимое MinIO через CLI:

```bash
docker compose exec mlflow aws --endpoint-url http://minio:9000 s3 ls
```


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         pad_ml_project and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── pad_ml_project   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes pad_ml_project a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

