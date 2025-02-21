from concurrent.futures.thread import ThreadPoolExecutor

from peewee import IntegrityError

from scrapers.places_scraper import PlacesScraper
from utils.database import db, setup_database
from models.Place import Place

setup_database()
db.create_tables([Place])

def create_or_update_image(place: Place):
    try:
        Place.create(
            name=place.name,
            url=place.url,
            id=place.id,
            image_url=place.image_url
        )
    except IntegrityError:
        if place.image_url:
            return
        existing_place = Place.get(Place.id == place.id)
        existing_place.image_url = place.image_url
        existing_place.save()

def cron():
    places = PlacesScraper(pages_to_scrape=5).scrape()
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(
            executor.map(
                create_or_update_image, places
            )
        )

if __name__ == "__main__":
    cron()