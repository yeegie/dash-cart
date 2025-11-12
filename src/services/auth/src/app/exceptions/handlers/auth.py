from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.auth_exceptions import InvalidCode, InvalidPhoneNumber, InvalidToken


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidCode)
    async def invalid_code(request: Request, exc: InvalidCode):
        details = exc.details if exc.details else "No additional details provided."
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_code",
                "details": details,
            }
        )

    @app.exception_handler(InvalidPhoneNumber)
    async def invalid_phone_number(request: Request, exc: InvalidPhoneNumber):
        details = exc.details if exc.details else "No additional details provided."
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_phone",
                "details": details,
            }
        )
    
    @app.exception_handler(InvalidToken)
    async def invalid_token(request: Request, exc: InvalidPhoneNumber):
        details = exc.details if exc.details else "No additional details provided."
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_token",
                "details": details,
            }
        )
