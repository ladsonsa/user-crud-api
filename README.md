# User CRUD API

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python 3.14">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL 17">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

> Backend REST API for user management, built with FastAPI, SQLAlchemy and PostgreSQL, featuring layered architecture, Dependency Injection, automated testing, Docker and CI/CD.

## About the Project

**User CRUD API** is a backend portfolio project designed to demonstrate professional Python backend development practices through a complete user management API.

The project focuses on:

* REST API development with FastAPI
* Layered architecture and separation of concerns
* SOLID principles and Dependency Injection
* SQLAlchemy ORM with PostgreSQL persistence
* Unit and integration testing with pytest
* Automated code quality validation
* Containerized development with Docker
* Continuous Integration with GitHub Actions

The application implements the complete user CRUD lifecycle with request validation, controlled error handling and persistent database operations.

## Highlights

* Layered architecture with clearly separated responsibilities
* Dependency Injection and repository abstraction
* Unit and integration test suites with minimum 80% coverage
* Automated quality gates through GitHub Actions
* Dockerized FastAPI and PostgreSQL environment

## Tech Stack

| Category              | Technology              |
| --------------------- | ----------------------- |
| Language              | Python 3.14             |
| Framework             | FastAPI                 |
| ORM                   | SQLAlchemy              |
| Database              | PostgreSQL 17           |
| Dependency Management | Poetry 2.4.1            |
| Containerization      | Docker & Docker Compose |
| Testing               | pytest                  |
| Coverage              | pytest-cov              |
| Code Quality          | Ruff & Black            |
| CI                    | GitHub Actions          |

## API Endpoints

| Method   | Endpoint                  | Description              |
| -------- | ------------------------- | ------------------------ |
| `POST`   | `/api/v1/users`           | Create a user            |
| `GET`    | `/api/v1/users`           | List users               |
| `GET`    | `/api/v1/users/{user_id}` | Retrieve a specific user |
| `PUT`    | `/api/v1/users/{user_id}` | Update an existing user  |
| `DELETE` | `/api/v1/users/{user_id}` | Delete an existing user  |

## Architecture

The application follows a layered architecture designed to separate HTTP concerns, application logic and data persistence.

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Router / Route
  │
  ▼
Controller
  │
  ▼
DTO
  │
  ▼
Service
  │
  ▼
Workflow
  │
  ▼
Repository
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
  │
  ▼
Response
```

### Request Flow

```text
Request
  ↓
Router / Route
  ↓
Controller
  ↓
DTO
  ↓
Service
  ↓
Workflow
  ↓
Repository
  ↓
Database
  ↓
Response
```

The architecture applies **separation of concerns, Dependency Injection and SOLID principles**, keeping HTTP and persistence details separated from application processing.

## Project Structure

```text
app/
├── config/
├── controllers/
├── database/
├── dtos/
├── exceptions/
├── logs/
├── models/
├── repositories/
├── router/
│   └── routes/
├── services/
├── workflows/
└── main.py

tests/
├── integration/
│   ├── repositories/
│   └── routes/
└── unit/
    ├── config/
    ├── exceptions/
    └── workflows/

.github/
└── workflows/
    └── ci.yml

Dockerfile
docker-compose.yml
.env.example
.gitignore
LICENSE
README.md
pyproject.toml
poetry.lock
```

## Getting Started

### Prerequisites

* Docker
* Docker Compose
* Git

### 1. Clone the repository

```bash
git clone https://github.com/ladsonsa/user-crud-api.git
cd user-crud-api
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Review the values in `.env` before starting the application.

> Do not commit `.env` files or real credentials to the repository.

### 3. Start the application

```bash
docker compose up -d
```

### 4. Verify the services

```bash
docker compose ps
```

The API and PostgreSQL containers should be running.

To inspect API logs:

```bash
docker compose logs -f api
```

## API Documentation

After starting the application, access the interactive Swagger documentation at:

```text
http://localhost:8000/docs
```

Swagger UI can be used to validate the complete CRUD workflow:

* Create users
* List users
* Retrieve users
* Update users
* Delete users
* Validate request payloads
* Test expected error responses

## Database

PostgreSQL runs as a Docker Compose service and uses a persistent Docker volume.

The API connects to PostgreSQL through environment variables configured in `.env`.

For local database inspection, tools such as **DBeaver** can be used with:

```text
Host: localhost
Port: 5432
Database: <POSTGRES_DB>
Username: <POSTGRES_USER>
Password: <POSTGRES_PASSWORD>
```

The API container uses `postgres` as the database hostname because both services communicate through the Docker network.

## Testing

The project separates tests into **unit** and **integration** suites.

### Unit Tests

Unit tests validate application logic without requiring PostgreSQL.

```bash
docker compose run --rm --no-deps --build api poetry run pytest tests/unit -v
```

### Integration Tests

Integration tests validate the interaction between the API and PostgreSQL.

```bash
docker compose up -d
docker compose exec api poetry run pytest tests/integration -v
```

### Complete Test Suite

```bash
docker compose exec api poetry run pytest -v
```

### Coverage

```bash
docker compose exec api poetry run pytest \
  --cov=app \
  --cov-report=term-missing
```

The project requires a minimum test coverage of **80%** for critical modules.

The same threshold is enforced automatically by the CI pipeline.

## Continuous Integration

GitHub Actions automatically validates changes submitted to the repository.

The current CI workflow runs on:

* Pushes to `dev`
* Pull requests targeting `dev`

### CI Pipeline

```text
Checkout
   ↓
Python 3.14
   ↓
Poetry 2.4.1
   ↓
Install Dependencies
   ↓
Ruff
   ↓
Black
   ↓
pytest + Coverage
```

PostgreSQL 17 is provided as a service container so integration tests can run in the CI environment.

The pipeline fails when:

* Ruff detects code quality issues
* Black detects formatting differences
* Tests fail
* Test coverage falls below 80%

## Engineering Practices

The project follows the team's development standards, including:

* SOLID principles
* Dependency Injection
* Separation of concerns
* PEP 8
* Static typing
* Google Style docstrings
* Conventional Commits
* Automated testing
* Automated code quality checks
* Layered architecture

## Stopping the Application

Stop the containers:

```bash
docker compose down
```

This removes the application and PostgreSQL containers while preserving the database volume.

To remove the database volume as well:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` permanently removes the persisted PostgreSQL data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
