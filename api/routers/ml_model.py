from fastapi import APIRouter

router = APIRouter()


# Send file_id and return the result of predicting photo.
@router.post("/probabilities")
async def probabilities():
    pass
