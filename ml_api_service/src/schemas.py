from pydantic import BaseModel, Field

class TextPayload(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)

class EmbeddingResponse(BaseModel):
    embedding: list[float]
    