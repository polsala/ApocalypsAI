import os
import json
from datetime import datetime, timedelta
import pytz
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apocalypse Chronometer</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; margin-top: 50px; }
        h1 { color: #ff0000; }
        .event { margin-bottom: 20px; padding: 10px; border: 1px solid #00ff00; display: inline-block; min-width: 300px; }
        .event-name { font-size: 1.5em; font-weight: bold; }
        .event-time { font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>Apocalypse Chronometer</h1>
    {% if events %}
        {% for event in events %}
            <div class="event">
                <div class="event-name">{{ event.name }}</div>
                <div class="event-time">{{ event.status }}</div>
            </div>
        {% endfor %}
    {% else %}
        <p>No apocalyptic events configured. The void is calm... for now.</p>
    {% endif %}
</body>
</html>
"""

def calculate_time_status(event_name, event_datetime_str):
    try:
        # Parse datetime string. If it's naive, assume UTC.
        event_dt = datetime.fromisoformat(event_datetime_str)
        if event_dt.tzinfo is None:
            event_dt = event_dt.replace(tzinfo=pytz.utc)
        
        now_dt = datetime.now(pytz.utc)

        if event_dt > now_dt:
            # Countdown
            delta = event_dt - now_dt
            prefix = "Countdown to"
        else:
            # Count-up
            delta = now_dt - event_dt
            prefix = "Time since"

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        status = f"{prefix} {event_name}: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        return {"name": event_name, "status": status}
    except ValueError:
        return {"name": event_name, "status": f"Error parsing datetime for {event_name}"}

@app.route('/')
def index():
    events_json_str = os.environ.get('APOCALYPSE_EVENTS_JSON', '[]')
    try:
        configured_events = json.loads(events_json_str)
    except json.JSONDecodeError:
        configured_events = []

    processed_events = []
    for event_data in configured_events:
        if 'name' in event_data and 'datetime' in event_data:
            processed_events.append(calculate_time_status(event_data['name'], event_data['datetime']))
        else:
            processed_events.append({"name": "Malformed Event", "status": "Missing 'name' or 'datetime'"})

    return render_template_string(HTML_TEMPLATE, events=processed_events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
