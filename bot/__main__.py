import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.router import Router

from bot.analytics.client import AnalyticsClient
from bot.config_reader import Config, load_config
from bot.handlers.commands import register_commands
from bot.middlewares.log_updates import LogUpdatesMiddleware
from bot.ui_commands import set_ui_commands

logger = logging.getLogger(__name__)


async def main():
    config: Config = load_config()
    bot = Bot(config.bot.token, parse_mode="HTML")
    influx = AnalyticsClient(config.influxdb)

    ok, error = await influx.check()
    if not ok:
        print(f"Could not connect to InfluxDB instance: {error}")
        return

    # Создаём единственный роутер
    default_router = Router()

    # Подключаем мидлварь логирования
    default_router.message.outer_middleware(LogUpdatesMiddleware())

    # Регистрация хэндлеров
    register_commands(default_router)

    # Создаём диспетчер и подключаем к нему наш единственный роутер
    dp = Dispatcher()
    dp.include_router(default_router)

    # Установка команд в интерфейсе
    await set_ui_commands(bot)

    # Запускаем бота
    await dp.start_polling(bot, influx=influx)


if __name__ == "__main__":
    asyncio.run(main())
