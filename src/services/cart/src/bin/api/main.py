from app.infrastructure.bootstrap.runner import init_app
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.ioc import ioc
from app.adapters.session_creator import SqlalchemySessionCreator
from app.repository.models.base import Base
from app.routers.cart import CartRouter
from app.repository.cart import CartRepository

import socket

from app.infrastructure.config import RootConfig

import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger.info("[⚙️] Launching the application...")
    app.state.logger.info("[📦] Connecting to the database...")
    app.state.logger.info(f"{app.state.config.database.connection_string}")
    try:
        async with app.state.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    except (OSError, socket.gaierror) as e:
        app.state.logger.critical(f"[❌] Unable to connect to the database: {e}")
        app.state.logger.info(f"[i] The problem may be here:")
        app.state.logger.info("    > Check your connection settings in /configs/database.yaml")
        app.state.logger.info("    > PostgreSQL or docker container")
        raise
    yield
    await app.state.engine.dispose()


def main():
    init_app(
        app_config_path="configs/app.yaml",
        database_config_path="configs/database.yaml",
    )
    config = ioc.get(RootConfig)

    app = FastAPI(
        title="Cart service",
        lifespan=lifespan,
        debug=config.app.debug
    )

    cart_router = CartRouter(ioc.get(CartRepository))

    app.include_router(cart_router, prefix="/carts", tags=["carts"])

    app.state.config = config
    app.state.engine = ioc.get(SqlalchemySessionCreator).get_engine
    app.state.logger = ioc.get(logging.Logger)

    uvicorn.run(
        app,
        host=config.app.host,
        port=config.app.port,
    )


if __name__ == "__main__":
    main()
