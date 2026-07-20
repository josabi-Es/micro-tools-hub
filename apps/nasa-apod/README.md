# nasa-apod

Returns NASA's Astronomy Picture of the Day (APOD)

## Setup

Get a free API key at https://api.nasa.gov, then:

```bash
cp .env.example .env   # fill NASA_API_KEY
```

## Run locally

```bash
uv sync
uv run --env-file .env uvicorn main:app --reload
```

Then: `curl http://localhost:8000/apod`

## Run with Docker

```bash
docker build -t nasa-apod .
docker run -p 8000:8000 nasa-apod
```
