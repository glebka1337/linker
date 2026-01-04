from typing import Protocol


class ModelServiceInterface(Protocol):
    
    async def vectorize(
        self,
        text: str
    ) -> list[float]: ...
    
    async def init_model(
        self
    ) -> None: ...
    