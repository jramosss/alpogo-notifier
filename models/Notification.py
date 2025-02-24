from datetime import datetime

from peewee import ForeignKeyField, DateTimeField, PrimaryKeyField, CharField

from models.BaseModel import BaseModel
from models.Event import Event
from models.User import User


class Notification(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, backref="notifications")
    error = CharField(null=True)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.user} - {self.created_at}"
