from aioinflux import lineprotocol, MEASUREMENT, TIMEDT, TAG, INT
from typing import NamedTuple


# Объект логирования разных именованных событий
@lineprotocol
class BotEvent(NamedTuple):
    measurement: MEASUREMENT
    timestamp: TIMEDT
    event_type: TAG
    user_id: TAG
    stub: INT


# Объект логирования "сырого" апдейта
@lineprotocol
class BotRawUpdate(NamedTuple):
    measurement: MEASUREMENT
    timestamp: TIMEDT
    is_handled: TAG
    stub: INT
