# {{cookiecutter.app_name}}

{{cookiecutter.description}}

## Run locally

```bash
uv sync
uv run uvicorn main:app --reload
```

## Run with Docker

```bash
docker build -t {{cookiecutter.app_name}} .
docker run -p 8000:8000 {{cookiecutter.app_name}}
```
