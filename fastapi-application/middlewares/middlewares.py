import logging
import time
from collections.abc import Awaitable, Callable

from core.config import settings
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.request_counts import request_count_middleware_dispatch

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format
)

log = logging.getLogger(__name__)

type CallNext = Callable[[Request], Awaitable[Response]]

AllowOrigins = [
    "http://localhost:8000",
    "http://localhost"
]

app = FastAPI()


async def add_proccess_time_to_requests(
        request: Request,
        call_next: CallNext
):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.5f}"
    return response


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(
            self, 
            *args, 
            process_time_header_name: str, 
            **kwargs
        ) -> Response:
        super().__init__(*args, **kwargs)
        self.process_time_header_name = process_time_header_name

    async def dispatch(
            self,
            request: Request,
            call_next: CallNext):
        start = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start
        response.headers[self.process_time_header_name] = f"{process_time:.5f}"
        return response
    

def register_middlewares(app: FastAPI):
    @app.middleware("http")
    async def log_new_requests(
        request: Request,
        call_next: CallNext
    ) -> Response:
        log.info(
            "Request %s to %s",
            request.method,
            request.url.path
        )
        return await call_next(request)

    app.middleware("http")(add_proccess_time_to_requests)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=AllowOrigins,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(
        ProcessTimeMiddleware,
        process_time_header_name="Process-Time"
    )
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=request_count_middleware_dispatch
    )
