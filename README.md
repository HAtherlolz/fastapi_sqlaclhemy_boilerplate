# FastAPI SQLAlchemy async boilerplate

## This boilerplate provides configured FastAPI application, SQLAlchemy orm async, alembic - migrations, sqladmin - customizable admin panel

## Setup
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
   
8. Create `.env` file inside cloned project and type inside it:

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


# Run Docker Container

## Setup for Linux
Install Docker, docker-compose:
```
sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

sudo apt-get install docker-ce
sudo apt-get install docker-compose


###### Check Docker deamon status ######
sudo systemctl status docker
```

## Setup for Windows
Update WSL and install Docker:
```
https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
```

## Run Docker containers
- Backend runs on port 5000 

```
sudo docker-compose up --build
```

# To run docker container in background use flag `-d`

```
sudo docker-compose up --build -d
```

## 3.4 Delete containers
```
docker rm -f $(docker ps -a -q)
```
