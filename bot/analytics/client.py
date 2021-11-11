from datetime import datetime
from typing import Tuple, Optional

from aiogram.types import Message
from aiohttp.client_exceptions import ClientConnectorError
from aioinflux import InfluxDBClient
from bot.config_reader import InfluxDB
from bot.analytics.objects import BotEvent, BotRawUpdate


class AnalyticsClient:
    def __init__(self, influx_config: InfluxDB):
        self.client = InfluxDBClient(
            host=influx_config.host,
            username=influx_config.user,
            password=influx_config.password,
            database=influx_config.db
        )

    async def check(self) -> Tuple[bool, Optional[str]]:
        try:
            await self.client.ping()
            return True, None
        except ClientConnectorError as ex:
            return False, str(ex)

    async def __log_event(self, event, retention_policy):
        """
        Общий метод логирования какого-либо события

        :param event: объект события
        :param retention_policy: в какую Retention Policy (условно: таблицу) писать
        """
        try:
            await self.client.write(event, rp=retention_policy)
        except Exception as ex:
            print(type(ex), str(ex))

    async def log_message(self, event_type: str, message: Message):
        """
        Логирование обычных сообщений (Message)

        :param event_type: текстовая отметка-маркер
        :param message: объект сообщения в Telegram
        """
        event = BotEvent(
            measurement="events",
            timestamp=message.date,
            event_type=event_type,
            user_id=str(message.from_user.id),
            stub=1
        )
        await self.__log_event(event, "one_month")

    async def log_update(self, is_handled: int, event_datetime: datetime):
        """
        Логирование любого апдейта

        :param is_handled: 0, если апдейт не был обработан, и 1, если обработан
        :param event_datetime: дата и время, указанные в апдейте (или utcnow())
        """
        event = BotRawUpdate(
            measurement="updates",
            timestamp=event_datetime,
            is_handled=str(is_handled),
            stub=1
        )
        await self.__log_event(event, "updates_7d")
