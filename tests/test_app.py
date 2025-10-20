from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_register_and_login():
    email = "a@a.com"
    pwd = "Minimo123!"
    r = client.post("/auth/register", json={"email": email, "password": pwd})
    assert r.status_code in (201, 409)
    r = client.post("/auth/login", json={"email": email, "password": pwd})
    assert r.status_code == 200
    assert "token" in r.json()
