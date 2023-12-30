from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db import Database
from src.data.repositories.bot import BotRepository
from src.data.repositories.news import NewsRepository
from src.data.repositories.parse import ParseNewsRepository, ParseRateRepository
from src.data.repositories.rate import RateRepository
from src.data.repositories.user import UserRepository
from src.data.repositories.weather import WeatherApiRepository
from src.domain.weather.interfaces import IWeatherRepository


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db: providers.Provider[Database] = providers.Dependency()
    session: providers.Provider[AsyncSession] = providers.Dependency()
    gateways = providers.DependenciesContainer()

    bot_repo = providers.Factory(BotRepository, bot=gateways.bot, db=db, session=session)
    parse_news_repo = providers.Factory(
        ParseNewsRepository,
        parse_client=gateways.parse_client,
        config=config.parse,
    )
    parse_rate_repo = providers.Factory(ParseRateRepository, api_url=config.rate.api_url)
    weather: providers.Factory[IWeatherRepository] = providers.Factory(
        WeatherApiRepository,
        config=config.open_weather,
    )
    user_repo = providers.Factory(UserRepository, db=db, session=session)
    news_repo = providers.Factory(NewsRepository, db=db, session=session)
    rate_repo = providers.Factory(RateRepository, db=db, session=session)
