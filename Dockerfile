# ==============================================================================
# @file         Dockerfile
# @description  Production-grade Python 3.11 image optimized for ASGI web 
#               applications managed via Poetry.
# @base-image   python:3.11-slim
# @maintainer   Development Team
# 
# @architectural-notes:
#   - Utilizes layer caching optimization by copying dependency manifests 
#     (pyproject.toml, poetry.lock) prior to the full source code.
#   - Disables Poetry virtual environments to install dependencies globally 
#     within the container runtime.
#
# @build-usage:
#   docker build -t <image-name>:<tag> .
#
# @run-usage:
#   docker run --rm -p 8000:8000 --env-file .env <image-name>:<tag>
# ==============================================================================

FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]