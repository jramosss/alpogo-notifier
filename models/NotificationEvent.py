from peewee import ForeignKeyField
from models.Notification import Notification
from models.Event import Event

from models.BaseModel import BaseModel


class NotificationEvent(BaseModel):
    notification = ForeignKeyField(Notification, backref="notification_events")
    event = ForeignKeyField(Event, backref="event_notifications")
