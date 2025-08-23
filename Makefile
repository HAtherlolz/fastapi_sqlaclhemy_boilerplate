.PHONY: install run makemigrations migrate shell add add-dev update export-reqs check black-check isort-check mypy-check black-format format isort-format init-project build up down lock
.SILENT:

MIGRATION_NAME ?= "New migration"

install:
	poetry install

run:
	poetry run uvicorn main:app --reload

makemigrations:
	poetry run alembic revision --autogenerate -m $(MIGRATION_NAME)

migrate:
	poetry run alembic upgrade head

shell:
	poetry shell

add:
	poetry add $(PACKAGE)

add-dev:
	poetry add --group dev $(PACKAGE)

update:
	poetry update

lock:
	poetry lock --no-update

export-reqs:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Code formatting and linting
check:
	poetry run black app tests --check
	poetry run isort app tests --check-only --diff
	poetry run mypy --show-error-codes app tests

black-check:
	poetry run black app tests --check

isort-check:
	poetry run isort app tests --check-only --diff

mypy-check:
	poetry run mypy --show-error-codes app tests

black-format:
	poetry run black app tests

isort-format:
	poetry run isort app tests

format:
	poetry run black app tests
	poetry run isort app tests


# Docker
init-project:
	docker-compose up --build

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

