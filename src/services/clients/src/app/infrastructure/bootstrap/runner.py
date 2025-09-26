from app.adapters.session_creator import SqlalchemySessionCreator

from app.infrastructure.config import RootConfig
from app.infrastructure.bootstrap.config import get_config

from app.repository import ClientRepository
from app.services.client_service import ClientService

from app.logger import get_logger
import logging
from app.ioc import ioc


def init_app(
    app_config_path: str,
    database_config_path: str,
) -> None:
    config = get_config(
        app_config=app_config_path,
        database_config=database_config_path
    )

    session_creator = SqlalchemySessionCreator(
        db_url=config.database.connection_string,
        echo=config.app.sql_echo
    )
    session = session_creator.create_session()

    logger = get_logger("client_service")

    client_repository = ClientRepository(session, logger)
    client_service = ClientService(client_repository, logger)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)
    ioc.set(SqlalchemySessionCreator, session_creator)
    ioc.set(ClientRepository, client_repository)
    ioc.set(ClientService, client_service)
