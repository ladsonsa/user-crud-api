# syntax=docker/dockerfile:1

# ============================================================
# Development
# ============================================================

FROM python:3.14-slim AS dev

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first to maximize Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install application and development dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --with dev --no-interaction --no-root

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ============================================================
# Production
# ============================================================

FROM python:3.14-slim AS prod

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first to maximize Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
