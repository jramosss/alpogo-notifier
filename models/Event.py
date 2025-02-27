from datetime import datetime

from peewee import (
    CharField,
    DateField,
    FloatField,
    BooleanField,
    DateTimeField,
    PrimaryKeyField,
    ForeignKeyField,
)

from models.BaseModel import BaseModel
from models.Place import Place


class Event(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    date = DateField()
    location = CharField()
    price = FloatField()
    stillPlacesLeft = BooleanField()
    url = CharField()
    place = ForeignKeyField(Place, backref="events")
    image_url = CharField(max_length=1024)
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        indexes = ((("name", "date"), True),)

    def to_html(self):
        return f"""
        <div class="event-container">
            <div class="event-title tooltip">
                {self.name if len(self.name) < 60 else self.name[:57] + "..."}
                <span class="tooltiptext">{self.name}</span>
            </div>
            <img src="{self.image_url}" alt="{self.name}" style="width: 300px; height: 300px; border-radius: 8px;">
            <div class="event-detail"><strong>Date:</strong> {self.date.strftime("%B %d, %Y, %H:%M")}</div>
            <div class="event-detail"><strong>Location:</strong> {self.location}</div>
            <div class="event-detail"><strong>Price:</strong> ${int(self.price)}</div>
            <a href="{self.url}" class="event-link">
                View Event
            </a>
        </div>
        """

    def __str__(self):
        return f"{self.id} - {self.name} - {self.date} - {self.location} - {self.price} - {self.stillPlacesLeft} - {self.url}"
