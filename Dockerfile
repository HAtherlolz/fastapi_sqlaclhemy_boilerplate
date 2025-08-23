FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/app

WORKDIR $APP_HOME

# Install system dependencies for PostgreSQL and build tools
RUN apk add --no-cache --virtual .build-deps \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    && apk add --no-cache \
    postgresql-client \
    ca-certificates

# Upgrade pip and install build tools
RUN pip install --upgrade pip wheel setuptools

RUN apk add --no-cache \
    gcc g++ make musl-dev \
    unixodbc unixodbc-dev

# Copy Poetry files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==1.8.5"
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# Copy project files
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY app/ ./app/
COPY main.py ./

# Create entrypoint script
RUN echo '#!/bin/sh\n\
# Start the application\n\
echo "Starting FastAPI application..."\n\
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload\n\
' > entrypoint.sh

RUN chmod +x entrypoint.sh

# Create non-root user for security
RUN adduser -u 5678 --system --disabled-password --gecos "" app && chown -R app $APP_HOME

USER app

# Expose port
EXPOSE 8000

CMD ["sh", "entrypoint.sh"]