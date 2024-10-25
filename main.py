import selectorlib
from scrape import scrape

URL = "https://programmer100.pythonanywhere.com/tours/"


print(f"Scraping the page: {URL}")
success, source = scrape(URL)
if success:
    print(source[:100])
else:
    print(f"Failed to scrape the page:\n\n {source[:100]}")
