.PHONY: help build up down restart logs shell composer console cache-clear

# Variables
DOCKER_COMPOSE = docker compose
EXEC_PHP = $(DOCKER_COMPOSE) exec php

## —— Docker ——
help: ## Affiche cette aide
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-20s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

build: ## Build les images Docker
	$(DOCKER_COMPOSE) build --no-cache

up: ## Démarre les conteneurs en arrière-plan
	$(DOCKER_COMPOSE) up -d

down: ## Arrête et supprime les conteneurs
	$(DOCKER_COMPOSE) down

restart: down up ## Redémarre les conteneurs

logs: ## Affiche les logs des conteneurs
	$(DOCKER_COMPOSE) logs -f

logs-php: ## Affiche les logs PHP uniquement
	$(DOCKER_COMPOSE) logs -f php

logs-nginx: ## Affiche les logs Nginx uniquement
	$(DOCKER_COMPOSE) logs -f nginx

## —— PHP / Symfony ——
shell: ## Ouvre un shell dans le conteneur PHP
	$(EXEC_PHP) sh

composer: ## Exécute Composer (ex: make composer c="install")
	$(EXEC_PHP) composer $(c)

console: ## Exécute une commande Symfony console (ex: make console c="cache:clear")
	$(EXEC_PHP) php bin/console $(c)

cache-clear: ## Vide le cache Symfony
	$(EXEC_PHP) php bin/console cache:clear

## —— Installation ——
install: up ## Installation complète du projet
	$(EXEC_PHP) composer install
	@echo "\033[32m✓ Installation terminée !\033[0m"
	@echo "\033[33m→ Accédez à l'application : http://localhost:$${APP_PORT:-8080}\033[0m"

## —— Debug ——
ps: ## Liste les conteneurs en cours d'exécution
	$(DOCKER_COMPOSE) ps

health: ## Affiche le statut de santé des conteneurs
	docker ps --format "table {{.Names}}\t{{.Status}}"

php-version: ## Affiche la version de PHP
	$(EXEC_PHP) php -v

php-modules: ## Liste les modules PHP installés
	$(EXEC_PHP) php -m
