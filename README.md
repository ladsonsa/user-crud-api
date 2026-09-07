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

> Layered REST API for user management, built with FastAPI, SQLAlchemy and PostgreSQL, featuring Dependency Injection, JWT authentication, ownership-based authorization, automated testing, Docker and CI.

## About the Project

**User CRUD API** is a backend portfolio project designed to demonstrate professional Python backend development practices through a complete user management API.

The project focuses on:

* REST API development with FastAPI
* Layered architecture and separation of concerns
* SOLID principles and Dependency Injection
* SQLAlchemy ORM with PostgreSQL persistence
* JWT-based authentication
* Ownership-based authorization
* Unit and integration testing with pytest
* Automated code quality validation
* Containerized development with Docker
* Continuous Integration with GitHub Actions

The application implements the complete user CRUD lifecycle with request validation, authentication, authorization, controlled error handling and persistent database operations.

## Highlights

* Layered architecture with clearly separated responsibilities
* Dependency Injection and repository abstraction
* JWT authentication with Bearer tokens
* Secure password hashing using Argon2 through `pwdlib`
* Ownership validation for individual user operations
* Unit and integration test suites with an enforced 80% coverage threshold
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
| Authentication        | JWT / PyJWT             |
| Password Hashing      | pwdlib / Argon2         |
| Containerization      | Docker & Docker Compose |
| Testing               | pytest                  |
| Coverage              | pytest-cov              |
| Code Quality          | Ruff & Black            |
| CI                    | GitHub Actions          |

## API Endpoints

| Method   | Endpoint                  | Authentication           | Description                                    |
| -------- | ------------------------- | ------------------------ | ---------------------------------------------- |
| `POST`   | `/api/v1/auth/login`      | Public                   | Authenticate user and issue a JWT access token |
| `POST`   | `/api/v1/users`           | Public                   | Create a user                                  |
| `GET`    | `/api/v1/users`           | Bearer token             | List users                                     |
| `GET`    | `/api/v1/users/{user_id}` | Bearer token + ownership | Retrieve a specific user                       |
| `PUT`    | `/api/v1/users/{user_id}` | Bearer token + ownership | Update an existing user                        |
| `DELETE` | `/api/v1/users/{user_id}` | Bearer token + ownership | Delete an existing user                        |

### Authentication Flow

```text
Register User
     ↓
POST /api/v1/users
     ↓
User created with hashed password
     ↓
POST /api/v1/auth/login
     ↓
Credentials validated
     ↓
JWT access token issued
     ↓
Authorization: Bearer <token>
     ↓
Protected endpoints
```

The user password is never returned by the API. Passwords are stored as secure hashes, while authenticated requests use JWT Bearer tokens.

## Authorization

Protected endpoints require a valid JWT access token.

Operations targeting a specific user also validate ownership:

```text
Authenticated User
       ↓
JWT validation
       ↓
Current user resolved
       ↓
Ownership validation
       ↓
Requested user resource
```

A user can only perform individual resource operations when the authenticated user's identifier matches the requested `user_id`.

## Architecture

The application follows a layered architecture designed to separate HTTP concerns, application logic and data persistence.

```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication
  │       │
  │       ▼
  │    JWT Validation
  │       │
  │       ▼
  │    Authorization
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
Authentication
  ↓
Authorization
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
├── security/
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

Authentication requires the following environment variables:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES
```

Use a strong secret key with at least 32 characters for `JWT_SECRET_KEY`.

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

Swagger UI can be used to validate the complete API workflow:

* Create users
* Authenticate users
* Authorize requests with a Bearer token
* List users
* Retrieve users
* Update users
* Delete users
* Validate request payloads
* Test expected error responses

### Authentication in Swagger

1. Create a user through `POST /api/v1/users`.
2. Authenticate through `POST /api/v1/auth/login`.
3. Copy the returned `access_token`.
4. Select **Authorize** in Swagger UI.
5. Provide the Bearer token.
6. Execute the protected endpoints.

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
  --cov-report=term-missing \
  --cov-fail-under=80
```

The project requires a minimum test coverage of **80%**.

The same threshold is enforced automatically by the CI pipeline.

## Continuous Integration

GitHub Actions automatically validates changes submitted to the repository.

The current CI workflow runs on:

* Pushes to `dev`
* Pull requests targeting `dev`
* Pull requests targeting `main`

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
* Secure password storage
* JWT-based authentication
* Ownership-based authorization

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
