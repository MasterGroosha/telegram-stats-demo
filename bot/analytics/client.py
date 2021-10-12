from datetime import datetime
from typing import Tuple, Optional

from aiohttp.client_exceptions import ClientConnectorError
from aioinflux import InfluxDBClient
from bot.config_reader import InfluxDB
from bot.analytics.objects import BotEvent


class AnalyticsClient:
    def __init__(self, influx_config: InfluxDB):
        self.client = InfluxDBClient(
            host=influx_config.host, username=influx_config.user, password=influx_config.password,
            database=influx_config.db
        )

    async def check(self) -> Tuple[bool, Optional[str]]:
        try:
            await self.client.ping()
            return True, None
        except ClientConnectorError as ex:
            return False, str(ex)

    async def log(self, event_type: str, event_datetime: datetime):
        event = BotEvent(
            measurement="events",
            timestamp=event_datetime,
            event_type=event_type,
            stub=1
        )
        try:
            await self.client.write(event)
        except Exception as ex:
            print(type(ex), str(ex))
