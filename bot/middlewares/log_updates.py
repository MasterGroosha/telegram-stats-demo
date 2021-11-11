import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram import BaseMiddleware

from bot.analytics.client import AnalyticsClient


class LogUpdatesMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        influx_client: AnalyticsClient = data.get("influx")

        # Выполнение хэндлера
        result = await handler(event, data)

        # Попытка извлечь отметку времени из некоторых апдейтов
        event_datetime = datetime.datetime.utcnow()
        if isinstance(event, Message):
            event_datetime = event.date
        elif isinstance(event, CallbackQuery) and event.message is not None:
            event_datetime = event.message.date

        # Логирование
        await influx_client.log_update(int(result is not UNHANDLED), event_datetime)

        # Необходимо вернуть результат выполнения хэндлера, иначе будет ошибка
        return result
