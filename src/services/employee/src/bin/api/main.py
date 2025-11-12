from app.infrastructure.bootstrap.runner import init_app
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.ioc import ioc
from app.adapters.session_creator import SqlalchemySessionCreator
from app.repositories.models.base import Base

from app.routers.employee import EmployeeRouter
from app.routers.shift import ShiftRouter
# from app.routers.exceptions import register_exception_handlers

from app.services.employee import EmployeeService
from app.services.shift import ShiftService

from app.infrastructure.config import RootConfig

import socket

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
        title="Employee service",
        lifespan=lifespan,
        debug=config.app.debug
    )
    app.state.config = config
    app.state.engine = ioc.get(SqlalchemySessionCreator).get_engine
    app.state.logger = ioc.get(logging.Logger)

    employee_router = EmployeeRouter(ioc.get(EmployeeService))
    shift_router = ShiftRouter(ioc.get(ShiftService))

    app.include_router(employee_router, prefix="/employees", tags=["employees"])
    app.include_router(shift_router, prefix="/shifts", tags=["shifts"])
    
    # register_exception_handlers(app)
    # register_exception_handlers(app)

    if config.app.debug:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


    uvicorn.run(
        app,
        host=config.app.host,
        port=config.app.port,
    )


if __name__ == "__main__":
    main()
