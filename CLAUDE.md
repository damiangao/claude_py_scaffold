# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Py Scaffold - A FastAPI Python scaffold optimized for Claude Code development.

## Common Commands

```bash
# Install dependencies
uv sync          # production
uv sync --dev    # development

# Run server
uv run uvicorn claude_py_scaffold.main:app --reload

# Testing
uv run pytest
uv run pytest tests/test_users.py::test_create_user

# Code quality
uv run ruff check .
uv run ruff format .

# Database migrations
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
uv run alembic downgrade -1

# Publish
uv build
uv publish
```

## Project Structure

```
claude_py_scaffold/
├── claude_py_scaffold/        # Main package
│   ├── main.py              # App entry point
│   ├── config.py            # Config (pydantic-settings)
│   ├── database.py          # Database (SQLAlchemy async)
│   ├── logging.py           # Logging config
│   ├── middleware.py        # CORS middleware
│   ├── exceptions.py        # Custom exceptions
│   ├── handlers.py          # Exception handlers
│   ├── deps.py              # Dependencies
│   ├── security.py          # Password hashing
│   ├── token.py             # JWT tokens
│   ├── schemas.py           # Pydantic models
│   ├── utils/               # Utilities
│   │   └── pagination.py    # Pagination helper
│   ├── models/              # SQLAlchemy models
│   │   ├── base.py          # Base model
│   │   └── user.py          # User model
│   └── routers/
│       └── v1/              # API v1
│           ├── auth.py      # Auth routes
│           └── users.py     # User routes
├── tests/
│   └── test_users.py        # Unit tests
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env.example
├── Dockerfile
└── README.md
```

## Module Details

### Config (config.py)
- `pydantic-settings` for environment variables
- `get_settings()` returns singleton

### Database (database.py)
- Async SQLAlchemy engine
- `get_db()` dependency injection

### Logging (logging.py)
- Colored console output
- `setup_logging()` initializes logging
- `get_logger(name)` gets logger instance

### Exception Handling (exceptions.py, handlers.py)
- `AppException` base class
- `NotFoundException`, `DuplicateException` subclasses
- `register_exception_handlers()` registers handlers

### Middleware (middleware.py)
- CORS support (localhost:3000/8080 by default)

### Pagination (utils/pagination.py)
- `PaginationParams` - page, page_size
- `paginate()` - generic pagination function
- `PaginatedResponse` - response format

### Migrations (alembic/)
- Config in `alembic.ini`
- Scripts in `alembic/versions/`
- Use `uv run alembic revision --autogenerate -m "msg"`

## Code Style

- Type hints for all functions
- Pydantic models in `schemas.py`
- Routes organized in `routers/` by module
- Import order: stdlib → third-party → local (auto-sorted by ruff)
- One model per file, exported in `models/__init__.py`
- Use `PaginationParams` and `paginate()` for pagination

## Pre-commit

- Config in `.pre-commit-config.yaml`
- Auto runs ruff check and format on commit
- Uses `--exit-non-zero-on-fix` to catch unfixable issues

## Testing

- Tests in `tests/` directory
- Use `httpx.AsyncClient` for API tests
- Reset database state with fixtures
- Test functions start with `test_`

## Claude Code Optimization

### Permissions

`.claude/settings.local.json` auto-approves common commands:
- `uv sync/run` - package management
- `pytest/ruff/pre-commit` - testing and linting
- `alembic` - database migrations
- `git status/diff/log` - read-only git operations
- `ls/cat/find` - file operations

Commands requiring confirmation:
- `git add/commit/push` - git history changes
- `rm/mv/cp` - file modifications
- `docker*` - container operations

### Quick Start for New Modules

See `.claude/commands.md` for templates:

1. Model → `models/<name>.py`
2. Schema → `schemas.py`
3. Router → `routers/v1/<name>.py`
4. Tests → `tests/test_<name>.py`
5. Migration → `alembic revision`

### Context Guidelines

- Keep code simple, avoid over-engineering
- Follow existing patterns (see `users.py`)
- Read related files before modifying
