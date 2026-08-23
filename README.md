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

- Layered Architecture (Controller → Service → Workflow → Repository)
- Dependency Injection
- SQLAlchemy ORM with PostgreSQL
- Dockerized Development Environment
- Unit and Integration Testing
- Interactive Swagger Documentation

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Containerization | Docker & Docker Compose |
| Testing | pytest |

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

- Docker
- Docker Compose
- Git

### Installation

```bash
git clone https://github.com/ladsonsa/user-crud-api.git
cd user-crud-api
cp .env.example .env
docker compose up
```

## API Documentation

After starting the application, Swagger UI is available at:

```text
http://localhost:8000/docs
```

## Testing

Run the complete test suite:

```bash
docker compose exec api poetry run pytest
```

Generate a coverage report:

```bash
docker compose exec api poetry run coverage html
```

The report is generated in:

```text
htmlcov/index.html
```

## Development Standards

The project follows established backend engineering practices, including:

- SOLID principles
- PEP8 compliance
- Static typing
- Google Style docstrings
- Conventional Commits
- Modular architecture

## Next Improvements

- GitHub Actions (CI)
- Release automation

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.