"""
Container for the application.
"""

from dependency_injector import containers, providers

from app.config.config import DatabaseSettings, Settings
from app.config.database import Database


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(Settings)

    db_settings = providers.Singleton(DatabaseSettings)

    db = providers.Singleton(
        Database,
        db_settings=db_settings,
    )

    # schema_repository = providers.Factory(
    #     SchemaRepository,
    #     db=db,
    # )

    # claim_repository = providers.Factory(
    #     ClaimRepository,
    #     db=db,
    # )

    # schema_service = providers.Factory(
    #     SchemaService,
    #     schema_repository=schema_repository,
    # )

    # claim_service = providers.Factory(
    #     ClaimService,
    #     claim_repository=claim_repository,
    #     message_service=message_service,
    # )

    # extraction_repo = providers.Factory(
    #     ExtractionRepository,
    #     db=db,
    # )

    # extraction_service = providers.Factory(
    #     ExtractionService,
    #     claims_service=claim_service,
    #     extraction_repo=extraction_repo,
    # )
