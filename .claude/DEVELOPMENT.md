# Development Guidelines

## Code Style

- Use type hints for all functions
- Add docstrings to functions
- Follow ruff formatting rules

## Database

- All models inherit from `Base` in `models/base.py`
- Add `created_at` and `updated_at` timestamps
- Use `ForeignKey` constraints for relationships

## API Design

- RESTful style
- Version control with `/api/v1/`
- Use `APIRouter` for organization
- Consistent response schemas

## Testing

- Use `@pytest.mark.asyncio` for async tests
- Reset database state with fixtures
- Cover normal and edge cases

## Git Commits

- Use semantic commit messages
- Format: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`
