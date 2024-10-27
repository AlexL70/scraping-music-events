import sqlite3
import selectorlib as sl
from scrape import scrape
from send_email import send_email
import time

URL = "https://programmer100.pythonanywhere.com/tours/"


def extract(source: str) -> dict:
    extractor = sl.Extractor.from_yaml_file("extract.yml")
    value = extractor.extract(source)["tours"]
    return value


def get_cursor() -> sqlite3.Cursor:
    connection = sqlite3.connect("./data.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS events (band TEXT, city TEXT, date TEXT)")
    return connection.cursor()


def store(extracted: str):
    band, city, date = extracted.split(", ")
    cursor = get_cursor()
    cursor.execute(
        f"INSERT INTO events (band, city, date) VALUES ('{band}', '{city}', '{date}')"
    )
    cursor.connection.commit()
    cursor.close()


def check(extracted: str) -> bool:
    band, city, date = extracted.split(", ")
    cursor = get_cursor()
    cursor.execute(
        f"SELECT * FROM events WHERE band = '{band}' AND city = '{city}' AND date = '{date}'"
    )
    if cursor.fetchone():
        result = True
    else:
        result = False
    cursor.close()
    return result


while True:
    print(f"Scraping the page: {URL}")
    success, scraped = scrape(URL)
    if success:
        extracted = extract(scraped)
        if extracted and extracted != "No upcoming tours" and not check(extracted):
            store(extracted)
            send_email(extracted)
        print(extracted)
    else:
        print(f"Failed to scrape the page:\n\n {scraped[:100]}")
    time.sleep(5)
