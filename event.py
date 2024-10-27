import requests
import selectorlib as sl


class Event:
    def scrape(self, url: str) -> tuple[bool, str]:
        """Scrape the page source from the URL"""
        response = requests.get(url)
        if response.status_code == 200:
            return (True, response.text)
        else:
            return (False, response.text)

    def extract(self, source: str) -> dict:
        extractor = sl.Extractor.from_yaml_file("extract.yml")
        value = extractor.extract(source)["tours"]
        return value


if __name__ == "__main__":
    URL = "https://programmer100.pythonanywhere.com/tours/"
    print(f"Scraping the page: {URL}")
    success, page_source = Event.scrape(URL)
    if success:
        print(page_source[:1000])
    else:
        print(f"Failed to scrape the page:\n\n {page_source[:1000]}")
