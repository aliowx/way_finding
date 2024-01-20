import logging
import traceback
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from app import utils
from app.core.config import settings

logger = logging.getLogger(__name__)


class CustomHTTPException(HTTPException):
    """Custom HTTPException class for common exception handling."""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        msg_code: utils.MessageCodes = utils.MessageCodes.internal_error,
        detail: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.msg_code = msg_code


def get_traceback_info(exc: Exception):
    traceback_str = (traceback.format_tb(exc.__traceback__))[-1]
    traceback_full = "".join(traceback.format_tb(exc.__traceback__))
    exception_type = type(exc).__name__
    return exception_type, traceback_str, traceback_full


def create_system_exception_handler(
    status_code: str,
    msg_code: str,
):
    async def exception_handler(request: Request, exc: Any):
        exception_type, traceback_str, traceback_full = get_traceback_info(exc)
        logger.error(f"Exception of type {exception_type}:\n{traceback_str}")

        response_data = {
            "data": str(exc.errors()),
            "msg_code": msg_code,
            "status_code": status_code,
        }
        if settings.DEBUG:
            raise
        response = utils.APIErrorResponse(**response_data)
        return response

    return exception_handler


def create_exception_handler(status_code):
    async def exception_handler(request: Request, exc: Any):
        exception_type, traceback_str, traceback_full = get_traceback_info(exc)
        logger.error(f"Exception of type {exception_type}:\n{traceback_str}")

        response_data = {
            "data": str(exc.detail),
            "msg_code": exc.msg_code,
            "status_code": status_code,
        }
        if settings.DEBUG:
            raise
        response = utils.APIErrorResponse(**response_data)
        return response

    return exception_handler


async def http_exception_handler(request: Request, exc: Any):
    _, _, traceback_full = get_traceback_info(exc)
    response = utils.APIErrorResponse(
        data=exc.detail,
        msg_code=utils.MessageCodes.internal_error,
        status_code=exc.status_code,
    )
    return response


async def internal_exceptions_handler(request: Request, exc: Any):
    exception_type, traceback_str, traceback_full = get_traceback_info(exc)
    logger.error(f"Unhandled {exception_type} Exception Happened:\n{traceback_str}")

    error_msg = ""
    if settings.DEBUG:
        error_msg = str(exc)

    return utils.APIErrorResponse(
        data=error_msg,
        msg_code=utils.MessageCodes.internal_error,
        status_code=500,
    )


# Define custom exception classes
class ValidationException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class NotFoundException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class AlreadyExistException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class InternalErrorException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class UnauthorizedException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class ForbiddenException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


# Create a dictionary of exception handlers
exception_handlers = {
    Exception: internal_exceptions_handler,
    HTTPException: http_exception_handler,
    ValidationException: create_exception_handler(status.HTTP_400_BAD_REQUEST),
    NotFoundException: create_exception_handler(status.HTTP_404_NOT_FOUND),
    AlreadyExistException: create_exception_handler(status.HTTP_409_CONFLICT),
    InternalErrorException: create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ),
    UnauthorizedException: create_exception_handler(status.HTTP_401_UNAUTHORIZED),
    ForbiddenException: create_exception_handler(status.HTTP_403_FORBIDDEN),
    RequestValidationError: create_system_exception_handler(
        status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.bad_request
    ),
    ResponseValidationError: create_system_exception_handler(
        status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.internal_error
    ),
}


def handle_exception(request: Request, exc: Any):
    exc_type = type(exc)
    if exc_type is Exception:
        return internal_exceptions_handler
    if exc_type is HTTPException:
        return http_exception_handler
    if exc_type is ValidationException:
        return create_exception_handler(status.HTTP_400_BAD_REQUEST)
    if exc_type is NotFoundException:
        return create_exception_handler(status.HTTP_404_NOT_FOUND)
    if exc_type is AlreadyExistException:
        return create_exception_handler(status.HTTP_409_CONFLICT)
    if exc_type is InternalErrorException:
        return create_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    if exc_type is UnauthorizedException:
        return create_exception_handler(status.HTTP_401_UNAUTHORIZED)
    if exc_type is ForbiddenException:
        return create_exception_handler(status.HTTP_403_FORBIDDEN)
    if exc_type is RequestValidationError:
        return create_system_exception_handler(
            status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.bad_request
        )
    if exc_type is ResponseValidationError:
        return create_system_exception_handler(
            status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.internal_error
        )

    return internal_exceptions_handler(request, exc)
