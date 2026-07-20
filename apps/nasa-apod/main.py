import os

import httpx
from fastapi import FastAPI, HTTPException
from models.apod import ApodResponse

app = FastAPI(title="nasa-apod")

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/apod", response_model=ApodResponse)
def apod() -> ApodResponse:
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="NASA_API_KEY is not set")

    response = httpx.get(NASA_APOD_URL, params={"api_key": api_key})
    response.raise_for_status()
    return ApodResponse.model_validate(response.json())
