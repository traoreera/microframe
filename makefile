# Makefile
.PHONY: help install dev test lint format clean run

help:
	@echo "Commandes disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make dev        - Installer les dépendances de développement"
	@echo "  make test       - Lancer les tests"
	@echo "  make lint       - Vérifier le code (flake8, mypy)"
	@echo "  make format     - Formater le code (black)"
	@echo "  make clean      - Nettoyer les fichiers générés"
	@echo "  make run        - Lancer l'application"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=microframework --cov-report=html

lint:
	flake8 microframework tests
	mypy microframework

format:
	black microframework tests examples

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist .pytest_cache .coverage htmlcov

run:
	poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000


lint-fix: ## Correction automatique des erreurs de linting (SAFE - préserve imports)
	@echo "🔧 Correction automatique du code (mode SAFE)..."
	@echo "📋 1. Correction autopep8 (lignes longues, espaces)..."
	@poetry run autopep8 --in-place --recursive --exclude=alembic,static,__pycache__ .
	@echo "📋 2. Tri des imports avec isort..."
	@poetry run isort . --skip=alembic --skip=static --skip=__pycache__
	@echo "📋 3. Formatage avec black..."
	@poetry run black . --exclude="(alembic|static|__pycache__)"
	@echo "📋 4. Suppression CONSERVATIVE des variables inutiles (préserve imports)..."
	@poetry run autoflake --in-place --recursive --remove-unused-variables --ignore-init-module-imports --exclude=alembic,static,__pycache__ .
	@echo "✅ Correction automatique terminée (imports préservés)!"
