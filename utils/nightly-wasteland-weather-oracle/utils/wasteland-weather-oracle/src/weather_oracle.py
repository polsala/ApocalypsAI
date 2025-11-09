import argparse
import json
import random
import sys

def _mock_weather_api_call(location=None, lat=None, lon=None):
    # Mock rationale: This utility is designed to be self-contained and not rely
    # on external API keys or network calls for its core functionality. In a real
    # scenario, this function would make an HTTP request to a weather API (e.g., OpenWeatherMap).
    # For testing and self-containment, we simulate a typical API response.

    # Simulate different weather conditions based on input or random choice
    mock_data_scenarios = {
        "clear": {
            "name": location or "Unknown Location",
            "main": {"temp": 298.15}, # ~25C
            "weather": [{"id": 800, "description": "clear sky"}],
            "wind": {"speed": 3.0} # ~10.8 kph
        },
        "rain": {
            "name": location or "Unknown Location",
            "main": {"temp": 280.15}, # ~7C
            "weather": [{"id": 500, "description": "light rain"}],
            "wind": {"speed": 8.0} # ~28.8 kph
        },
        "storm": {
            "name": location or "Unknown Location",
            "main": {"temp": 290.15}, # ~17C
            "weather": [{"id": 200, "description": "thunderstorm with light rain"}],
            "wind": {"speed": 12.0} # ~43.2 kph
        },
        "fog": {
            "name": location or "Unknown Location",
            "main": {"temp": 285.15}, # ~12C
            "weather": [{"id": 741, "description": "fog"}],
            "wind": {"speed": 2.0} # ~7.2 kph
        },
        "snow": {
            "name": location or "Unknown Location",
            "main": {"temp": 268.15}, # ~-5C
            "weather": [{"id": 600, "description": "light snow"}],
            "wind": {"speed": 6.0} # ~21.6 kph
        },
        "extreme_cold": {
            "name": location or "Unknown Location",
            "main": {"temp": 253.15}, # ~-20C
            "weather": [{"id": 602, "description": "heavy snow"}],
            "wind": {"speed": 15.0} # ~54 kph
        },
        "extreme_heat": {
            "name": location or "Unknown Location",
            "main": {"temp": 313.15}, # ~40C
            "weather": [{"id": 800, "description": "clear sky"}],
            "wind": {"speed": 5.0} # ~18 kph
        }
    }

    # For deterministic testing, specific locations could map to specific scenarios.
    # For general use, pick a random one if no specific scenario is implied.
    if location and "new york" in location.lower():
        return mock_data_scenarios["rain"]
    elif location and "los angeles" in location.lower():
        return mock_data_scenarios["clear"]
    elif location and "london" in location.lower():
        return mock_data_scenarios["fog"]
    elif lat == 40.7128 and lon == -74.0060: # New York coords
        return mock_data_scenarios["rain"]
    elif lat == 34.0522 and lon == -118.2437: # LA coords
        return mock_data_scenarios["clear"]
    else:
        return random.choice(list(mock_data_scenarios.values()))

def _get_apocalyptic_description(weather_data):
    temp_k = weather_data['main']['temp']
    temp_c = temp_k - 273.15
    condition_id = weather_data['weather'][0]['id']
    wind_speed_mps = weather_data['wind']['speed']
    wind_speed_kph = wind_speed_mps * 3.6
    location_name = weather_data.get('name', 'The Wasteland')

    temp_desc = ""
    if temp_c < -10:
        temp_desc = "Freezing wastes."
    elif -10 <= temp_c < 5:
        temp_desc = "Chilly winds."
    elif 5 <= temp_c < 20:
        temp_desc = "Mild, but don't get complacent."
    else:
        temp_desc = "Scorching sun."

    condition_desc = ""
    if 200 <= condition_id < 300: # Thunderstorm
        condition_desc = "Electrical storms rage, avoid high ground!"
    elif 300 <= condition_id < 400: # Drizzle
        condition_desc = "Light acid rain, cover your gear."
    elif 500 <= condition_id < 600: # Rain
        condition_desc = "Heavy acid downpour, seek immediate shelter!"
    elif 600 <= condition_id < 700: # Snow
        condition_desc = "Blizzard conditions, visibility near zero."
    elif 701 <= condition_id < 800: # Atmosphere (Mist, Smoke, Haze, Dust, Fog, Sand, Ash, Squall, Tornado)
        if condition_id == 781: # Tornado
            condition_desc = "Twister inbound! Find deep shelter NOW!"
        elif condition_id in [731, 751, 761]: # Sand/Dust
            condition_desc = "Dust devils brewing, visibility low, don your respirators!"
        else:
            condition_desc = "Toxic fog/dust/ash cloud rolling in, don your respirators!"
    elif condition_id == 800: # Clear
        condition_desc = "Clear skies, but watch for raiders and mutated wildlife."
    elif 801 <= condition_id < 900: # Clouds
        condition_desc = "Overcast, good for stealth, but watch for aerial threats."
    else:
        condition_desc = "Unidentifiable atmospheric anomaly detected."

    wind_desc = ""
    if wind_speed_kph < 10:
        wind_desc = "A gentle, eerie breeze."
    elif 10 <= wind_speed_kph < 30:
        wind_desc = "Gusty winds, secure your scavenged goods."
    else:
        wind_desc = "Gale force winds, shelter immediately or risk being blown away!"

    return f"""--- Wasteland Weather Report for {location_name} ---
Conditions: {temp_desc} {condition_desc}
Wind: {wind_desc}
"""

def main():
    parser = argparse.ArgumentParser(
        description="Get a post-apocalyptic weather forecast for a given location."
    )
    parser.add_argument(
        "--location", type=str, help="City name (e.g., 'New York')"
    )
    parser.add_argument(
        "--lat", type=float, help="Latitude (e.g., 40.7128)"
    )
    parser.add_argument(
        "--lon", type=float, help="Longitude (e.g., -74.0060)"
    )

    args = parser.parse_args()

    if not args.location and not (args.lat is not None and args.lon is not None):
        parser.error("Either --location or both --lat and --lon must be provided.")
        sys.exit(1)

    try:
        weather_data = _mock_weather_api_call(location=args.location, lat=args.lat, lon=args.lon)
        if weather_data:
            forecast = _get_apocalyptic_description(weather_data)
            print(forecast)
        else:
            print(f"Error: Could not retrieve weather for {args.location or f'{args.lat},{args.lon}'}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
