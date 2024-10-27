import sqlite3
from event import Event
from email_class import Email
import time

URL = "https://programmer100.pythonanywhere.com/tours/"


def get_cursor() -> sqlite3.Cursor:
    connection = sqlite3.connect("./data.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS events (band TEXT, city TEXT, date TEXT)")
    return connection.cursor()


def store(extracted: str):
    splitted = extracted.split(",")
    splitted = [item.strip() for item in splitted]
    band, city, date = splitted
    cursor = get_cursor()
    cursor.execute(
        f"INSERT INTO events (band, city, date) VALUES (?, ?, ?)",
        (band, city, date)
    )
    cursor.connection.commit()
    cursor.close()


def check(extracted: str) -> bool:
    band, city, date = extracted.split(", ")
    cursor = get_cursor()
    cursor.execute(
        f"SELECT * FROM events WHERE band = ? AND city = ? AND date = ?",
        (band, city, date)
    )
    if cursor.fetchone():
        result = True
    else:
        result = False
    cursor.close()
    return result


if __name__ == "__main__":
    while True:
        print(f"Scraping the page: {URL}")
        event = Event()
        success, scraped = event.scrape(URL)
        if success:
            extracted = event.extract(scraped)
            if extracted and extracted != "No upcoming tours" and not check(extracted):
                store(extracted)
                email = Email()
                email.send(extracted)
            print(extracted)
        else:
            print(f"Failed to scrape the page:\n\n {scraped[:100]}")
        time.sleep(5)
