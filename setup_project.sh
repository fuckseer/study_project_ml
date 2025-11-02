#!/usr/bin/env bash
# ============================================================
# Project setup script for study_project_ml
# ============================================================

set -e  # Exit immediately if any command fails

PYTHON_VERSION="3.12"
PROJECT_NAME="study_project_ml"

echo "============================"
echo "🚀 Setting up project: ${PROJECT_NAME}"
echo "============================"

# ------------------------------------------------------------
# 1. Create virtual environment with uv
# ------------------------------------------------------------
if [ ! -d ".venv" ]; then
  echo "🔧 Creating virtual environment (Python ${PYTHON_VERSION})..."
  uv venv --python ${PYTHON_VERSION}
else
  echo "✅ Virtual environment already exists, skipping creation."
fi

# ------------------------------------------------------------
# 2. Install dependencies
# ------------------------------------------------------------
echo "📦 Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

# ------------------------------------------------------------
# 3. Install dev tools (lint, type check, pre-commit)
# ------------------------------------------------------------
echo "🧰 Installing development tools..."
uv pip install flake8 mypy black isort pre-commit

# ------------------------------------------------------------
# 4. Set up pre-commit hooks
# ------------------------------------------------------------
echo "⚙️ Setting up pre-commit hooks..."
uv run pre-commit install

# ------------------------------------------------------------
# 5. Initial lint/type check test
# ------------------------------------------------------------
echo "🔍 Running initial lint and type check..."
uv run flake8 ${PROJECT_NAME} || true
uv run mypy ${PROJECT_NAME} || true

# ------------------------------------------------------------
# 6. Done
# ------------------------------------------------------------
echo "✅ Setup complete!"
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate     # (Linux/macOS)"
echo "  .\\.venv\\Scripts\\activate    # (Windows PowerShell)"
echo ""
echo "Run these commands for code checks:"
echo "  uv run flake8 ${PROJECT_NAME}"
echo "  uv run mypy ${PROJECT_NAME}"
echo ""
echo "Happy coding 💻"