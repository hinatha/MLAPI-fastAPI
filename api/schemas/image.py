from pydantic import BaseModel, Field

class ImageList(BaseModel):
    file_id: int
    filename: str = Field(None, example="0.jpg")
    
    class Config:
        orm_mode = True
