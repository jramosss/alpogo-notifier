from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from Event import Event
from scrapers.Scraper import Scraper
from utils.utils import parse_date


class EventScraper(Scraper):
    def __init__(self, place_id: int):
        self.place_id = place_id
        super().__init__()

    def get_html(self):
        # response = get(f"{MUSICA_A_CIEGAS_URL}/lugar/{self.place_id}")
        # return response.text
        with open('../mocks/all_events.html', 'r') as file:
            return file.read()

    def __get_events(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        row = soup.find('div', class_='row eventos')
        return row.find_all('div', class_='evento-container')

    def get_text_safely(self, element: Tag):
        if element:
            return element.text
        print(f'Failed to get text of element {element}')
        return ""

    def __parse_event(self, event: Tag):
        raw_name = event.find('h4', class_='nombre-artista').text
        raw_date = event.find('p', class_='fecha').text
        raw_url = event.find('a')['href']
        raw_location = event.find('a', class_='lugar-link').text
        image_url = event.find('img')['src']
        buttons = event.find('div', class_='botones')
        button = buttons.find('a', class_='btn')
        still_places_left = 'btn-agotado' not in button['class']
        price = button.text.split('$')[1].split(' ')[0] if still_places_left else 0

        return Event(
            name=raw_name,
            date=parse_date(raw_date),
            location=raw_location,
            url=raw_url,
            stillPlacesLeft=still_places_left,
            price=float(price),
            image_url=image_url
        )

    def parse_events(self, events:  ResultSet[Tag]):
        return [self.__parse_event(event) for event in events]

    def scrape(self):
        html = self.get_html()
        events = self.__get_events(html)
        return self.parse_events(events)