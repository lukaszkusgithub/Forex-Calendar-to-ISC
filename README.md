## HTML to ICS Calendar Converter
This Python script parses a calendar event HTML file and converts it into an .ics calendar file. It uses BeautifulSoup for HTML parsing and the ics library to generate the ICS calendar format. You can use this script to create event reminders for various types of events, such as meetings or schedules, directly from an HTML source.

# Prerequisites
To run the script, you'll need the following Python libraries:

- beautifulsoup4: For parsing HTML content.
- ics: For creating the .ics calendar file.
- python-dotenv: To load environment variables from a .env file.
- pytz: For timezone handling.

# Install Dependencies
You can install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

```bash
pip install beautifulsoup4 ics python-dotenv pytz
```

# Setup
1. Clone this repository or download the script.
2. Create a .env file to configure the script. The .env file should contain the following settings:
```ini
HTML_FILE=path/to/your/html/file.html
OUTPUT_FILE=path/to/output/your/calendar.ics
TIMEZONE=Your/Timezone  # e.g., 'UTC' or 'America/New_York'
DEFAULT_DURATION_MINUTES=30  # Default duration for events in minutes
```

- *HTML_FILE*: The path to the HTML file that contains the calendar data.
- *OUTPUT_FILE*: The path where the resulting .ics file will be saved.
- *TIMEZONE*: The timezone for the events (e.g., UTC, America/New_York).
- *DEFAULT_DURATION_MINUTES*: The default duration for events in minutes if duration is not provided.
# Running the Script
To run the script, execute it from the command line:

```bash
python converter.py
```
The script will read the HTML file, parse it, and generate an .ics calendar file containing all the events.

# Notes
Make sure to keep the .html file up to date if the Forex calendar changes. You may need to re-download the HTML content periodically to reflect any changes.

The script expects the Forex calendar data to be in a specific format. If the structure of the HTML changes, you may need to update the parsing logic in the script.

# License
This project is open-source and available under the MIT License.