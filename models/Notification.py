from datetime import datetime

from peewee import CharField, ForeignKeyField, DateTimeField

from models.BaseModel import BaseModel
from models.User import User


class Notification(BaseModel):
    id = CharField(primary_key=True)
    user = ForeignKeyField(User, backref='notifications')
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.user} - {self.created_at}'