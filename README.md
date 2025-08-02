# Directory API

REST API for Organizations Directory built with FastAPI, SQLAlchemy, and PostgreSQL.

## Requirements

- Docker and Docker Compose

## Setup and Running

1. Clone the repository:
```bash
git clone https://github.com/musashimiyomoto/directory.git
cd directory
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
