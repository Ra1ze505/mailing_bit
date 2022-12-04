from dependency_injector import containers, providers

from src.domain.handlers.use_cases.start import StartHandler
from src.domain.handlers.use_cases.weather import WeatherByDayHandler, WeatherHandler
from src.domain.mailing.use_cases.bulk_mailing import BulkMailing
from src.domain.mailing.use_cases.mailing import Mailing
from src.domain.news.use_cases.parse_last_news import ParseLastNews
from src.domain.rate.use_cases.parse_current_rate import ParseCurrentRate
from src.domain.user.use_cases.get_or_create import GetOrCreateUser
from src.domain.weather.use_cases.get_weather_forecast import GetWeatherForecast
from src.domain.weather.use_cases.get_weather_now import GetWeatherNow


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    get_or_create_user = providers.Factory(GetOrCreateUser, user_repo=repos.user_repo)
    get_weather_now = providers.Factory(GetWeatherNow, weather_repo=repos.weather)
    get_weather_forecast = providers.Factory(GetWeatherForecast, weather_repo=repos.weather)

    mailing = providers.Factory(Mailing, bot=repos.bot_repo)
    bulk_mailing = providers.Factory(
        BulkMailing,
        user_repo=repos.user_repo,
        get_weather_forecast=get_weather_forecast,
        bot=repos.bot_repo,
    )

    # Parser
    parse_last_news = providers.Factory(
        ParseLastNews, parse_repo=repos.parse_news_repo, news_repo=repos.news_repo
    )
    parse_current_rate = providers.Factory(
        ParseCurrentRate,
        parse_rate_repo=repos.parse_rate_repo,
        rate_repo=repos.rate_repo,
    )

    # Handlers
    start_handler = providers.Factory(
        StartHandler, get_or_create_user=get_or_create_user, config=config.app
    )
    weather_handler = providers.Factory(
        WeatherHandler,
        get_weather_now=get_weather_now,
        get_or_create_user=get_or_create_user,
    )
    weather_by_day_handler = providers.Factory(
        WeatherByDayHandler,
        get_weather_forecast=get_weather_forecast,
        get_or_create_user=get_or_create_user,
    )
