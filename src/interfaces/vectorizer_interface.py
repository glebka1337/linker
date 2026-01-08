from typing import (
    Protocol
)
from pydantic import BaseModel

class VectorizerInterface(Protocol):
    """
    Class responsible only for wrapping up a sending messages to queue
    """
    async def send_for_process(
        self,
        note_uuid: str
    ): ...