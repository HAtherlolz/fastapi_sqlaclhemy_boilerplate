from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqladmin import Admin

from app.config.config import settings
# from app.config.database import engine

from app.endpoints.routers import api_router
# from app.endpoints import admins_models

app = FastAPI(
    openapi_url="/api/v1/",
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/",
    title=f"{settings.PROJECT_NAME}",
    description=f"Backend for {settings.PROJECT_NAME}",
    version="0.1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

# Include admin panel

# admin = Admin(app, engine, "/api/v1/admin/")

# for view in admins_models:
#     admin.add_view(view)
