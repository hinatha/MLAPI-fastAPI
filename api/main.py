from fastapi import FastAPI

from api.routers import image, ml_model

app = FastAPI()
app.include_router(image.router)
app.include_router(ml_model.router)
