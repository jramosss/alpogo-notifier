import pytest
from models.Place import Place
from models.Subscription import Subscription
from models.User import User
from services.auth import create_access_token
from mixer.backend.peewee import mixer


@pytest.fixture
def test_user():
    email = "test@example.com"
    if User.select().where(User.email == email).exists():
        u = User.get(User.email == email)
        if Subscription.select().where(Subscription.user == u).exists():
            Subscription.delete().where(Subscription.user == u).execute()
        u.delete_instance()
    return User.create_user(email=email, password="hashedpassword")

@pytest.fixture
def test_place():
    """Creates and returns a test place."""
    return mixer.blend(Place)

@pytest.fixture
def auth_token(test_user):
    """Generates an authentication token for the test user."""
    return create_access_token(test_user)