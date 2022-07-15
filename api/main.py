from fastapi import FastAPI

from api.routers import image, ml

app = FastAPI()
app.include_router(image.router)
app.include_router(ml.router)

