import smtplib
import requests
import selectorlib
import sqlite3
from email.message import EmailMessage
import time
import os

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("SENDER")
RECEIVER = os.getenv("RECEIVER")
WAIT_TIME = 2*60

connections = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        page_source = response.text
        return page_source

    except requests.RequestException as e:
        print(f"Failed to fetch URL: {e}")
        return None


def extract(src):
    """Extract the tour information from source code."""
    try:
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(src)["tours"]
        return value

    except KeyError as e:
        print(f"Extraction failed: {e}")
        return None

def read(extracted):
    # with open("tours.txt", "r") as f:
    #     return f.read()

    extracted_row = extracted.split(",")
    extracted_row = [item.strip() for item in extracted_row]
    bandname, city, date = extracted_row
    cursor = connections.cursor()
    cursor.execute("SELECT * FROM tours WHERE bandname=? AND city=? AND date=?",(bandname, city, date))
    row = cursor.fetchall()
    return row


def store(extracted):
    """Store tour data.db in data.db.txt"""
    # with open("tours.txt", "a") as file:
    #     file.write(extracted + "\n")

    extracted_row = extracted.split(",")
    extracted_row = [item.strip() for item in extracted_row]
    cursor = connections.cursor()
    cursor.execute("INSERT INTO tours VALUES (?, ?, ?)", extracted_row)
    connections.commit()


def send_email(content):
    """Send an email."""
    email_msg = EmailMessage()
    email_msg["Subject"] = "Upcoming New Tour!"
    email_msg.set_content(f"Hello,\n\nA new tour has been announced:\n\n{content}\n\nBest regards,\nYour Tour Bot")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
            gmail.ehlo()
            gmail.starttls()
            gmail.login(SENDER, PASSWORD)
            gmail.send_message(email_msg, SENDER, RECEIVER)
        print("Email sent successfully.")

    except smtplib.SMTPException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Uncomment this line if you are running the script for the first time for testing
    # with open("tours.txt", "w") as file_clear:
    #     file_clear.write("")

    try:
        while True:
            scraped = scrape(URL)
            extracted = extract(scraped)
            print(extracted)

            if extracted != 'No upcoming tours':
                row = read(extracted)
                # True when row is empty
                if not row:
                    store(extracted)
                    send_email(extracted)
                else:
                    print("Tour already exists in database!")

            time.sleep(WAIT_TIME)

    except KeyboardInterrupt:
        print("Script terminated by user.")

