from enum import Enum
from aioinflux import InfluxDBClient, InfluxDBWriteError
from datetime import datetime
import logging


class DBParams:
    STATS_DB   = None
    STATS_HOST = None
    STATS_USER = None
    STATS_PASS = None


class EventCommand(Enum):
    START = "/start"
    RESTART = "/restart"
    STOP = "/stop"
    PING = "/ping"
    HELP = "/help"


async def log(user_id: int, event: EventCommand):
    data = {
        "measurement": "bot_commands",
        "time": datetime.utcnow(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "command": event.value
        }
    }
    try:
        async with InfluxDBClient(host=DBParams.STATS_HOST, db=DBParams.STATS_DB,
                                  username=DBParams.STATS_USER, password=DBParams.STATS_PASS) as client:
            await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f"InfluxDB write error: {str(ex)}")
