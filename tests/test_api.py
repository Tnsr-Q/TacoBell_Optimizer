## tests/test_api.py

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
