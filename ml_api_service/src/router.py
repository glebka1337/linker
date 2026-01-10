import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from ml_api_service.src.ml_service import MLService, get_ml_service
from ml_api_service.src.schemas import TextPayload, EmbeddingResponse

rt = APIRouter(tags=['main',  'ml_service'])

logger = logging.getLogger(__name__)

@rt.post(
    '/encode',
    response_model=EmbeddingResponse
)
async def encode(
    text_data: TextPayload,
    ml_service: Annotated[MLService, Depends(get_ml_service)]
):
    try:
        embedding = await ml_service.vectorize(
            text=text_data.text
        )
        
        return EmbeddingResponse(
            embedding=embedding
        )
        
    except Exception as e:
        logger.critical(f"Something went wrong {e}")
        
        raise HTTPException(
            detail="Something went wrong, please try again latter",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@rt.get(
    '/info',
)
async def info(
    ml_service: Annotated[MLService, Depends(get_ml_service)]
):
    if not ml_service.model:
        raise HTTPException(
            detail="Model loading",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return {
        "model_name": ml_service.model_name,
        "dim": ml_service.model.get_sentence_embedding_dimension()
    }