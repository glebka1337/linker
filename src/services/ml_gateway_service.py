import logging
from typing import Type, TypeVar, Literal
from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)

class MLInfoResponse(BaseModel):
    dim: int 

class MLEmbeddingResponse(BaseModel):
    embedding: list[float]

class MLGatewayService:
    
    def __init__(self, client: AsyncClient):
        self.client = client
    
    async def close_client(self):
        await self.client.aclose()

    async def _execute_request(
        self, 
        method: Literal["GET", "POST"], 
        url: str, 
        response_model: Type[ModelType],
        json_payload: dict | None = None
    ) -> ModelType:
        
        try:
            resp = await self.client.request(method, url, json=json_payload)
            resp.raise_for_status()
            
            return response_model.model_validate(resp.json())
            
        except ValidationError as e:
            logger.critical(f"Contract broken at {url}: {e}")
            raise e
        except Exception as e:
            logger.critical(f"Network error at {url}: {e}")
            raise e

    async def get_dimension(self) -> int:
        response = await self._execute_request(
            method="GET",
            url="/info",
            response_model=MLInfoResponse
        )
        return response.dim
        
    async def vectorize(self, text: str) -> list[float]:
        response = await self._execute_request(
            method="POST",
            url="/encode",
            json_payload={"text": text},
            response_model=MLEmbeddingResponse
        )
        return response.embedding