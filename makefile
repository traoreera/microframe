


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
