[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/directory-api/actions/workflows/ci.yml/badge.svg)](https://github.com/musashimiyomoto/directory-api/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Directory API

REST API for Organizations Directory built with FastAPI, SQLAlchemy, and PostgreSQL.

## Requirements

- Docker and Docker Compose

## Setup and Running

1. Clone the repository:
```bash
git clone https://github.com/musashimiyomoto/directory-api.git
cd directory-api
```

2. Create an environment file:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your settings.


4. Start the application with Docker Compose:
```bash
docker compose up --build
```

5. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
