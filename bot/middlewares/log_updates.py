import datetime
from queue import Queue
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.analytics import RawUpdatePre


class LogUpdatesMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        objects_queue: Queue = data.get("objects_queue")

        # Выполнение хэндлера
        result = await handler(event, data)

        # Попытка извлечь отметку времени из некоторых апдейтов
        event_datetime = datetime.datetime.utcnow()
        if isinstance(event, Message):
            event_datetime = event.date
        elif isinstance(event, CallbackQuery) and event.message is not None:
            event_datetime = event.message.date

        # Логирование
        objects_queue.put(RawUpdatePre(is_handled=result is not UNHANDLED))

        # Необходимо вернуть результат выполнения хэндлера, иначе будет ошибка
        return result
