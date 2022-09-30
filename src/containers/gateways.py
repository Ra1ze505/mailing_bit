from dependency_injector import containers, providers

from src.common.bot import init_bot
from src.common.db import Database
from src.common.logging import setup_logging
from src.common.scheduler import init_scheduler


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging_setup: providers.Provider[None] = providers.Resource(
        setup_logging, config=config.logger
    )
    db = providers.Singleton(Database, config.database)
    bot = providers.Singleton(init_bot, config.bot)
    scheduler = providers.Singleton(init_scheduler)
