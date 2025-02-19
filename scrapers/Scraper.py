class Scraper:
    def scrape(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def __init__(self):
        self.setup()

    def __del__(self):
        self.teardown()