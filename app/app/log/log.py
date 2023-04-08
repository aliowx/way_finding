import logging
import json
from typing import Callable

import httpx

from fastapi import Request, BackgroundTasks
from fastapi.routing import APIRoute
from fastapi.responses import Response

from app import crud, schemas, exceptions
from app.db.session import async_session


logger = logging.getLogger(__name__)


async def save_request_log_async(
        request: Request,
        response: Response = None,
        trace_back: str = ""
) -> None:
    authorization = request.headers.get("authorization")
    client_host = request.client.host
    service_name = request.url.path
    method = request.method
    request_data = {
        "body": {},
        "path_params": str(request.path_params),
        "query_params": str(request.query_params),
    }

    response_data = ""
    if response:
        if "json" not in response.headers.get("content-type"):
            response_data = json.dumps(dict(response.headers))
        else:
            response_data = str(response.body)

    try:
        request_data["body"] = await request.json()
    except Exception as e:
        pass

    request_log_data = {
        "authorization": authorization,
        "service_name": service_name,
        "method": method,
        "ip": client_host,
        "request": json.dumps(request_data),
        "response": response_data,
        "trace": trace_back,
    }

    request_log_in = schemas.request_log.RequestLogCreate(**request_log_data)
    async with async_session() as db:
        await crud.request_log.create(db=db, obj_in=request_log_in)
        await db.commit()


async def save_ws_request_log_async(
        request: httpx.Request,
        response: httpx.Response,
) -> None:
    authorization = request.headers.get("Authorization")
    service_name = request.url.path
    method = request.method
    response_data = str(response.text) or None
    query_params = request.url.query
    request_data = {
        "url": str(request.url),
        "body": "",
        "query_params": query_params,
    }

    try:
        request_data["body"] = request.content
    except Exception as e:
        pass

    ws_request_log_data = {
        "authorization": authorization,
        "request": str(request_data),
        "response": response_data,
        "service_name": service_name,
        "method": method,
        "status_code": response.status_code,
    }

    ws_request_log_in = schemas.ws_request_log.WSRequestLogCreate(**ws_request_log_data)
    async with async_session() as db:
        await crud.ws_request_log.create(db=db, obj_in=ws_request_log_in)
        await db.commit()


class LogRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                response = await exceptions.handle_exception(request, e)
                return response

            if not response.background:
                tasks = BackgroundTasks()
                tasks.add_task(save_request_log_async, request, response)
                response.background = tasks
            else:
                response.background.add_task(save_request_log_async, request, response)
            return response

        return custom_route_handler
