import datetime
import re
from unicodedata import normalize

from Event import Event


def remove_accents_from_str(s: str):
    res = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize( "NFD", s), 0, re.I
    )
    return normalize('NFC', res)


def parse_date(date_string: str):
    try:
        day_mapping = {
            'Lunes': 'Monday',
            'Martes': 'Tuesday',
            'Miercoles': 'Wednesday',
            'Jueves': 'Thursday',
            'Viernes': 'Friday',
            'Sabado': 'Saturday',
            'Domingo': 'Sunday'
        }

        day, date_time = date_string.strip().split(' ', 1)
        day = remove_accents_from_str(day).replace('\t', '').replace('\n', '')
        date_str, time_str = date_time.split(', ')
        hour, minute = time_str.replace('hs', '').split(':')

        day_en = day_mapping.get(day)
        if not day_en:
            raise ValueError(f"Invalid day name: {day}")

        date_object = datetime.datetime.strptime(date_str, '%d/%m')

        combined_datetime = datetime.datetime(
            datetime.datetime.now().year,
            date_object.month,
            date_object.day,
            int(hour),
            int(minute)
        )

        return combined_datetime

    except ValueError as e:
        print(f"Error parsing date {date_string}: {e}")
        return None


def generate_html_for_events(events: list[Event]):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Event List</title>
    <style>
    .event-container {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 20px;
        width: 300px; /* Adjust as needed */
        margin: 20px;
        font-family: sans-serif;
        display: inline-block; /* Display events horizontally */
        vertical-align: top; /* Align events to the top */
    }

    .event-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .event-detail {
        margin-bottom: 5px;
    }

    .available {
        color: green;
        font-weight: bold;
    }

    .unavailable {
        color: red;
        font-weight: bold;
    }

    .event-link {
        display: block;
        margin-top: 10px;
        padding: 8px 12px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        text-align: center;
    }

    .event-link:hover {
        background-color: #367C39;
    }

    .event-list-container {
        text-align: center; /* Center the events horizontally */
    }
    .tooltip {
      position: relative;
      display: inline-block;
      border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
    }
    
    .tooltip .tooltiptext {
      visibility: hidden;
      width: 300px;
      background-color: gray;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 10px;

      /* Position the tooltip text - see examples below! */
      position: absolute;
      z-index: 1;
    }

    .tooltip .tooltiptext {
      width: 120px;
      top: 50%;
      left: 50%;
      margin-left: -60px; /* Use half of the width (120/2 = 60), to center the tooltip */
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .tooltiptext {
      visibility: visible;
    }
    </style>
    </head>
    <body>
    <div class="event-list-container">
    """

    for event in events:
        html += event.to_html()

    html += """
    </div>
    </body>
    </html>
    """

    return html