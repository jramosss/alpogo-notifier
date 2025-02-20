from scrapers.places_scraper import PlacesScraper
from utils.database import db, setup_database
from models.Place import Place

setup_database()

def cron():
    places = PlacesScraper().scrape()
    with db.atomic():
        Place.bulk_create(places)


if __name__ == "__main__":
    cron()