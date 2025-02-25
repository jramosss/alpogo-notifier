from peewee import CharField, PrimaryKeyField

from models.BaseModel import BaseModel


class Place(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    url = CharField()
    location = CharField(null=True)
    image_url = CharField(max_length=1024, null=True)

    def __str__(self):
        return f"{self.name}"
