from queue import Queue

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.router import Router

from bot.analytics import NamedEventPre


async def cmd_start(message: Message, objects_queue: Queue):
    """
    Хэндлер на команду /start
    :param message: сообщение, начинающееся с команды /start
    :param objects_queue: очередь, из которой потом объекты улетают в InfluxDB
    """
    await message.answer("Обработчик команды <code>/start</code>")
    objects_queue.put(NamedEventPre(event="Команда /start"))


async def cmd_help(message: Message, objects_queue: Queue):
    """
    Хэндлер на команду /help
    :param message: сообщение, начинающееся с команды /help
    :param objects_queue: очередь, из которой потом объекты улетают в InfluxDB
    """
    await message.answer("Обработчик команды <code>/help</code>")
    objects_queue.put(NamedEventPre(event="/help"))


async def cmd_button(message: Message, objects_queue: Queue):
    """
    Хэндлер на команду /help
    :param message: сообщение, начинающееся с команды /help
    :param objects_queue: очередь, из которой потом объекты улетают в InfluxDB
    """
    button = InlineKeyboardButton(text="Нажми меня", callback_data="press_me")
    await message.answer(
        "Нажми на кнопку, чтобы она исчезла",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]])
    )
    objects_queue.put(NamedEventPre(event="/button"))


def register_commands(router: Router):
    router.message.register(cmd_start, commands="start")
    router.message.register(cmd_help, commands="help")
    router.message.register(cmd_button, commands="button")
