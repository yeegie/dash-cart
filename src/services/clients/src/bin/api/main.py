from app.infrastructure.bootstrap.runner import init_app
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.ioc import ioc
from app.adapters.session_creator import SqlalchemySessionCreator
from app.repository.models.base import Base

from app.routers.client import ClientRouter
from app.services.client_service import ClientService
from app.routers.exceptions import register_exception_handlers

from app.infrastructure.config import RootConfig

import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger.info("[⚙️] Launching the application...")
    async with app.state.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await app.state.engine.dispose()


def main():
    init_app(
        app_config_path="configs/app.yaml",
        database_config_path="configs/database.yaml",
    )
    config = ioc.get(RootConfig)

    app = FastAPI(
        title="Client service",
        lifespan=lifespan,
        debug=config.app.debug
    )
    app.state.engine = ioc.get(SqlalchemySessionCreator).get_engine
    app.state.logger = ioc.get(logging.Logger)

    client_router = ClientRouter(ioc.get(ClientService))
    app.include_router(client_router, prefix="/client", tags=["client"])
    register_exception_handlers(app)

    uvicorn.run(
        app,
        host=config.app.host,
        port=config.app.port,
    )


if __name__ == "__main__":
    main()
