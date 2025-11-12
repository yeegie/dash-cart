from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.category import CategoryNotFound, CategoryAlreadyExists, InvalidCategoryId
from uuid import UUID


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(CategoryNotFound)
    async def category_not_found(request: Request, exc: CategoryNotFound):
        category_id = str(exc.id) if isinstance(exc.id, UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=404,
            content={
                "error": "category_not_found",
                "details": details,
                "category_id": category_id,
                "slug": exc.slug
            }
        )

    @app.exception_handler(CategoryAlreadyExists)
    async def category_already_exists(request: Request, exc: CategoryAlreadyExists):
        category_id = str(exc.id) if isinstance(exc.id, UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=409,
            content={
                "error": "category_already_exists",
                "details": details,
                "category_id": category_id,
                "slug": exc.slug
            }
        )
