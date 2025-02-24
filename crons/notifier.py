from datetime import datetime

from models.Event import Event
from models.Subscription import Subscription
from services.notifier import Notifier


def get_subscriptions():
    return (
        Subscription.select().where(Subscription.is_active).group_by(Subscription.user)
    )


def get_events(subscription) -> list[Event]:
    date = datetime.now()
    return list(
        Event.select()
        .where(
            Event.place == subscription.place, Event.date >= date, Event.stillPlacesLeft
        )
        .order_by(Event.date)
        .execute()
    )


def notify():
    subscriptions = get_subscriptions()
    for subscription in subscriptions:
        events = get_events(subscription)
        if events:
            Notifier.notify(subscription.user, events)
        else:
            print(f"No events for {subscription.place.name}")


if __name__ == "__main__":
    notify()
