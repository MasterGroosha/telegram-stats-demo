from aioinflux import lineprotocol, MEASUREMENT, TIMEDT, TAG, INT
from typing import NamedTuple


@lineprotocol
class BotEvent(NamedTuple):
    measurement: MEASUREMENT
    timestamp: TIMEDT
    event_type: TAG
    stub: INT
