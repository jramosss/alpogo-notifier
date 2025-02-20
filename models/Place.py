from peewee import CharField, IntegerField, PrimaryKeyField

from models.BaseModel import BaseModel


class Place(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    url = CharField()
    image_url = CharField(max_length=1024)

    def __str__(self):
        return f'{self.name}'