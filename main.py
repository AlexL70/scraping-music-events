import os
import selectorlib as sl
from scrape import scrape

URL = "https://programmer100.pythonanywhere.com/tours/"


def extract(source: str) -> dict:
    extractor = sl.Extractor.from_yaml_file("extract.yml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted: str):
    with open("data.txt", "a") as file:
        file.write(f"{extracted}\n")


def check(extracted: str):
    if not os.path.isfile("data.txt"):
        open("data.txt", "w").close()
    with open("data.txt", "r") as file:
        data = file.read()
        if extracted in data:
            return True
        return False


def send_email():
    print("Email sent")


print(f"Scraping the page: {URL}")
success, scraped = scrape(URL)
if success:
    extracted = extract(scraped)
    if extracted and extracted != "No upcoming tours" and not check(extracted):
        store(extracted)
        send_email()
    print(extracted)
else:
    print(f"Failed to scrape the page:\n\n {scraped[:100]}")
