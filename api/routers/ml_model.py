from fastapi import APIRouter

import api.schemas.ml_model as ml_model_schema

router = APIRouter()


# Send file_id and return the result of predicting photo.
@router.post("/probabilities/{file_id}", response_model=ml_model_schema.PredictResult)
async def probabilities(file_id: str):
    return ml_model_schema.PredictResult(
        file_id=file_id,
        observed_result=[1, 2, 3, 4],
        predicted_result=[1, 3, 3, 4],
        accuracy=0.75
        )
