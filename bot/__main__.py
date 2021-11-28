import asyncio
import logging
from queue import Queue

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.router import Router

from bot.analytics import InfluxAnalyticsClient
from bot.config_reader import Config, load_config
from bot.handlers.callbacks import register_callbacks
from bot.handlers.commands import register_commands
from bot.middlewares.log_updates import LogUpdatesMiddleware
from bot.ui_commands import set_ui_commands


async def main():
    logging.basicConfig(level=logging.INFO)
    config: Config = load_config()
    bot = Bot(config.bot.token, parse_mode="HTML")

    # Объект очереди событий
    objects_queue = Queue()

    influx = InfluxAnalyticsClient(
        url=config.influxdb.host, token=config.influxdb.token, org=config.influxdb.org, objects_queue=objects_queue
    )
    if not influx.healthcheck():
        raise ChildProcessError

    # Запуск процесса обработки очереди событий
    influx.start()

    # Создаём единственный роутер
    default_router = Router()

    # Подключаем мидлварь логирования
    default_router.message.outer_middleware(LogUpdatesMiddleware())
    default_router.callback_query.outer_middleware(LogUpdatesMiddleware())

    # Регистрация хэндлеров
    register_commands(default_router)
    register_callbacks(default_router)

    # Создаём диспетчер и подключаем к нему наш единственный роутер
    dp = Dispatcher()
    dp.include_router(default_router)

    # Установка команд в интерфейсе
    await set_ui_commands(bot)

    # Запускаем бота
    try:
        await dp.start_polling(bot, objects_queue=objects_queue, allowed_updates=dp.resolve_used_update_types())
    except:
        influx.stopflag.set()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped gracefully")
