from peewee import CharField, IntegerField

from models.BaseModel import BaseModel


class Place(BaseModel):
    name = CharField(unique=True)
    id = IntegerField()
    url = CharField()
    image_url = CharField(max_length=1024)

    def __str__(self):
        return f'{self.name}'