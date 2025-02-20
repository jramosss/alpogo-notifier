from typing import Annotated

from fastapi import APIRouter, Depends

from models.Place import Place
from models.Subscription import Subscription
from models.User import User
from services.auth import get_current_user

router = APIRouter()


@router.get("/all")
async def get_all_subscriptions_for_user(user: Annotated[User, Depends(get_current_user)]):
    return {"subscriptions": [subscription.place.name for subscription in user.subscriptions]}


@router.post("/{place_id}")
async def subscribe_to_place(place_id: int, user: Annotated[User, Depends(get_current_user)]):
    place = Place.select().where(Place.id == place_id).get()
    Subscription.create(user=user, place=place)
    return {"message": f"Subscribed to place {place.name} successfully"}