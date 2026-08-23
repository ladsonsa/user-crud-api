# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.4.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install \
    --only main \
    --no-root \
    --no-interaction

COPY app ./app
COPY docker/production ./docker/production


FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
COPY --from=builder /app/docker/production /app/docker/production

RUN chmod +x /app/docker/production/entrypoint.sh \
    && chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker/production/entrypoint.sh"]