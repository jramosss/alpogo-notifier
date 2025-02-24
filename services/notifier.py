from models.Event import Event
from models.Notification import Notification
from models.NotificationEvent import NotificationEvent
from utils.email import EmailUtils
from models.User import User


class Notifier:
    @staticmethod
    def notify(user: User, events: list[Event]):
        notification_data = {"user": user}
        try:
            EmailUtils().send_email([user.email], events)
        except Exception as e:
            notification_data["error"] = str(e)
        finally:
            notification = Notification.create(**notification_data)
            NotificationEvent.bulk_create(
                [
                    NotificationEvent(notification=notification, event=event)
                    for event in events
                ]
            )
