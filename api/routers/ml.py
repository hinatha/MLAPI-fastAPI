from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
import api.schemas.ml as ml_schema
from api.predictions import calculation

router = APIRouter()


# Send file_id and return the result of predicting photo.
@router.get("/probabilities/{file_id}", response_model=ml_schema.PredictResult)
async def probabilities(file_id: str, db: AsyncSession = Depends(get_db)):
    return await calculation.evaluate_probs(file_id, db)
