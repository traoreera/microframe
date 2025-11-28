


# ============================================================
# 📚 Commande HELP - Affiche toutes les commandes disponibles
# ============================================================
help: ## Afficher la liste des commandes disponibles et leur usage
	@echo "📚 Liste des commandes disponibles :"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean: ## Supprimer __pycache__ et fichiers *.pyc, *.pyo
	@echo "🧹 Nettoyage des fichiers inutiles..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f \( -name "*.backup" -o -name "*.backup" \) -exec rm -f {} +
	@find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} +

# ============================================================
# 📦 Installation & initialisation projet
# ============================================================

install: ## Installer les dépendances Python via Poetry
	@poetry lock
	@poetry install

# ============================================================
# 🚀 Lancement de l'application
# ============================================================

run-dev: ## Lancer en mode développement (reload automatique)
	@echo "🚀 Lancement en mode développement..."
	@poetry run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-st: ## Lancer en mode production / statique (sans reload)
	@echo "🚀 Lancement en mode statique..."
	@poetry run python -m uvicorn main:app --host 0.0.0.0 --port 8000



# ============================================================
# 🏗️  Build & Correction automatique du code
# ============================================================

build: ## Build complet du projet (clean + install + lint-fix + format)
	@echo "🏗️  CONSTRUCTION DU PROJET"
	@echo "==========================="
	@echo ""
	@echo "🧹 1. Nettoyage des fichiers compilés..."
	@$(MAKE) clean
	@echo ""
	@echo "📦 2. Installation des dépendances..."
	@$(MAKE) install
	@echo ""
	@echo "🔧 3. Correction automatique du code..."
	@$(MAKE) lint-fix
	@echo ""
	@echo "✅ Build terminé avec succès!"

build-prod: ## Build pour production (build + tests + validation)
	@echo "🚀 BUILD PRODUCTION"
	@echo "=================="
	@echo ""
	@$(MAKE) build
	@echo ""
	@echo "🧪 5. Exécution des tests..."
	@$(MAKE) test
	@echo ""
	@echo "🔒 6. Validation sécurité..."
	@$(MAKE) security-check
	@echo ""
	@poetry build --no-cache
	@echo "🎉 Build production prêt!"
	

build-fast: ## Build rapide (clean + install uniquement)
	@echo "⚡ BUILD RAPIDE"
	@echo "=============="
	@$(MAKE) clean
	@$(MAKE) install
	@poetry build
	@echo "✅ Build rapide terminé!"

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

test: ## Exécution des tests
	@echo "🧪 Exécution des tests..."
	@poetry run pytest  --cov --cov-branch --cov=src --cov-report=xml --verbose; 


security-check: ## Vérification de sécurité basique
	@echo "🔒 Vérification de sécurité..."
	@echo "✅ Vérification .env (ne pas commiter)"
	@if git ls-files | grep -q "\.env$$"; then \
		echo "❌ ATTENTION: .env est tracké par git!"; \
	else \
		echo "✅ .env correctement ignoré"; \
	fi
	@echo "✅ Vérification des mots de passe hardcodés..."
	@if grep -r "password\s*=\s*[\"'][^\"']*[\"']" . --exclude-dir=.git --exclude-dir=static --exclude-dir=__pycache__ 2>/dev/null; then \
		echo "❌ ATTENTION: Mots de passe potentiels trouvés!"; \
	else \
		echo "✅ Aucun mot de passe hardcodé détecté"; \
	fi