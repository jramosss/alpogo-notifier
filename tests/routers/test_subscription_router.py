import pytest
from fastapi.testclient import TestClient
from app import app
from models.Place import Place
from services.auth import create_access_token
from mixer.backend.peewee import mixer

client = TestClient(app)


@pytest.fixture
def place():
    return mixer.blend(Place, image_url="https://example.com/image.jpg")


@pytest.fixture
def auth_token(test_user):
    return create_access_token(test_user)


def test_get_subscriptions_no_subscriptions(auth_token):
    """Test getting subscriptions when user has none."""
    response = client.get(
        "/subscription/all", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"subscriptions": []}


def test_subscribe_to_place(auth_token, place):
    """Test subscribing to a place."""

    response = client.post(
        f"/subscription/{place.id}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Subscribed to place {place.name} successfully"
    }


def test_get_subscriptions_after_subscribing(auth_token, place):
    """Test that a user sees their subscription after subscribing."""
    client.post(
        f"/subscription/{place.id}", headers={"Authorization": f"Bearer {auth_token}"}
    )

    response = client.get(
        "/subscription/all", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"subscriptions": [place.__dict__["__data__"]]}


def test_subscribe_to_nonexistent_place(auth_token):
    response = client.post(
        "/subscription/999", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert (
        response.status_code == 404
    )  # Assuming Peewee raises `DoesNotExist` for missing places


def test_get_subscriptions_unauthenticated():
    """Test accessing subscriptions without authentication."""
    response = client.get("/subscription/all")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_subscribe_unauthenticated(place):
    """Test subscribing without authentication."""
    response = client.post(f"/subscription/{place.id}")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
