# FastAPI SQLAlchemy async boilerplate

## This boilerplate provides configured FastAPI application, SQLAlchemy orm async, alembic - migrations, sqladmin - customizable admin panel

## Setup

### Option 1: Using Poetry (Recommended)

1. Clone repo using `git clone https://github.com/HAtherlolz/fastapi_sqlaclhemy_boilerplate.git`
2. Install Python 3.11 +
3. Install PostgreSQL 14 +
4. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
5. Install dependencies: `poetry install`
6. Activate virtual environment: `poetry shell`
7. Create `.env` file inside cloned project and type inside it:

```
# SMTP Settings
 MAIL_USERNAME=
 MAIL_PASSWORD=
 MAIL_FROM=
 MAIL_PORT=587
 MAIL_SERVER=smtp.gmail.com
 MAIL_STARTTLS=False
 MAIL_SSL_TLS=True
 USE_CREDENTIALS=True
 VALIDATE_CERTS=True

# PROJECT NAME
 PROJECT_NAME=

# SWAGGER URL
 SWAGGER_URL=

# DOMAIN
 DOMAIN=

# DB Connection
 DB_NAME=
 DB_USER=
 DB_PASSWORD=
 DB_HOST=
 DB_PORT=
 DB_URL=

# JWT
 SECRET_KEY=
 ALGORITHM=
 ACCESS_TOKEN_EXPIRE_MINUTES=
```

### Option 2: Using pip (Legacy)

1. Clone repo using `git clone https://github.com/HAtherlolz/fastapi_sqlaclhemy_boilerplate.git`
2. Install Python 3.11 +
3. Install PostgreSQL 14 +
4. Install virtualenv package for Python `pip install virtualenv`
5. Create virtualenv `virtualenv <name_of_env>`
6. Activate it `source <name_of_env>/bin/activate` (for Windows: `cd <name_of_env>/Scripts`, `activate`)
7. Install all the required packages for project using
   ### For Linux / MacOs
    Run the command - `pip install -r requirements.txt --no-deps`
   ### For Windows
   1 . Comment `uvloop` module in `requirements.txt` 
   2 . Change 'psycopg2-binary' to 'psycopg2'
   3 . Run the command - `pip install -r requirements.txt --no-deps`
   
8. Create `.env` file (same as above)

## Start the app
- Now you can start the project `uvicorn main:app` and navigate to `localhost:8000`
- The flag `--reload` allows you to automatically restart the server after the applied changes in the code
- The flag `--port` allows you to change port.

## Migrations
### WARNING! - Do not forget to import all models to app/models/__init__.py
### Create a migrations file
- alembic revision --autogenerate -m "name_of_your_migration"
### Run last migrations
- alembic upgrade head 


## Swagger url: 
- `{domain}/api/v1/docs/`

## Poetry Commands
- `poetry install` - Install dependencies
- `poetry add <package>` - Add a new dependency
- `poetry add --group dev <package>` - Add a development dependency
- `poetry shell` - Activate virtual environment
- `poetry run <command>` - Run command in virtual environment
- `poetry update` - Update dependencies
- `poetry export -f requirements.txt --output requirements.txt` - Export to requirements.txt

# Run Docker Container

## Prerequisites
Install Docker and Docker Compose:

### For Linux
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (optional)
sudo usermod -aG docker $USER
```

### For macOS
Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop

### For Windows
Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop

## Environment Setup
1. Create a `.env` file in the project root with your configuration:
```bash
# Database Configuration
DB_USERNAME=postgres
DB_PASSWORD=your_secure_password
DB_HOST=postgres-db
DB_PORT=5432
DB_DATABASE=fastapi_db
DB_ENGINE=postgres
DB_PASSWORD_AUTH=true
DB_URL=postgresql://postgres:your_secure_password@postgres-db:5432/fastapi_db

# Application Configuration
PROJECT_NAME=FastAPI SQLAlchemy Boilerplate
DOMAIN=localhost:8000
SWAGGER_URL=/api/v1/docs/

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SMTP Configuration (optional)
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=False
MAIL_SSL_TLS=True
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```

## Run Docker containers

### Architecture
The Docker setup includes three main services:
- **postgres**: PostgreSQL database with health checks
- **migrations**: Runs database migrations before the app starts
- **app**: FastAPI application (starts after migrations complete)

### Development mode
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up --build -d

# View logs
docker-compose logs -f app

# View migration logs
docker-compose logs migrations
```

### Production mode
```bash
# Build and start in production mode
docker-compose -f docker-compose.yml up --build -d
```

## Access the application
- **FastAPI Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs/
- **ReDoc Documentation**: http://localhost:8000/api/v1/redoc/
- **PostgreSQL Database**: localhost:5432

## Docker Commands

### Basic operations
```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# View running containers
docker-compose ps

# View logs
docker-compose logs [service_name]

# Execute commands in running container
docker-compose exec app poetry run alembic upgrade head
docker-compose exec app poetry shell
```

### Database operations
```bash
# Access PostgreSQL
docker-compose exec postgres-db psql -U postgres -d ${DB_DATABASE:-fastapi_db}

# Run migrations manually (if needed)
docker-compose exec app poetry run alembic upgrade head

# Create new migration
docker-compose exec app poetry run alembic revision --autogenerate -m "migration_name"

# Run migrations service separately
docker-compose run --rm migrations
```

### Cleanup
```bash
# Stop and remove containers, networks
docker-compose down

# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove all containers and images
docker system prune -a
```
