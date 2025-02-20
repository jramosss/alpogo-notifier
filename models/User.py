from peewee import CharField, BooleanField, DateTimeField
from datetime import datetime

from models.BaseModel import BaseModel


class User(BaseModel):
    id = CharField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username
