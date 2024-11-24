import smtplib
import requests
import selectorlib
from email.message import EmailMessage
import time
import os

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("SENDER")
RECEIVER = os.getenv("RECEIVER")
WAIT_TIME = 5*60

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


def store(tour_data):
    """Store tour data in data.txt"""
    with open("tours.txt", "a") as file:
        file.write(tour_data + "\n")


def send_email(content):
    """Send an email."""
    email_msg = EmailMessage()
    email_msg["Subject"] = "Upcoming New Tour!"
    email_msg.set_content(content)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
            gmail.ehlo()
            gmail.starttls()
            gmail.login(SENDER, PASSWORD)
            gmail.send_message(email_msg, SENDER, RECEIVER)
        print(content)
        print("Email sent successfully.")

    except smtplib.SMTPException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    with open("tours.txt", "w") as file_clear:
        file_clear.write("")

    extracted_tours = []
    try:
        while True:
            scraped = scrape(URL)
            extracted = extract(scraped)

            if extracted != 'No upcoming tours' and extracted not in extracted_tours:
                store(extracted)
                send_email(extracted)
                extracted_tours.append(extracted)

            time.sleep(WAIT_TIME)

    except KeyboardInterrupt:
        print("Script terminated by user.")

