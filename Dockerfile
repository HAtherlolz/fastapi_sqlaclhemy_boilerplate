FROM python:3.12-alpine

# -------------------------
# Environment
# -------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/app

WORKDIR ${APP_HOME}

# -------------------------
# System dependencies
# -------------------------
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    postgresql-client \
    unixodbc \
    unixodbc-dev \
    ca-certificates

# -------------------------
# Python tooling
# -------------------------
RUN pip install --upgrade pip setuptools wheel
RUN pip install poetry==1.8.5

# Disable venv inside container
RUN poetry config virtualenvs.create false

# -------------------------
# Install dependencies
# -------------------------
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi

# -------------------------
# Copy application
# -------------------------
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY src/ ./src/

# -------------------------
# Security: non-root user
# -------------------------
RUN adduser -D -u 5678 app \
    && chown -R app:app ${APP_HOME}

USER app

# -------------------------
# Expose & Run
# -------------------------
EXPOSE 8000

CMD ["uvicorn", "src.main:create_api", "--factory", "--host", "0.0.0.0", "--port", "8000"]