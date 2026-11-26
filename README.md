# Gestion Cabinet Medical

A Django-based medical appointment management system developed
as part of the Technologies Web 2.0 course at ESPRIT.

## Technology Stack

- Python 3.12
- Django 5.2 LTS
- SQLite
- uv

## Project Structure

- `config/` — Project configuration.
- `cabinet/` — Users, patients, doctors and specialities.
- `appointments/` — Medical appointment management.
- `docs/` — Case study and project documentation.

## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Generate a Django secret key:

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set `DJANGO_SECRET_KEY` in the `.env` file.

### 3. Apply database migrations

```bash
uv run python manage.py migrate
```

### 4. Start the development server

```bash
uv run python manage.py runserver
```

Access the development server at http://127.0.0.1:8000.

## Development Status

- [x] Project initialization
- [x] Data modeling
- [x] Field validation and database constraints
- [x] Database migrations
- [x] Manual model testing
- [ ] Back-office
- [ ] Front-office
- [ ] REST API

## Documentation

See [Case Study](docs/CASE_STUDY.md) for project requirements.