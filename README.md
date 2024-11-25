# Tour Notification Bot

A Python-based script that automates the process of scraping a webpage for upcoming band tours, storing the data in a SQLite database, and sending email notifications for new tours.

## How It Works

1. **Scraping**: The script scrapes a given webpage for upcoming tour details using the `requests` library.
2. **Extraction**: The scraped HTML is parsed using the `selectorlib` library with an extractor configuration defined in `extract.yaml`.
3. **Database Storage**: Extracted tour information is stored in a SQLite database to ensure duplicate notifications are not sent.
4. **Email Notifications**: When a new tour is detected, an email notification is sent to the configured recipient.

## Features

- Scrapes and extracts tour information in real-time.
- Ensures no duplicate notifications using a database-backed storage mechanism.
- Sends email alerts for new tours with details about the band, city, and date.

## Technologies Used

- **Python Libraries**:
  - `requests`: For HTTP requests and web scraping.
  - `selectorlib`: For structured data extraction.
  - `sqlite3`: For managing the SQLite database.
  - `smtplib`: For sending email notifications.
  - `os`: For environment variable management.
- **Database**: SQLite for storing tour details.
- **Email Service**: Gmail SMTP server for sending emails.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/g-o-t-w/web-scraping-tours.git
   cd web-scraping-tours
   ```
2. Install dependencies:
    ```bash
    pip install requests selectorlib
    ```
3. Create a SQLite database named ```data.db``` and define a table for tours:
    ```bash
    CREATE TABLE tours (
    bandname TEXT,
    city TEXT,
    date TEXT
   );
    ```
4. Set up environment variables for email credentials:
    ```bash
    export PASSWORD="sender_gmail_app_password"
    export SENDER="sender_email@gmail.com"
    export RECEIVER="receiver_email@gmail.com"
    ```
5. Configure the ```extract.yaml``` file:
   * Define the selector for extracting the required information from the scraped webpage.
     ```bash
     tours:
        css: "#displaytimer"  
     ```
## Usage
1. Run the script.
    ```bash
   python3 main.py
    ```
2. The script will scrape the specified URL every 2 minutes (```WAIT_TIME```), check for new tours, and notify the recipient via email if a new tour is found.