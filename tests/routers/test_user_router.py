import pytest
from fastapi.testclient import TestClient
from app import app
from models.User import User

@pytest.fixture
def client():
    """Returns a FastAPI test client."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    User.delete().execute()

def test_register_user(client):
    response = client.post("/user/register/", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created"}

def test_register_existing_user(client):
    client.post("/user/register/", json={"email": "test@example.com", "password": "testpassword"})
    response = client.post("/user/register/", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_login_success(client):
    client.post("/user/register/", json={"email": "test@example.com", "password": "testpassword"})
    response = client.post("/user/login/", params={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    client.post("/user/register/", json={"email": "test@example.com", "password": "testpassword"})
    response = client.post("/user/login/", params={"email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_nonexistent_user(client):
    response = client.post("/user/login/", params={"email": "nouser@example.com", "password": "testpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}