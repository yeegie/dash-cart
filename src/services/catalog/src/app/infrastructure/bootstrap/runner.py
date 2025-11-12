from app.adapters.session_creator import SqlalchemySessionCreator

from app.infrastructure.config import RootConfig
from app.infrastructure.bootstrap.config import get_config

from app.repository.category import CategoryRepository
from app.repository.product import ProductRepository

from app.services.category import CategoryService
from app.services.product import ProductService

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

    logger = get_logger("category_service")

    category_repository = CategoryRepository(session, logger)
    product_repository = ProductRepository(session, logger)

    category_service = CategoryService(category_repository, product_repository, logger)
    product_service = ProductService(product_repository, logger)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)

    ioc.set(SqlalchemySessionCreator, session_creator)

    ioc.set(CategoryRepository, category_repository)
    ioc.set(ProductRepository, product_repository)

    ioc.set(CategoryService, category_service)
    ioc.set(ProductService, product_service)
