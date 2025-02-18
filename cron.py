from datetime import datetime
from Event import Event
from scraper import get_events
from notifier import send_email


def filter_events(events: list[Event], date: datetime):
    return [event for event in events if event.date >= date and event.stillPlacesLeft]


def sort_events(events: list[Event]):
    return sorted(events, key=lambda event: event.date)


def notify():
    date = datetime.now()
    events = get_events()
    events_to_send = sort_events(filter_events(events, date))
    if events_to_send:
        send_email(events_to_send)
    else:
        print('No events to notify')


if __name__ == '__main__':
    notify()