from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.client_exceptions import ClientNotFound, ClientAlreadyExists
import uuid


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ClientNotFound)
    async def client_not_found(request: Request, exc: ClientNotFound):
        client_id = str(exc.id) if isinstance(exc.id, uuid.UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=404,
            content={
                "error": "client_not_found",
                "details": details,
                "client_id": client_id,
                "telephone": exc.telephone
            }
        )

    @app.exception_handler(ClientAlreadyExists)
    async def client_already_exists(request: Request, exc: ClientAlreadyExists):
        client_id = str(exc.id) if isinstance(exc.id, uuid.UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=409,
            content={
                "error": "client_already_exists",
                "details": details,
                "client_id": client_id,
                "telephone": exc.telephone
            }
        )
