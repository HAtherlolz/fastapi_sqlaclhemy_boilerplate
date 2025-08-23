.PHONY: install run makemigrations migrate shell add add-dev update export-reqs
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

export-reqs:
	poetry export -f requirements.txt --output requirements.txt --without-hashes