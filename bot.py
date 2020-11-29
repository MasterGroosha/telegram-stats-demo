import logging
from os import getenv
from sys import exit, stderr
from cachetools import TTLCache
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from analytics import log, EventCommand, DBParams

# Токен берётся из переменной окружения (можно задать через systemd unit или docker-compose)
token = getenv("BOT_TOKEN")
if not token:
    exit("Error: no token provided")

# Инициализация объектов бота, хранилища в памяти, логера и кэша (для троттлинга)
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
cache = TTLCache(maxsize=float('inf'), ttl=0.5)


# Мидлварь для тротлинга. Игнорирует любые повторные запросы в течение 0.5 сек
class ThrottleMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if not cache.get(message.chat.id):  # Предполагается, что бот НЕ работает в группах
            cache[message.chat.id] = True  # Записи в кэше нет, создаём
            return
        else:  # Пропускаем обработку
            raise CancelHandler


dp.middleware.setup(ThrottleMiddleware())


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Обработчик команды /start")
    await log(message.from_user.id, EventCommand.START)


@dp.message_handler(commands="stop")
async def cmd_stop(message: types.Message):
    await message.answer("Обработчик команды /stop")
    await log(message.from_user.id, EventCommand.STOP)


@dp.message_handler(commands="help")
async def cmd_help(message: types.Message):
    await message.answer("Обработчик команды /help")
    await log(message.from_user.id, EventCommand.HELP)


@dp.message_handler(commands="ping")
async def cmd_ping(message: types.Message):
    await message.answer("Обработчик команды /ping")
    await log(message.from_user.id, EventCommand.PING)


async def set_commands():
    commands = [
        types.BotCommand(command=cmd, description=f"Команда /{cmd}") for cmd in ("start", "stop", "help", "ping")
    ]
    await bot.set_my_commands(commands)


async def check_before_start(dp: Dispatcher):
    await set_commands()

    # Это переменные окружения
    for envvar in ("STATS_DB", "STATS_HOST", "STATS_USER", "STATS_PASS"):
        if not getenv(envvar):
            print(f'Error: missing "{envvar}" environment variable', file=stderr)
            exit(1)
        setattr(DBParams, envvar, getenv(envvar))

    # TODO: надо как-то проверить, что InfluxDB вообще жив.
    # client = InfluxDBClient(host=getenv("STATS_HOST"))
    # ping = await client.ping()
    # logging.info(f"PING: {ping}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=check_before_start)
