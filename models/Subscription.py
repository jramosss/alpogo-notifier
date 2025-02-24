from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField, PrimaryKeyField

from models.BaseModel import BaseModel
from models.Place import Place
from models.User import User


class Subscription(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, backref="subscriptions", on_delete="CASCADE")
    place = ForeignKeyField(Place, backref="subscriptions", on_delete="CASCADE")
    created_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    class Meta:
        indexes = (
            (("user", "place"), True),
        )


    def __str__(self):
        return f"Subscription for user {self.user.id} {self.user.email} - {self.place.name}"