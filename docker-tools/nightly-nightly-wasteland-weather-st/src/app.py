import os
import requests
import sys

def get_weather_data(api_key, location=None, lat=None, lon=None):
    """Fetches weather data from OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "appid": api_key,
        "units": "metric"
    }

    if lat and lon:
        params["lat"] = lat
        params["lon"] = lon
    elif location:
        params["q"] = location
    else:
        raise ValueError("Either 'location' or 'lat' and 'lon' must be provided.")

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch weather data: {e}", file=sys.stderr)
        sys.exit(1)

def format_weather_report(data):
    """Formats the raw weather data into a wasteland-style report."""
    if not data or "main" not in data or "weather" not in data or "wind" not in data:
        return "ERROR: Incomplete weather data received."

    location_name = data.get("name", "Unknown Wasteland")
    conditions = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)

    wind_speed_kmh = round(wind_speed * 3.6)

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    direction_index = round(wind_deg / 45)
    wind_direction = directions[direction_index]

    weather_icon = "❓"
    if "clear" in conditions.lower():
        weather_icon = "☀️"
    elif "cloud" in conditions.lower():
        weather_icon = "☁️"
    elif "rain" in conditions.lower() or "drizzle" in conditions.lower():
        weather_icon = "🌧️"
    elif "storm" in conditions.lower() or "thunder" in conditions.lower():
        weather_icon = "⛈️"
    elif "snow" in conditions.lower():
        weather_icon = "❄️"
    elif "mist" in conditions.lower() or "fog" in conditions.lower():
        weather_icon = "🌫️"
    elif "dust" in conditions.lower() or "sand" in conditions.lower():
        weather_icon = "🌪️"

    report = [
        "+-------------------------------------+",
        "|  Wasteland Weather Report           |",
        "+-------------------------------------+",
        f"| Location: {location_name.ljust(29)}|",
        f"| Conditions: {conditions} {weather_icon}".ljust(38) + "|",
        f"| Temperature: {round(temp)}°C (Feels like: {round(feels_like)}°C){' '.ljust(3)}|",
        f"| Wind: {wind_speed_kmh} km/h {wind_direction}".ljust(38) + "|",
        f"| Humidity: {humidity}%".ljust(38) + "|",
        "+-------------------------------------+"
    ]
    return "\n".join(report)

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    location = os.getenv("LOCATION")
    lat = os.getenv("LAT")
    lon = os.getenv("LON")

    if not api_key:
        print("ERROR: API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        weather_data = get_weather_data(api_key, location, lat, lon)
        print(format_weather_report(weather_data))
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
