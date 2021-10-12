from aiogram import types
from aiogram.dispatcher.router import Router
from bot.analytics.client import AnalyticsClient


async def cmd_start(message: types.Message, influx: AnalyticsClient):
    """
    Хэндлер на команду /start
    :param message: сообщение, начинающееся с команды /start
    :param influx: класс для работы с InfluxDB
    """
    await message.answer("Обработчик команды <code>/start</code>")
    await influx.log("/start", message.date)


async def cmd_help(message: types.Message, influx: AnalyticsClient):
    """
    Хэндлер на команду /help
    :param message: сообщение, начинающееся с команды /help
    :param influx: класс для работы с InfluxDB
    """
    await message.answer("Обработчик команды <code>/help</code>")
    await influx.log("/help", message.date)


def register_commands(router: Router):
    router.message.register(cmd_start, commands="start")
    router.message.register(cmd_help, commands="help")
