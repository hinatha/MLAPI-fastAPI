from pydantic import BaseModel, Field

class FileIdModel(BaseModel):
    file_id: str

class FileNameModel(BaseModel):
    filename: str

class ImageList(FileIdModel):
    filename: str = Field(None)
    
    class Config:
        orm_mode = True
