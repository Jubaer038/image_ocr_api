from fastapi import FastAPI
from app.api.v1.endpoints.compare_temp import router as compare_router

app = FastAPI(
    title="Image Data Extract & Compare API",
    description="Extract temperature text from image and compare with OpenWeather API",
    version="1.0"
)

app.include_router(compare_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Welcome to Image Data Extract & Compare API"}
