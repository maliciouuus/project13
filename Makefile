.PHONY: clean lint test coverage docs run docker-build docker-up docker-down clean-all

# Variables
PYTHON = python3
COVERAGE_REPORT_DIR = htmlcov
DOCS_DIR = docs
DOCS_BUILD_DIR = $(DOCS_DIR)/_build

# Nettoyer les fichiers temporaires et les artefacts de build
clean:
	rm -rf $(COVERAGE_REPORT_DIR)
	rm -rf $(DOCS_BUILD_DIR)
	rm -rf .coverage
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Nettoyage complet pour préparation au push GitHub
clean-all: clean
	rm -f coverage.xml
	find . -name ".DS_Store" -delete
	rm -f Dockerfile.simple docker-compose.simple.yml
	rm -f SENTRY_SETUP.md projet13_rapport.txt
	rm -f run_server.sh setup_sentry.sh
	rm -f requirements-docker-updated.txt
	@echo "Nettoyage complet terminé! Projet prêt à être poussé vers GitHub."

# Exécuter le linter flake8
lint:
	flake8 .

# Exécuter les tests avec pytest
test:
	$(PYTHON) -m pytest

# Exécuter les tests avec couverture de code
coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=term-missing --cov-report=html

# Générer la documentation HTML
docs:
	cd $(DOCS_DIR) && make html

# Exécuter le serveur de développement Django
run:
	$(PYTHON) manage.py runserver

# Docker
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

# Commande combinée pour la vérification de qualité complète
quality-check: lint test coverage docs

# Aide
help:
	@echo "Les commandes disponibles sont :"
	@echo "  clean        - Nettoyer les fichiers temporaires"
	@echo "  clean-all    - Nettoyage complet pour préparation au push GitHub"
	@echo "  lint         - Exécuter flake8 pour vérifier le style de code"
	@echo "  test         - Exécuter les tests"
	@echo "  coverage     - Exécuter les tests avec rapport de couverture"
	@echo "  docs         - Générer la documentation HTML"
	@echo "  run          - Démarrer le serveur de développement Django"
	@echo "  docker-build - Construire les images Docker"
	@echo "  docker-up    - Démarrer les conteneurs Docker"
	@echo "  docker-down  - Arrêter les conteneurs Docker"
	@echo "  quality-check - Exécuter lint, test, coverage et docs"

# Commande par défaut
default: help 