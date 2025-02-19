from datetime import datetime
from models.Event import Event
from scrapers.event_scraper import EventScraper
from notifier import send_email


def filter_events(events: list[Event], date: datetime):
    return [event for event in events if event.date >= date and event.stillPlacesLeft]


def sort_events(events: list[Event]):
    return sorted(events, key=lambda event: event.date)


def notify():
    date = datetime.now()
    events = EventScraper().scrape()
    events_to_send = sort_events(filter_events(events, date))
    if events_to_send:
        send_email(events_to_send)
    else:
        print('No events to notify')


if __name__ == '__main__':
    notify()