import logging
import traceback
from typing import Any, Union

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
        detail: Union[str, None] = None,
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


# Define custom exception classes
class ValidationException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class NotFoundException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class AlreadyExistException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class InternalErrorException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class UnauthorizedException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


class ForbiddenException(CustomHTTPException):
    def __init__(self, detail: Union[str, None] = None, msg_code: utils.MessageCodes = None):
        super().__init__(msg_code=msg_code, detail=detail)


# Create a dictionary of exception handlers
exception_handlers = {
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
