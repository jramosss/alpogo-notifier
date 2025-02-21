from concurrent.futures.thread import ThreadPoolExecutor
from traceback import print_tb

from fastapi_utilities import repeat_every
from peewee import IntegrityError

from models.Place import Place
from models.Event import Event
from scrapers.event_scraper import EventScraper
from utils.database import setup_database, db

setup_database()
db.create_tables([Place, Event])


def scrape_events_from_place(place: Place):
    events_scraper = EventScraper(place.id)
    try:
        place_events = events_scraper.scrape()
        return place_events
    except Exception as e:
        print(f"Failed to scrape {place.id}", e)
        print_tb(e.__traceback__)
        return []

# @repeat_every(seconds=86400)
def cron():
    places_query = Place.select(Place.id).where(Place.url.is_null(False))
    places = list(places_query.execute())
    with ThreadPoolExecutor(max_workers=10) as executor:
        events = list(
            executor.map(
                scrape_events_from_place, places
            )
        )

    events = [event for place_events in events for event in place_events]

    for event in events:
        try:
            event.save()
        except IntegrityError as e:
            print(f"Duplicated event {event}", e)
            print_tb(e.__traceback__)


if __name__ == "__main__":
    cron()