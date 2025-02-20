from fastapi import APIRouter

from models.Place import Place
from models.Subscription import Subscription
from models.User import User

router = APIRouter()


@router.get("/all")
async def get_all_subscriptions_for_user():
    # todo get this user_id from cookies
    user_email = 'test@test.com'
    user = User.select().where(User.email == user_email).get()
    return {"subscriptions": [subscription.place.name for subscription in user.subscriptions]}


@router.post("/{place_id}")
async def subscribe_to_place(place_id: int):
    # todo get this user_id from cookies
    user_email = 'test@test.com'
    user: User = User.select().where(User.email == user_email).get()
    place = Place.select().where(Place.id == place_id).get()
    Subscription.create(user=user, place=place)
    return {"message": f"Subscribed to place {place.name} successfully"}