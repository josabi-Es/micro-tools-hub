def test_protected_endpoint_without_key(client, monkeypatch):
    monkeypatch.setenv("API_KEY", "correct-key")
    response = client.get("/database")
    assert response.status_code == 401


def test_protected_endpoint_with_wrong_key(client, monkeypatch):
    monkeypatch.setenv("API_KEY", "correct-key")
    response = client.get("/database", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
