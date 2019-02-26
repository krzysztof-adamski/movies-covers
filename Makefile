SHELL := /bin/bash
PWD := $(shell pwd)
PROJECT_NAME := movies
PROJECT_LOCAL_PORT := 8080
WORKON_HOME := env
APP_PATH := $(PWD)
ENV_PATH := $(APP_PATH)/$(WORKON_HOME)

DB_USER := $(shell echo ${DB_USER})
DB_PASSWORD := $(shell echo ${DB_PASSWORD})
DB_NAME := ${PROJECT_NAME}

RED := \u001b[0;31m
NC := \u001b[0m
GREEN := \u001b[0;32m
YELLOW := \u001b[1;33m

.PHONY: docs
export PATH := $(PATH):$(WORKON_HOME)/bin
export PYTHONPATH := $(WORKON_HOME)/bin
export ENV_PATH := $(APP_PATH)/$(WORKON_HOME)
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@-python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

test: ## uruchamia testy w środowisku wirtualnym
	@-mkdir -p .reports
	@-source ${ENV_PATH}/bin/activate && coverage run ./manage.py test ${PROJECT_NAME} #  -p="test_*.py"

report:  ## generuje raport pokrycia kodu testami
	@-coverage xml -o .reports/coverage.xml
	@-coverage report -m
	@-coverage html

codestyle: ## przeprowadza analizę statyczną kodu
	@-flake8 .

docstyle:  ## sprawdza jakość dokumentacji
	pydocstyle --ignore=D205,D211,D212,D400 .  2>/dev/null || true

start:  ## uruchamia serwer lokalny
	echo -e "${YELLOW}Uruchamiam lokalny serwer${NC}"
	python manage.py runserver

collectstatic:  ## Wgrywanie statykow
	@-python manage.py collectstatic --noinput 2>/dev/null || true

clearcache:  ## czysci cache
	@-find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
	@-find . -name "*.pyc" -exec rm -rf {} \; 2>/dev/null || true
	@-find . -name ".pytest_cache" -exec rm -rf {} \; 2>/dev/null || true

migrations:  ## migracje
	python manage.py makemigrations 2>/dev/null
	python manage.py migrate 2>/dev/null
	python manage.py makemigrations 2>/dev/null

rm-migrations-sqlite:  ## usuwa migracje sqlite
	@-rm *.sqlite3
	@-rm ./movies/migrations/0*

rm-migrations-mysql:  ## usuwa migracje mysql
	@-echo -e "${YELLOW}Usuwa migracje mysql i czysci baze jeśli jest${NC}"
	@-rm ./movie/migrations/0* 2>/dev/null || true
	@-echo -e "${RED}Potwierdzasz czyszczenie bazy <yes> <no> ?${NC}"
	@-python manage.py reset_db || true

create-dbuser:  ## tworzy uzytkownika bazy
	@-echo -e "${YELLOW}Nowy użytkownik bazy${NC}"
	@-echo -e "User: ${GREEN}${DB_USER}${NC}"
	@-echo -e "Database: ${GREEN}${DB_NAME}${NC}"
	@-echo -e "Password: ${GREEN}${DB_PASSWORD}${NC}"
	@-echo "Zatwierdź hasłem superuser mysql"
	@-echo "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';GRANT ALL PRIVILEGES ON * . * TO '${DB_USER}'@'localhost';FLUSH PRIVILEGES;" | mysql -u root -p

create-dbase:  ## tworzy baze z userem z env
	@-echo -e "${YELLOW}Nowa baza${NC}"
	@-echo -e "Database: ${GREEN}${DB_NAME}${NC}"
	@-echo "Zatwierdź hasłem superuser mysql"
	@-echo "CREATE DATABASE IF NOT EXISTS ${DB_NAME};" | mysql -u root -p

develop:  ## tworzy lokalnie środowisko virtualne
	@-rm -rf ${WORKON_HOME}
	@-virtualenv --python=python3 ${WORKON_HOME}  #  virtualenv --python=python3 .venv
	@-source ${ENV_PATH}/bin/activate
	@-${ENV_PATH}/bin/pip install -r requirements.txt
