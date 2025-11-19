# pad_ml_project

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

for uni  homeworks


### 1️⃣ Установка окружения  
```bash
git clone https://github.com/fuckseer/study_project_ml.git
cd study_project_ml
uv venv --python 3.12
uv pip install -r requirements.txt
# или одной командой
bash setup_project.sh
```

### 2️⃣ Запуск MinIO (S3)
```bash
docker run -d \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=admin123 \
  quay.io/minio/minio server /data --console-address ":9001"
```
Создайте bucket **`study-project-data`** в консоли <http://localhost:9001>  
и поместите туда сырой датасет (например, `titanic.csv`).

Создайте файл `.env`:
```
AWS_ACCESS_KEY_ID=admin
AWS_SECRET_ACCESS_KEY=admin123
S3_ENDPOINT_URL=http://localhost:9000
RAW_BUCKET=study-project-data
PROCESSED_BUCKET=study-project-data
```

### 3️⃣ Запуск пайплайна
```bash
uv run python -m study_project_ml.pad_project_ml.pipeline_s3
```
Сценарий выполнит:
1. Загрузка `titanic.csv` → S3  
2. Скачивание обратно → `data/raw/`  
3. Обработка и сохранение в `data/processed/`  
4. Отправка обработанного файла обратно в S3  

Ожидаемые логи:
```
⬆️ Upload ... → s3://study-project-data/titanic.csv
🔧 Processing dataset ...
🎯 Pipeline finished successfully
```

### 4️⃣ Проверка линтеров
```bash
uv run flake8 study_project_ml
uv run mypy study_project_ml
```

✅ У вас должны пройти проверки и появиться в S3 оба файла: `titanic.csv` и `titanic_processed.csv`.

---


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

