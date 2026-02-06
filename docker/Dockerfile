# MusicList for Soundiiz - Docker Image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=.venv
ENV PATH="/app/.venv/bin:/root/.local/bin:/root/.cargo/bin:${PATH}"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY docker/entrypoint.sh /app/entrypoint.sh

# Set up environment and install dependencies
RUN uv venv \
    && uv sync --frozen --no-dev

RUN chmod +x /app/entrypoint.sh

# Create mount points
VOLUME ["/music", "/output"]

ENV OUTPUT_DIR=/output

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--help"]
