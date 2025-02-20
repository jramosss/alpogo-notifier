from peewee import CharField, BooleanField, DateTimeField, PrimaryKeyField
from datetime import datetime
import bcrypt

from models.BaseModel import BaseModel


class User(BaseModel):
    id: str = PrimaryKeyField()
    password_hash: str = CharField()
    email: str = CharField(unique=True)
    is_active: bool = BooleanField(default=True)
    is_admin: bool = BooleanField(default=False)
    created_at: datetime = DateTimeField(default=datetime.now)
    deleted_at: datetime = DateTimeField(null=True)

    @staticmethod
    def create_user(email: str, password: str):
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return User.create(email=email, password_hash=hashed_pw)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def __str__(self):
        return self.email
