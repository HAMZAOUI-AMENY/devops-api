from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, DevOps!"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_sum():
    response = client.get("/sum?a=3&b=5")
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_create_item():
    response = client.post("/items/", json={"name":"Test","price":10})
    assert response.status_code == 200
    assert "total_price" in response.json()
