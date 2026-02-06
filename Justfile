set shell := ["bash", "-c"]

default:
    @just --list

# Initializes the project (uv-based)
setup:
    uv venv
    uv sync --extra dev
    cp -n .env.example .env || true

# Starts dev environment (fast prototyping)
dev:
    bash docker/entrypoint.sh

# Formats code (Black + Ruff)
format:
    uv run --with black black src tests scripts
    uv run ruff check --fix src tests scripts

# Checks code quality (read-only)
lint:
    uv run ruff check src tests scripts
    uv run --with black black --check src tests scripts
    uv run --with flake8 flake8 src tests scripts

# Type-checking
typecheck:
    uv run mypy src

# Runs tests
test:
    PYTHONPATH=src uv run pytest

# Builds distribution packages
build:
    uv run --with build python -m build
    uv run --with twine twine check dist/*

# Full quality check (CI simulation)
check: lint typecheck test

# Full local CI (lint, typecheck, tests, build)
ci: lint typecheck test build

# Starts Docker container (deployment test)
docker-up:
    docker compose up -d --build
    docker compose logs -f

# Stops Docker container
docker-down:
    docker compose down

# Cleans artifacts
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache .coverage htmlcov .ruff_cache
