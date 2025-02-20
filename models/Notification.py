from datetime import datetime

from peewee import CharField, ForeignKeyField, DateTimeField, PrimaryKeyField

from models.BaseModel import BaseModel
from models.User import User


class Notification(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, backref='notifications')
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.user} - {self.created_at}'