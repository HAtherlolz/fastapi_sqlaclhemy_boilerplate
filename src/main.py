from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

from src.config.config import settings
from src.endpoints.routers import api_router

# Init of the httpx client for the whole app.
from src.utils.logging import LoggingConfig, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to create and close global HTTP Client."""
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=5.0, read=60.0, write=60.0, pool=5.0),
        limits=httpx.Limits(max_connections=200, max_keepalive_connections=20),
    ) as app_client:
        logger.info("Created global HTTP Client for the app lifespan.")
        app.state.app_client = app_client  # type: ignore[attr-defined]
        yield
    logger.info("Destroyed global HTTP Client for the app lifespan.")


# App initialization
def create_api() -> FastAPI:
    app = FastAPI(
        openapi_url="/api/v1/",
        docs_url="/docs",
        redoc_url="/redoc",
        title=f"{settings.PROJECT_NAME}",
        description=f"Backend for {settings.PROJECT_NAME}",
        version="0.1",
        lifespan=lifespan,
    )

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router)

    return app


def run_api():
    in_development_mode = os.getenv("ENV", "prod") == "dev"
    use_web_concurrency = "WEB_CONCURRENCY" in os.environ

    options = {
        "host": "0.0.0.0",
        "port": 8000,
        "log_level": "debug",
        "reload": in_development_mode,
        "factory": True,
        "log_config": LoggingConfig.LOGGING_CONFIG,
    }

    if not in_development_mode and use_web_concurrency:
        options["workers"] = int(os.getenv("WEB_CONCURRENCY"))

    uvicorn.run("src.main:create_api", **options)


if __name__ == "main":
    run_api()
