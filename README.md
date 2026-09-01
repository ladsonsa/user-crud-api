# User CRUD API

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

> A REST API built with FastAPI, SQLAlchemy, PostgreSQL, and Docker, following a layered architecture and professional backend development practices.

## Highlights

* Layered Architecture (Controller → Service → Workflow → Repository)
* Dependency Injection
* SQLAlchemy ORM with PostgreSQL
* Dockerized Development Environment
* Unit and Integration Testing
* Interactive Swagger Documentation

## Tech Stack

| Category         | Technology              |
| ---------------- | ----------------------- |
| Language         | Python 3.14             |
| Framework        | FastAPI                 |
| ORM              | SQLAlchemy              |
| Database         | PostgreSQL              |
| Containerization | Docker & Docker Compose |
| Testing          | pytest                  |

## Overview

This project demonstrates a production-oriented backend architecture using FastAPI, SQLAlchemy, PostgreSQL, and Docker, with a strong focus on separation of concerns, dependency injection, and automated testing.

The application follows a layered architecture where business logic remains isolated from both HTTP and database implementation details.

## Architecture

```text
Client
  │
  ▼
FastAPI
  ▼
Controller
  ▼
Service
  ▼
Workflow
  ▼
Repository
  ▼
SQLAlchemy
  ▼
PostgreSQL
```

The project follows SOLID principles, Dependency Injection, and a modular architecture to keep each layer focused on a single responsibility.

## Project Structure

```text
app/
├── config/
├── controllers/
├── database/
├── dtos/
├── exceptions/
├── models/
├── repositories/
├── router/
├── services/
├── workflows/
└── main.py

tests/
├── integration/
└── unit/
```

## Getting Started

### Prerequisites

* Docker
* Docker Compose
* Git

### Installation

Clone the repository and create the environment file:

```bash
git clone https://github.com/ladsonsa/user-crud-api.git
cd user-crud-api
cp .env.example .env
```

Start the application:

```bash
docker compose up -d
```

Verify the running services:

```bash
docker compose ps
```

## Environment Variables

The application configuration is provided through environment variables.

Create a `.env` file based on `.env.example`:

```text
APP_NAME=user-crud-api
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

| Variable            | Description                                   |
| ------------------- | --------------------------------------------- |
| `APP_NAME`          | Application name                              |
| `APP_ENV`           | Application environment                       |
| `APP_HOST`          | Host used by the application server           |
| `APP_PORT`          | Port used by the application server           |
| `POSTGRES_DB`       | PostgreSQL database name                      |
| `POSTGRES_USER`     | PostgreSQL username                           |
| `POSTGRES_PASSWORD` | PostgreSQL password                           |
| `POSTGRES_HOST`     | PostgreSQL hostname used by the API container |
| `POSTGRES_PORT`     | PostgreSQL port                               |

Do not commit `.env` files or real database credentials to the repository.

## API Documentation

After starting the application, Swagger UI is available at:

```text
http://localhost:8000/docs
```

Swagger can be used to manually test all CRUD endpoints, including successful operations, validation errors, duplicated emails, nonexistent users, and invalid payloads.

## Database

PostgreSQL runs as a separate Docker Compose service and persists data through a Docker volume.

The API connects to PostgreSQL using the environment variables defined in `.env`.

### DBeaver

DBeaver can be used to connect directly to the PostgreSQL database and verify the state produced by API operations.

With the Docker Compose environment running, create a PostgreSQL connection using the values from `.env`.

For DBeaver running on the host machine, use:

| Setting  | Value                        |
| -------- | ---------------------------- |
| Host     | `localhost`                  |
| Port     | `5432`                       |
| Database | Value of `POSTGRES_DB`       |
| Username | Value of `POSTGRES_USER`     |
| Password | Value of `POSTGRES_PASSWORD` |

After connecting, navigate to:

```text
Schemas
└── public
    └── Tables
        └── users
```

The `users` table can be used to verify:

* Users created through the API
* User updates
* Deleted users
* Current database state

> The hostname `postgres` is used by the API container to communicate with the PostgreSQL container through the Docker network. DBeaver running on the host should use `localhost`.

## Testing

The project separates unit and integration tests according to their dependencies.

### Unit Tests

Unit tests validate application logic without requiring PostgreSQL.

Run them using the API container without starting the database:

```bash
docker compose run --rm --no-deps --build api poetry run pytest tests/unit -v
```

### Integration Tests

Integration tests validate the API and database integration and require the Docker Compose environment and PostgreSQL.

Start the environment:

```bash
docker compose up -d
```

Run the integration tests:

```bash
docker compose exec api poetry run pytest tests/integration -v
```

### All Tests

Start the Docker Compose environment:

```bash
docker compose up -d
```

Run the complete test suite:

```bash
docker compose exec api poetry run pytest -v
```

### Test Coverage

Generate the coverage report with:

```bash
docker compose exec api poetry run pytest \
  --cov=app \
  --cov-report=term-missing
```

The project requires a minimum coverage of 80%.

Current measured coverage:

```text
95%
```

The configured `fail_under` threshold ensures the test suite fails if coverage falls below 80%.

## Stop the Application

Stop the Docker Compose services with:

```bash
docker compose down
```

This stops and removes the application and PostgreSQL containers while preserving the PostgreSQL volume.

To also remove the PostgreSQL volume:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` removes the PostgreSQL volume and permanently deletes the persisted database data.

## Development Standards

The project follows established backend engineering practices, including:

* SOLID principles
* PEP8 compliance
* Static typing
* Google Style docstrings
* Conventional Commits
* Modular architecture

## Next Improvements

* GitHub Actions (CI)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
