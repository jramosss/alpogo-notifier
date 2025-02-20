from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField

from models.BaseModel import BaseModel
from models.Place import Place
from models.User import User


class Subscription(BaseModel):
    user = ForeignKeyField(User, backref="subscriptions", on_delete="CASCADE")
    place = ForeignKeyField(Place, backref="subscriptions", on_delete="CASCADE")
    created_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    def __str__(self):
        return f"{self.user.id} - {self.event_id}"