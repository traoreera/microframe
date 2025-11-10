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
	uvicorn main:app --reload --host 0.0.0.0 --port 8000