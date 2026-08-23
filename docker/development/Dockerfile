FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.4.1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry.
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

# Install project dependencies.
RUN poetry install --no-root

COPY . .

# Enable the development entrypoint.
RUN chmod +x docker/development/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker/development/entrypoint.sh"]
