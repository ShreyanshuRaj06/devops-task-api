import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert data["count"] >= 2


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Verify CI Pipeline"})
    assert response.status_code == 201
    created = response.get_json()
    assert created["title"] == "Verify CI Pipeline"
    assert created["done"] is False