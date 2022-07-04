from typing import List

from fastapi import APIRouter, UploadFile, File

import api.schemas.image as image_schema

router = APIRouter()

# Show list of image id and images names
@router.get("/images", response_model=List[image_schema.ImageList])
async def list_images():
    return [image_schema.ImageList(file_id=1, filename="0.jpg")]

# Save picture file to S3 and filename to DB and return file_id.
@router.post("/images", response_model=image_schema.ImageList)
async def upload_images(file: UploadFile = File(...)):
    return image_schema.ImageList(file_id=1, filename=file.filename)
