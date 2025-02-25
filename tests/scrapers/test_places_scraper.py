from scrapers.places_scraper import PlacesScraper
from pathlib import Path
from selenium.webdriver.chrome.options import Options as DriverOptions


def test_places_scraper(mocker):
    options = DriverOptions()
    options.add_argument("--headless=new")
    scraper = PlacesScraper(
        pages_to_scrape=5, driver_options=options, time_to_wait=0.05
    )
    mocker.patch.object(scraper, "get_page")
    mock_html_path = (
        Path(__file__).resolve().parent.parent.parent
        / "mocks"
        / "alpogo_interactive.html"
    )
    scraper.driver.get(f"file:///{mock_html_path}")
    places = scraper.scrape()
    expected_places = [
        "1915 eventos",
        "berta circuito de pruebas",
        "black sheep",
        "casa astral",
        "casa babylon",
        "casa pulsar",
        "cc bula",
        "club la falda",
        "club legrand",
        "club paraguay guemes",
        "club resistencia",
        "club v",
        "comuna club",
        "crucero arquimides",
        "la barra boliche",
        "la cúpula",
        "la minerita",
        "liverpool club",
        "macanudo bar",
        "medio tono club de música",
        "mística.qtp",
        "pez volcán",
        "polideportivo el rodeo",
        "predio artesanos",
        "pétalos de sol",
        "regio",
        "sala formosa",
        "salon pueyrredon",
        "studio theater",
        "teatro edén hotel",
        "teatro maria castaña",
        "uniclub",
        "zebra club",
        "zen disco",
    ]
    assert sorted([place.name.lower() for place in places]) == sorted(expected_places)
    casa_astral = [place for place in places if place.name == "Casa Astral"][0]
    assert casa_astral.location == "Córdoba"
