.PHONY:
.SILENT:

MIGRATION_NAME ?= "New migration"

run:
	uvicorn main:app --reload

makemigrations:
	alembic revision --autogenerate -m $(MIGRATION_NAME) - create migrations file

migrate:
	alembic upgrade head