.PHONY: venv dev test lint format typecheck docker docker-down clean coverage

venv:
	uv sync

dev: venv
	uv run flask --app "flask_apache:create_app" run --port 3100

test:
	uv run pytest

coverage:
	uv run pytest --cov-report=html

lint:
	uv run ruff check .

format:
	uv run isort . && uv run black .

typecheck:
	uv run mypy

docker:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage dist
