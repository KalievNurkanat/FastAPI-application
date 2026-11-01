import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from google.genai.errors import ServerError
from sqlalchemy.exc import DatabaseError

log = logging.getLogger(__name__)


def register_error_handlers(
    app: FastAPI
):
    @app.exception_handler(RequestValidationError)
    def validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": "Unhandled error",
                "error": exc.errors()
            },
        )

    @app.exception_handler(DatabaseError)
    def database_error_handler(
        request: Request,
        exc: DatabaseError
    ) -> JSONResponse:
        log.error(
            "Unhandled database error",
            exc_info=exc
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error occured. "
                "Our admins already working on it"
            },
        )

    @app.exception_handler(ServerError)
    def server_error_handler(
        request: Request,
        exc: ServerError
    ) -> JSONResponse:
        log.error(
            "Server issues occured",
            exc_info=exc
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "The problems with service occured. Please try again or later"
            },
        )
        
        