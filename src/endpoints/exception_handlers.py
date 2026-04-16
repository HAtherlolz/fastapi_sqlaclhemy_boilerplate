from fastapi import Request, Response, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, ValidationError

from src.exceptions.base_exceptions import BaseAppException
from src.utils.logging import logger


class ErrorResponseSchema(BaseModel):
    message: str
    trace_id: str
    error_type: str


def _build_error_response(request: Request, status_code: int, message: str, error_type: str) -> ORJSONResponse:
    response_schema = ErrorResponseSchema(
        message=message,
        trace_id=request.state.trace_id,
        error_type=error_type,
    )
    return ORJSONResponse(status_code=status_code, content=response_schema.model_dump())


async def base_app_exception_handler(request: Request, exc: BaseAppException) -> Response:
    logger.error(f"Handled error: {exc.message}")
    return _build_error_response(
        request=request,
        status_code=exc.status_code,
        message=exc.message,
        error_type=exc.__class__.name,
    )


async def pydantic_validation_exception_handler(request: Request, exc: Exception) -> Response:
    if not any([isinstance(exc, ValidationError), isinstance(exc, RequestValidationError)]):
        logger.error(f"Validation error handler received non-validation exception: {exc}")
        return await unexpected_exception_handler(request, TypeError())

    error = exc.errors()[0]  # type: ignore
    path = ".".join(map(str, error["loc"]))
    message = f"Your request contained invalid structure on path {path}. {error['msg']}"

    return _build_error_response(
        request=request,
        status_code=status.HTTP_400_BAD_REQUEST,
        message=message,
        error_type=exc.__class__.name,
    )


async def unexpected_exception_handler(request: Request, exc: Exception) -> Response:
    logger.exception(f"Unexpected error: {str(exc)}")
    return _build_error_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Unexpected error occurred.",
        error_type=exc.__class__.name,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseAppException, base_app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
