import logging
import traceback
from typing import Any

from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from httpx import HTTPError, RequestError, ConnectError
from requests import RequestException
from starlette.background import BackgroundTask

from app import utils
from app.log import log


logger = logging.getLogger(__name__)


class CustomException(HTTPException):
    def __init__(self, status_code, data, msg_status=2, msg_code=2):
        super().__init__(status_code)
        self.data = data
        self.msg_status = msg_status
        self.msg_code = msg_code


def get_error_log_background_task(
    request: Request, trace_back: str, response: Response = None
):
    task = BackgroundTask(
        log.save_request_log_async,
        request=request,
        response=response,
        trace_back=trace_back,
    )
    return task


def get_traceback_info(exc: Exception):
    traceback_str = (traceback.format_tb(exc.__traceback__))[-1]
    traceback_full = "".join(traceback.format_tb(exc.__traceback__))
    exception_type = type(exc).__name__
    return exception_type, traceback_str, traceback_full


async def custom_exception_handler(request: Request, exc: Any):
    exception_type, traceback_str, traceback_full = get_traceback_info(exc)
    logger.error(f"Internal service error{exception_type}:\n{traceback_str}")

    response = utils.CustomResponse(
        data=exc.data,
        msg_code=exc.msg_code,
        msg_status=exc.msg_status,
        status_code=exc.status_code,
    )
    log_background_task = get_error_log_background_task(
        request=request, response=response, trace_back=traceback_full
    )
    response.background = log_background_task
    return response


async def http_exception_handler(request: Request, exc: Any):
    _, _, traceback_full = get_traceback_info(exc)

    response = utils.CustomResponse(
        data={"detail": str(exc).strip()}
        if str(exc).strip()
        else {"message": "Internal Server Error"},
        msg_code=utils.MessageCodes.Internal_Error,
        msg_status=2,
        status_code=exc.status_code,
    )
    log_background_task = get_error_log_background_task(
        request=request, response=response, trace_back=traceback_full
    )
    response.background = log_background_task
    return response


async def http_request_exceptions_handler(request: Request, exc: Any):
    exception_type, traceback_str, _ = get_traceback_info(exc)
    logger.error(f"Http Request {exception_type} Exception Happened:\n{traceback_str}")

    response = utils.CustomResponse(
        data={"detail": str(exc).strip()}
        if str(exc).strip()
        else {"message": "External Error"},
        msg_code=utils.MessageCodes.External_Error,
        msg_status=1,
        status_code=503,
    )
    
    return response


async def internal_exceptions_handler(request: Request, exc: Any):
    exception_type, traceback_str, traceback_full = get_traceback_info(exc)
    logger.error(f"Unhandled {exception_type} Exception Happened:\n{traceback_str}")

    response = utils.CustomResponse(
        data={"detail": str(exc).strip()}
        if str(exc).strip()
        else {"message": "Internal Server Error"},
        msg_code=utils.MessageCodes.Internal_Error,
        msg_status=2,
        status_code=500,
    )
    log_background_task = get_error_log_background_task(
        request, response=response, trace_back=traceback_full
    )
    response.background = log_background_task
    return response


def handle_exception(request: Request, exc: Any):
    exc_type = type(exc)
    if exc_type is HTTPException:
        return http_exception_handler(request, exc)
    if exc_type is CustomException:
        return custom_exception_handler(request, exc)
    if exc_type in [RequestException, RequestError, HTTPError, ConnectError]:
        return http_request_exceptions_handler(request, exc)
    return internal_exceptions_handler(request, exc)


http_exceptions = (HTTPException, http_exception_handler)
custom_exception = (CustomException, custom_exception_handler)
http_request_exceptions = (RequestException, http_request_exceptions_handler)
httpx_request_exceptions = (RequestError, http_request_exceptions_handler)
httpx_http_exceptions = (HTTPError, http_request_exceptions_handler)
httpx_connect_exceptions = (ConnectError, http_request_exceptions_handler)
