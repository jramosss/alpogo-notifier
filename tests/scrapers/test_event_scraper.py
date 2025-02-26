from datetime import datetime
from scrapers.event_scraper import EventScraper


def test_scrape_all_events(mocker):
    with open("mocks/all_events.html", "r") as file:
        mocker.patch(
            "scrapers.event_scraper.EventScraper.get_html", return_value=file.read()
        )
    scraper = EventScraper(1)
    events = scraper.scrape()
    assert len(events) == 12

    first_event = events[0]
    assert first_event.name == "Festi Surfer Rosas"
    assert first_event.stillPlacesLeft
    assert first_event.date == datetime(2025, 2, 18, 00, 1)
    assert int(first_event.price) == 5000
    assert (
        first_event.image_url
        == "https://imagenes.alpogo.com/eventos/alta_evento_1739829950_67b3b2be91753.jpg"
    )
    assert first_event.url == "https://alpogo.com/evento/festi-surfer-rosas-18766"


def test_scrape_casa_astral(mocker):
    with open("mocks/casa_astral.html", "r") as file:
        mocker.patch(
            "scrapers.event_scraper.EventScraper.get_html", return_value=file.read()
        )
    scraper = EventScraper(1)
    events = scraper.scrape()
    assert len(events) == 17

    first_event = events[0]
    assert first_event.name == "Musica a Ciegas - Led Zeppelin"
    assert first_event.stillPlacesLeft
    assert first_event.date == datetime(2025, 2, 21, 21, 30)
    assert int(first_event.price) == 8500
    assert (
        first_event.image_url == "https://imagenes.alpogo.com/eventos/21LEDZEPPELIN.png"
    )
    assert (
        first_event.url
        == "https://alpogo.com/evento/musica-a-ciegas-led-zeppelin-18382"
    )

    pink_floyd = events[6]

    assert pink_floyd.name == "Musica a Ciegas - Pink Floyd"
    assert not pink_floyd.stillPlacesLeft
