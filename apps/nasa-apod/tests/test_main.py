import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_ready():
    assert client.get("/ready").json() == {"status": "ok"}


FAKE_APOD = {
    "date": "2026-07-20",
    "title": "A Test Nebula",
    "explanation": "Some explanation.",
    "url": "https://apod.nasa.gov/apod/image/test.jpg",
    "media_type": "image",
    "service_version": "v1",
}


def test_apod_missing_api_key(monkeypatch):
    monkeypatch.delenv("NASA_API_KEY", raising=False)

    response = client.get("/apod")

    assert response.status_code == 500


def test_apod_success(monkeypatch):
    monkeypatch.setenv("NASA_API_KEY", "test-key")

    def fake_get(url, params=None):
        return httpx.Response(200, json=FAKE_APOD, request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", fake_get)

    response = client.get("/apod")

    assert response.status_code == 200
    assert response.json()["title"] == "A Test Nebula"
