#################################################################################
# GLOBALS                                                                       #
#################################################################################
PROJECT_NAME = study_project_ml
PYTHON_VERSION = 3.12
#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
.PHONY: requirements
requirements:
    uv pip install -r requirements.txt

## Delete all compiled Python files
.PHONY: clean
clean:
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete

## Lint using flake8, black, and isort (use `make format` to auto-format)
.PHONY: lint
lint:
    flake8 $(PROJECT_NAME)
    isort --check --diff $(PROJECT_NAME)
    black --check $(PROJECT_NAME)

## Format source code with black and isort
.PHONY: format
format:
    isort $(PROJECT_NAME)
    black $(PROJECT_NAME)

## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
    aws s3 sync s3://bucket-name/data/ data/

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
    aws s3 sync data/ s3://bucket-name/data/

## Set up Python interpreter environment using uv
.PHONY: create_environment
create_environment:
    uv venv --python $(PYTHON_VERSION)
    @echo ">>> New uv virtual environment created. Activate with:"
    @echo ">>> Windows: .\\.venv\\Scripts\\activate"
    @echo ">>> Linux/macOS: source .venv/bin/activate"
    @echo ">>> Then install requirements via: make requirements"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make dataset
.PHONY: data
data: requirements
    uv run python $(PROJECT_NAME)/dataset.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.DEFAULT_GOAL := help
define PRINT_HELP_PYSCRIPT
import re, sys
lines = "\n".join([line for line in sys.stdin])
matches = re.findall(r'## (.+)\n([a-zA-Z0-9._-]+):', lines)
print("Available rules:\n")
print("\n".join([f"{name:25} {desc}" for desc, name in matches]))
endef
export PRINT_HELP_PYSCRIPT
help:
    @uv run python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)