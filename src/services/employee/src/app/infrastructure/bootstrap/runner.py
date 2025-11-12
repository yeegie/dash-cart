from app.adapters.session_creator import SqlalchemySessionCreator

from app.infrastructure.config import RootConfig
from app.infrastructure.bootstrap.config import get_config

from app.repositories.employee import EmployeeRepository
from app.repositories.shift import ShiftRepository

from app.services.employee import EmployeeService
from app.services.shift import ShiftService

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

    logger = get_logger("employee_service")

    employee_repository = EmployeeRepository(session, logger)
    shift_repository = ShiftRepository(session, logger)

    employee_service = EmployeeService(employee_repository, logger)
    shift_service = ShiftService(shift_repository, logger)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)

    ioc.set(SqlalchemySessionCreator, session_creator)

    ioc.set(EmployeeRepository, employee_repository)
    ioc.set(ShiftRepository, shift_repository)

    ioc.set(EmployeeService, employee_service)
    ioc.set(ShiftService, shift_service)
