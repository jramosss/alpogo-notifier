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
    disk_name: str

    def to_html(self):
        availability_class = "available" if self.stillPlacesLeft else "unavailable"
        availability_text = "Places Available" if self.stillPlacesLeft else "Sold Out"

        return f"""
        <div class="event-container">
            <div class="event-title">{self.name}</div>
            <img src="{self.image_url}" alt="{self.name}" style="width: 100%; border-radius: 8px;">
            <div class="event-detail"><strong>Disk Name:</strong> {self.disk_name}</div>
            <div class="event-detail"><strong>Date:</strong> {self.date.strftime('%B %d, %Y, %H:%M')}</div>
            <div class="event-detail"><strong>Location:</strong> {self.location}</div>
            <div class="event-detail"><strong>Price:</strong> ${self.price}</div>
            <div class="event-detail">
                <strong>Availability:</strong>
                <span class="{availability_class}">{availability_text}</span>
            </div>
            <a href="{self.url}" class="event-link">
                View Event
            </a>
        </div>
        """

    def __str__(self):
        return f'{self.name} - {self.date} - {self.location} - {self.price} - {self.stillPlacesLeft} - {self.url}'