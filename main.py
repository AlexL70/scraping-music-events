import selectorlib as sl
from scrape import scrape

URL = "https://programmer100.pythonanywhere.com/tours/"


def extract(source: str) -> dict:
    extractor = sl.Extractor.from_yaml_file("extract.yml")
    value = extractor.extract(source)["tours"]
    return value


print(f"Scraping the page: {URL}")
success, scraped = scrape(URL)
if success:
    extracted = extract(scraped)
    print(extracted)
else:
    print(f"Failed to scrape the page:\n\n {scraped[:100]}")
