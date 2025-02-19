from datetime import datetime
from dataclasses import dataclass


@dataclass
class Event:
    name: str
    date: datetime
    location: str
    price: float
    stillPlacesLeft: bool
    url: str
    image_url: str

    def to_html(self):
        return f"""
        <div class="event-container">
            <div class="event-title tooltip">
                {self.name if len(self.name) < 60 else self.name[:57] + '...'}
                <span class="tooltiptext">{self.name}</span>
            </div>
            <img src="{self.image_url}" alt="{self.name}" style="width: 300px; height: 300px; border-radius: 8px;">
            <div class="event-detail"><strong>Date:</strong> {self.date.strftime('%B %d, %Y, %H:%M')}</div>
            <div class="event-detail"><strong>Location:</strong> {self.location}</div>
            <div class="event-detail"><strong>Price:</strong> ${int(self.price)}</div>
            <a href="{self.url}" class="event-link">
                View Event
            </a>
        </div>
        """

    def __str__(self):
        return f'{self.name} - {self.date} - {self.location} - {self.price} - {self.stillPlacesLeft} - {self.url}'