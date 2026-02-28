set shell := ["bash", "-c"]
uv_bin := if command -v uv >/dev/null 2>&1; then command -v uv; elif [ -x "$HOME/.openclaw/bin/uv" ]; then echo "$HOME/.openclaw/bin/uv"; else echo uv; fi

default:
    @just --list

# Initializes the project (uv-based)
setup:
    {{uv_bin}} venv
    {{uv_bin}} sync --extra dev
    cp -n .env.example .env || true

# Loads .env (if present) and prints bootstrap debug info when enabled
bootstrap-env:
    bash scripts/bootstrap.sh env

# Canonical startup path for local runs
bootstrap-run:
    bash scripts/bootstrap.sh run ${ARGS:-"--help"}

# Starts dev environment (fast prototyping)
dev:
    @just bootstrap-run

# Formats code (Ruff)
format:
    {{uv_bin}} run ruff format src tests scripts
    {{uv_bin}} run ruff check --fix src tests scripts

# Checks code quality (read-only)
lint:
    {{uv_bin}} run ruff check src tests scripts
    {{uv_bin}} run ruff format --check src tests scripts

# Type-checking
typecheck:
    {{uv_bin}} run mypy src

# Runs tests
test:
    PYTHONPATH=src {{uv_bin}} run pytest

# Builds distribution packages
build:
    {{uv_bin}} run --with build python -m build
    {{uv_bin}} run --with twine twine check dist/*

# Full quality check (CI simulation)
check: lint typecheck test

# Full local CI (lint, typecheck, tests, build)
ci: lint typecheck test build

# === WEB INTERFACE COMMANDS ===

# Setup web environment (installs Django dependencies)
setup-web:
    {{uv_bin}} sync --extra dev --extra web
    cp -n .env.example .env || true
    @echo "Web environment ready. Run 'just web-migrate' to initialize database."

# Run Django migrations
web-migrate:
    {{uv_bin}} run python src/manage.py migrate

# Create superuser for web interface
web-createsuperuser:
    {{uv_bin}} run python src/manage.py createsuperuser

# Start web development server
web-dev:
    {{uv_bin}} run python src/manage.py runserver 0.0.0.0:8000 --noreload

# Start web server via entrypoint (alternative)
web-start:
    {{uv_bin}} run musiclist-for-soundiiz-web

# Collect static files for production
web-collectstatic:
    {{uv_bin}} run python src/manage.py collectstatic --noinput

# Run web tests
web-test:
    PYTHONPATH=src {{uv_bin}} run pytest tests/ -v

# Run web tests with coverage
web-test-cov:
    PYTHONPATH=src {{uv_bin}} run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Full web setup (setup + migrate + test)
web-setup: setup-web web-migrate

# Start production server
web-production:
    {{uv_bin}} run musiclist-for-soundiiz-web --production --port 8080

# === DOCKER COMMANDS ===

# Starts Docker container (deployment test)
docker-up:
    docker compose up -d --build
    docker compose logs -f

# Stops Docker container
docker-down:
    docker compose down

# Start web with Docker (includes PostgreSQL)
docker-web-up:
    docker compose -f docker-compose.yml up -d --build
    @echo "Web interface starting..."
    @sleep 5
    docker compose logs -f web

# === UTILITY COMMANDS ===

# Show all available commands
help:
    @just --list
    @echo ""
    @echo "Quick start:"
    @echo "  1. just setup-web    # Install dependencies"
    @echo "  2. just web-migrate  # Setup database"
    @echo "  3. just web-dev      # Start development server"

# Cleans artifacts
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache .coverage htmlcov .ruff_cache
