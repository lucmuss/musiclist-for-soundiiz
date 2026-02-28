# Python 3.11 base
FROM python:3.11-slim

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:/root/.local/bin:$PATH"

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files first for better caching
WORKDIR /app
COPY pyproject.toml uv.lock /app/ 2>/dev/null || true

# Install dependencies
RUN uv venv /app/.venv && \
    uv pip install --system django django-environ psycopg2-binary dj-database-url \
    django-htmx gunicorn whitenoise mutagen python-dotenv Pillow celery redis

# Copy the application
COPY . /app

# Install the local project
RUN uv pip install -e /app || true

# Working directory to Django app
WORKDIR /app/src

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create media directory
RUN mkdir -p /app/src/media

# Expose port
EXPOSE 8083

# Entrypoint script
COPY docker/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8083} --workers 4 --timeout 120 musiclist_project.wsgi:application"]
