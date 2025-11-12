from app.adapters.session_creator import SqlalchemySessionCreator

from app.infrastructure.config import RootConfig
from app.infrastructure.bootstrap.config import get_config

from app.repository import UserRepository
from app.services.user import UserService

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

    user_repository = UserRepository(session, logger)
    user_service = UserService(user_repository, logger)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)
    ioc.set(SqlalchemySessionCreator, session_creator)
    ioc.set(UserRepository, user_repository)
    ioc.set(UserService, user_service)
