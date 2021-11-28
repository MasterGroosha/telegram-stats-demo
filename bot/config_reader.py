from dataclasses import dataclass
from os import getenv


@dataclass
class TgBot:
    token: str


@dataclass
class InfluxDB:
    host: str
    org: str
    token: str


@dataclass
class Config:
    bot: TgBot
    influxdb: InfluxDB


def load_config():
    return Config(
        bot=TgBot(
            token=getenv("BOT_TOKEN"),
        ),
        influxdb=InfluxDB(
            host=getenv("INFLUXDB_HOST"),
            org=getenv("INFLUXDB_ORG"),
            token=getenv("INFLUXDB_TOKEN"),
        )
    )
