from pydantic import BaseModel, Field

class PredictResult(BaseModel):
    file_id: str
    observed_result: list = Field(None, example=[1, 2, 3, 4])
    predicted_result: list = Field(None, example=[1, 3, 3, 4])
    accuracy: float = Field(None, example=0.75)
    