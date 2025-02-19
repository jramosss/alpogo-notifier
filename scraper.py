import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

from requests import get
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from Event import Event
from utils import parse_date, get_disk_name_from_image

ALPOGO_URL = 'https://alpogo.com'
MUSICA_A_CIEGAS_URL = f'{ALPOGO_URL}/lugar/1253'

def get_html():
    response = get(MUSICA_A_CIEGAS_URL)
    return response.text


def __get_events(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find('div', class_='row eventos')
    return row.find_all('div', class_='evento-container')


def get_text_safely(element: Tag):
    if element:
        return element.text
    print(f'Failed to get text of element {element}')
    return ""


def __parse_event(event: Tag):
    raw_name = event.find('h4', class_='nombre-artista').text
    if not raw_name or not raw_name.startswith('Musica a Ciegas'):
        return
    raw_date = event.find('p', class_='fecha').text
    raw_url = event.find('a')['href']
    raw_location = event.find('a', class_='lugar-link').text
    image_url = event.find('img')['src']
    disk_name = get_disk_name_from_image(image_url)
    buttons = event.find('div', class_='botones')
    button = buttons.find('a', class_='btn')
    still_places_left = 'btn-agotado' not in button['class']
    price = button.text.split('$')[1].split(' ')[0] if still_places_left else 0
    return Event(
        name=raw_name.replace('Musica a Ciegas - ', ''),
        date=parse_date(raw_date),
        location=raw_location,
        url=raw_url,
        stillPlacesLeft=still_places_left,
        price=float(price),
        image_url=image_url,
        disk_name=disk_name
    )


def parse_events(events:  ResultSet[Tag]):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(__parse_event, events))


def get_events():
    html = get_html()
    events = __get_events(html)
    return parse_events(events)