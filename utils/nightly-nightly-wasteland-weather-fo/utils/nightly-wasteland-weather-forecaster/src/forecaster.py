import argparse
import random
from datetime import datetime, timedelta

class WastelandForecaster:
    def __init__(self):
        self.conditions = [
            "Clear Skies", "Overcast", "Partly Cloudy", "Foggy",
            "Dusty", "Smoggy", "Ashfall", "Acid Rain", "Radiation Storm"
        ]
        self.temperatures = [
            ("Bone-Chilling Cold", -10, 0), ("Chilly", 1, 10), ("Mild", 11, 20),
            ("Warm", 21, 30), ("Scorching Hot", 31, 40)
        ]
        self.radiation_levels = [
            ("Low", "Safe for short excursions"),
            ("Moderate", "Geiger counter clicking steadily"),
            ("High - Seek Shelter!", "Geiger counter screaming!"),
            ("Extreme - Evacuate Immediately!", "Radiation sickness imminent!")
        ]
        self.winds = [
            "Calm", "Light Breeze", "Gusty (Watch for flying debris!)",
            "Strong Gale", "Howling Winds (Structural damage possible!)"
        ]
        self.special_events = [
            "None", "Mutant Swarm Alert - Stay Indoors!",
            "Scavenger's Luck - Increased chance of finding useful scrap!",
            "Trader Caravan Sighted - Prepare for bartering!",
            "Mysterious Signal Detected - Investigate with caution.",
            "Resource Cache Discovered - Mark your map!"
        ]

    def _generate_day_forecast(self, day_offset: int) -> dict:
        """Generates a single day's forecast."""
        temp_desc, min_temp, max_temp = random.choice(self.temperatures)
        temp_c = random.randint(min_temp, max_temp)
        temp_f = int(temp_c * 9/5 + 32)

        rad_desc, rad_impact = random.choice(self.radiation_levels)

        return {
            "conditions": random.choice(self.conditions),
            "temperature": f"{temp_desc} ({temp_c}°C / {temp_f}°F)",
            "radiation": f"{rad_desc} ({rad_impact})",
            "wind": random.choice(self.winds),
            "special_event": random.choice(self.special_events)
        }

    def get_forecast(self, location: str, days: int = 3) -> list[dict]:
        """Generates a multi-day forecast for a given location."""
        forecast_data = []
        for i in range(days):
            forecast_data.append(self._generate_day_forecast(i))
        return forecast_data

    def run(self, location: str, days: int):
        print(f"Forecasting for {location} for {days} days:\n")
        forecast = self.get_forecast(location, days)
        start_date = datetime.now()

        for i, day_forecast in enumerate(forecast):
            current_date = start_date + timedelta(days=i)
            print(f"Day {i+1} ({current_date.strftime('%Y-%m-%d')}):\n")
            for key, value in day_forecast.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a simulated post-apocalyptic weather forecast."
    )
    parser.add_argument(
        "--location",
        type=str,
        required=True,
        help="The name of the wasteland location to forecast for."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="The number of days to forecast. Defaults to 3."
    )

    args = parser.parse_args()
    forecaster = WastelandForecaster()
    forecaster.run(args.location, args.days)
