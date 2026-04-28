# Todo API

A RESTful API built with **FastAPI**, **SQLAlchemy async**, and **SQLite** — demonstrating
clean architecture, JWT authentication, and production-ready patterns.

## Tech Stack

| Layer      | Technology                 |
| ---------- | -------------------------- |
| Framework  | FastAPI 0.115              |
| ORM        | SQLAlchemy 2.0 (async)     |
| Database   | SQLite (via aiosqlite)     |
| Auth       | JWT (python-jose) + bcrypt |
| Validation | Pydantic v2                |
| Migrations | Alembic                    |
| Runtime    | Python 3.12                |

## Architecture

The project follows a layered architecture separating concerns cleanly:

```text
app/
├── api/v1/endpoints/   # HTTP layer — request/response only
├── services/           # Business logic — validation, rules
├── repositories/       # Data access layer — DB queries only
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic request/response schemas
├── core/               # Config, security, JWT
└── db/                 # Engine, session, base
```

## Features

- JWT authentication (register, login, protected routes)
- Full CRUD for todos, scoped per user
- Filtering by completion status and due date
- Pagination with configurable page size
- Timezone-aware timestamps throughout
- Alembic database migrations
- Auto-generated interactive API docs (Swagger UI + ReDoc)

## Quick Start

```bash
git clone https://github.com/jaynero/fastapi-todo-api.git
cd fastapi-todo-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set a secure SECRET_KEY

alembic upgrade head
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Auth

| Method | Endpoint                | Description                 |
| ------ | ----------------------- | --------------------------- |
| `POST` | `/api/v1/auth/register` | Register a new user         |
| `POST` | `/api/v1/auth/login`    | Login and receive JWT token |

### Users

| Method | Endpoint           | Description              |
| ------ | ------------------ | ------------------------ |
| `GET`  | `/api/v1/users/me` | Get current user profile |

### Todos

| Method   | Endpoint             | Description                        |
| -------- | -------------------- | ---------------------------------- |
| `POST`   | `/api/v1/todos`      | Create a new todo                  |
| `GET`    | `/api/v1/todos`      | List todos (filterable, paginated) |
| `GET`    | `/api/v1/todos/{id}` | Get a single todo                  |
| `PATCH`  | `/api/v1/todos/{id}` | Partially update a todo            |
| `DELETE` | `/api/v1/todos/{id}` | Delete a todo                      |

### Query Parameters for `GET /todos`

| Parameter    | Type       | Description                             |
| ------------ | ---------- | --------------------------------------- |
| `completed`  | `bool`     | Filter by completion: `true` or `false` |
| `due_before` | `datetime` | ISO 8601, e.g. `2026-12-31T23:59:59`    |
| `due_after`  | `datetime` | ISO 8601                                |
| `skip`       | `int`      | Offset for pagination (default: `0`)    |
| `limit`      | `int`      | Page size, max 100 (default: `20`)      |

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:

| Variable                      | Description                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| `SECRET_KEY`                  | JWT signing key — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL`                | SQLAlchemy async DB URL                                                                    |
| `DEBUG`                       | Enables SQL logging and disables production key check                                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime in minutes                                                                    |

## Running Migrations

```bash
# Apply all migrations
alembic upgrade head

# Generate a new migration after changing a model
alembic revision --autogenerate -m "describe your change"

# Roll back one migration
alembic downgrade -1
```

## Project Structure

```text
fastapi-todo-api/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── todos.py
│   │   │   └── users.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── todo.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── todo_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── todo.py
│   │   └── user.py
│   ├── services/
│   │   ├── todo_service.py
│   │   └── user_service.py
│   └── main.py
├── alembic/
│   ├── versions/
│   │   └── 0001_initial_schema.py
│   └── env.py
├── alembic.ini
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
