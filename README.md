# financial-api

Microservice REST API for personal finance control.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL

## Setup

Activate the conda environment (dependencies already installed):

```bash
conda activate financial-control
```

Copy environment variables:

```bash
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/api/v1/docs

## Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
alembic upgrade head
```

## Tests

```bash
pytest
```
