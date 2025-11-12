# from app.adapters.session_creator import SqlalchemySessionCreator
import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from app.infrastructure.config import RootConfig
from app.infrastructure.bootstrap.config import get_config

from app.service.auth import AuthService
from app.clients.user import UserClient

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
    logger = get_logger("auth_service")

    try:
        logger.info("[📦] Connecting to the Redis...")
        pool = ConnectionPool.from_url(
            "redis://localhost:6379",
            max_connections=10,
            decode_responses=True,
        )
        redis_client = redis.Redis(connection_pool=pool)
        logger.info("[i] Redis connected successfully")
    except Exception as ex:
        logger.critical(f"Failed to connect the Redis\n{ex}")
        raise
    
    # Clients
    user_client = UserClient("http://localhost:8001", logger)
    
    # Services
    auth_service = AuthService(redis_client, user_client, logger)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)
    ioc.set(AuthService, auth_service)
