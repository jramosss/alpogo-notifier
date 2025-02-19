from peewee import Model
from utils.database import db


class BaseModel(Model):
    class Meta:
        database = db