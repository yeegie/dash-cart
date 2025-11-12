from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.product import ProductNotFound, ProductAlreadyExists, InvalidProductId
from uuid import UUID


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ProductNotFound)
    async def product_not_found(request: Request, exc: ProductNotFound):
        product_id = str(exc.id) if isinstance(exc.id, UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=404,
            content={
                "error": "product_not_found",
                "details": details,
                "product_id": product_id,
                "slug": exc.slug
            }
        )

    @app.exception_handler(ProductAlreadyExists)
    async def product_already_exists(request: Request, exc: ProductAlreadyExists):
        product_id = str(exc.id) if isinstance(exc.id, UUID) else exc.id
        details = exc.details if exc.details else "No additional details provided."

        return JSONResponse(
            status_code=409,
            content={
                "error": "product_already_exists",
                "details": details,
                "product_id": product_id,
                "slug": exc.slug
            }
        )
