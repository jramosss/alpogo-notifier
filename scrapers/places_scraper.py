from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from scrapers.Scraper import Scraper
from utils.constants import ALPOGO_URL
from models.Place import Place


class PlacesScraper(Scraper):
    driver: webdriver.Chrome | None

    def __init__(self, pages_to_scrape = 3, time_to_wait = 0.5):
        self.driver = None
        self.pages_to_scrape = pages_to_scrape
        self.time_to_wait = time_to_wait
        super().__init__()

    def load_pages(self):
        for i in range(self.pages_to_scrape):
            self.driver.find_element(by=By.ID, value="cargar-eventos").click()
            sleep(self.time_to_wait)

    def get_place_id_from_href(self, href: str):
        return int(href.split('/')[-1])

    def find_places(self):
        places_elements = self.driver.find_elements(by=By.CLASS_NAME, value="lugar-link")
        places = []
        place_names = set()
        for place in places_elements:
            if not place.text:
                continue
            if place.text in place_names:
                continue
            places.append(
                Place(
                    name=place.text,
                    url=place.get_attribute('href'),
                    id=self.get_place_id_from_href(place.get_attribute('href')),
                    # TODO: enhance scraper to go into every place and extract image
                    image_url=""
                )
            )
            place_names.add(place.text)
        return places

    def scrape(self):
        self.driver.get(f"{ALPOGO_URL}")
        self.driver.implicitly_wait(self.time_to_wait)
        self.load_pages()
        return self.find_places()

    def setup(self):
        service = webdriver.ChromeService()
        self.driver = webdriver.Chrome(service=service)

    def teardown(self):
        self.driver.quit()
