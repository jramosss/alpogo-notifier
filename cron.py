from datetime import datetime

from models.Event import Event
from models.Subscription import Subscription
from notifier import send_email


def notify():
    date = datetime.now()
    subscriptions = Subscription.select().where(Subscription.is_active).group_by(Subscription.user)
    for subscription in subscriptions:
        events = list(Event.select().where(Event.place == subscription.place, Event.date >= date, Event.stillPlacesLeft).order_by(Event.date).execute())
        if events:
            send_email([subscription.user.email], events)
        else:
            print(f"No events for {subscription.place.name}")

if __name__ == '__main__':
    notify()