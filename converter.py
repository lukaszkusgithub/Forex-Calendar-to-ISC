import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from ics import Calendar, Event
import pytz
from dotenv import load_dotenv

load_dotenv()

def parse_html_to_ics():
    # Load configuration from .env file
    html_file = os.getenv('HTML_FILE')
    output_file = os.getenv('OUTPUT_FILE')
    timezone = os.getenv('TIMEZONE', 'UTC')
    default_duration = int(os.getenv('DEFAULT_DURATION_MINUTES', 30))

    # Initialize the calendar
    cal = Calendar()
    tz = pytz.timezone(timezone)
    current_year = datetime.now().year  # Assume current year

    # Read and process HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    current_date = None
    remaining_rowspan = 0
    current_time = None

    # Loop through all <tbody> elements in the HTML
    for tbody in soup.find_all('tbody'):
        for row in tbody.find_all('tr'):
            # Check if the row has an event and is not a "no event" row
            if 'data-event-id' in row.attrs and 'calendar__row--no-event' not in row.get('class', []):
                # Parse the date
                date_td = row.find('td', class_='calendar__date')
                if date_td:
                    date_span = date_td.find('span', class_='date')
                    if date_span:
                        date_str = date_span.find('span').text.strip()
                        try:
                            # Combine date string with the current year
                            date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %Y")
                            current_date = date_obj.date()
                            remaining_rowspan = int(date_td.get('rowspan', 1)) - 1
                        except ValueError:
                            current_date = None
                else:
                    if remaining_rowspan > 0:
                        remaining_rowspan -= 1
                    else:
                        current_date = None

                if not current_date:
                    continue

                # Parse the time
                time_td = row.find('td', class_='calendar__time')
                time_text = time_td.get_text(strip=True) if time_td else ''
                if time_text:
                    try:
                        current_time = datetime.strptime(time_text, "%I:%M%p").time()
                    except ValueError:
                        pass

                # Determine the start time
                start_naive = datetime.combine(current_date, current_time or datetime.min.time())
                start = tz.localize(start_naive)
                end = start + timedelta(minutes=default_duration)

                # Collect event details
                title = row.find('span', class_='calendar__event-title').text.strip()
                currency = row.find('td', class_='calendar__currency').text.strip()
                impact = row.find('span', title=True).get('title', '') if row.find('span', title=True) else ''
                actual = row.find('td', class_='calendar__actual').text.strip()
                forecast = row.find('td', class_='calendar__forecast').text.strip()
                previous = row.find('td', class_='calendar__previous').text.strip()

                # Create event description
                description = (
                    f"Currency: {currency}\n"
                    f"Impact: {impact}\n"
                    f"Actual: {actual}\n"
                    f"Forecast: {forecast}\n"
                    f"Previous: {previous}"
                )

                # Add the event to the calendar
                event = Event(
                    name=title,
                    begin=start,
                    end=end,
                    description=description,
                    uid=row.get('data-event-id', '')
                )
                cal.events.add(event)

    # Save the calendar to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cal)

if __name__ == "__main__":
    parse_html_to_ics()
