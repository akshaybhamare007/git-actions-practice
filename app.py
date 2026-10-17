
from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from Cloud Run!",
        "environment": os.getenv("APP_ENV", "development")
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

