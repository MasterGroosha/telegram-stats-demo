from dataclasses import dataclass
from os import getenv


@dataclass
class TgBot:
    token: str


@dataclass
class InfluxDB:
    host: str
    db: str
    user: str
    password: str


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
            host=getenv("DB_HOST"),
            db=getenv("INFLUXDB_DB"),
            user=getenv("INFLUXDB_WRITE_USER"),
            password=getenv("INFLUXDB_WRITE_USER_PASSWORD"),
        )
    )
