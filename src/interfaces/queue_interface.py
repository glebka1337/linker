# src/interfaces/queue_interface.py
from typing import (
    Protocol
)
import pydantic

class QueueInterface(Protocol):
    async def send_msg(
        self, msg: pydantic.BaseModel,
        queue_name: str
    ) -> None: ...