.PHONY: setup run test lint fmt migrate db

setup:      ## install deps and create .env
	uv sync
	test -f .env || cp .env.example .env

db:         ## start local Postgres
	docker compose up -d db

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

fmt:
	uv run ruff check --fix .
	uv run ruff format .
