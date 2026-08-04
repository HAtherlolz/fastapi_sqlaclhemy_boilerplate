FROM python:3.12-slim

WORKDIR /app

# System deps for asyncpg, psycopg2, pyodbc
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies (no dev, no virtualenv)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

# Copy application code
COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
