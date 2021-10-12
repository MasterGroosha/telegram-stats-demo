import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.router import Router

from bot.analytics.client import AnalyticsClient
from bot.config_reader import Config, load_config
from bot.handlers.commands import register_commands
# from bot.handlers.forwarded_messages import register_forwards
# from bot.handlers.add_or_migrate import register_add_or_migrate
# from bot.handlers.inline_mode import register_inline
# from bot.handlers.errors import register_errors
# from bot.ui_commands import set_bot_commands

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

    # Регистрация хэндлеров
    register_commands(default_router)
    # register_forwards(default_router)
    # register_add_or_migrate(default_router)
    # register_inline(default_router)
    # register_errors(default_router)

    # Создаём диспетчер и подключаем к нему наш единственный роутер
    dp = Dispatcher()
    dp.include_router(default_router)

    # Set bot commands in UI
    # await set_bot_commands(bot)

    # Запускаем бота
    await dp.start_polling(bot, influx=influx)


if __name__ == "__main__":
    asyncio.run(main())
