import argparse
import datetime
import random

def get_wasteland_forecast(date_str=None):
    """
    Generates a whimsical wasteland weather forecast based on a date.
    If no date is provided, it uses the current date.
    The forecast is deterministic for a given date.
    """
    if date_str:
        try:
            forecast_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: Invalid date format '{date_str}'. Please use YYYY-MM-DD.")
            return None
    else:
        forecast_date = datetime.date.today()

    # Seed the random generator with the date for deterministic forecasts
    # Mock rationale: Ensures that for a given date, the forecast is always the same,
    # making the utility predictable and testable.
    random.seed(forecast_date.toordinal())

    weather_events = [
        {"name": "Clear Skies, High Radiation", "impact": "Good visibility, but dangerous radiation levels. Limit exposure."},
        {"name": "Dust Storm", "impact": "Low visibility, respiratory hazard. Seek shelter and cover mouth/nose."},
        {"name": "Acid Rain", "impact": "Corrosive precipitation. Requires immediate shelter and protective gear."},
        {"name": "Scorching Sun", "impact": "Dehydration risk is extreme. Seek shade and conserve water."},
        {"name": "Freezing Winds", "impact": "Hypothermia risk. Bundle up and find warmth."},
        {"name": "Mutant Fog", "impact": "Low visibility, potential for unexpected encounters. Proceed with extreme caution."},
        {"name": "Ashfall", "impact": "Respiratory hazard, covers everything. Protect breathing and equipment."},
        {"name": "Gamma Burst (rare)", "impact": "EXTREMELY DANGEROUS. Seek immediate deep shelter. Survival unlikely without advanced protection."},
        {"name": "Scattered Debris Showers", "impact": "Falling junk from orbit. Keep an eye on the sky and stay agile."},
        {"name": "Whispering Winds", "impact": "Eerie calm, but whispers carry far. Be mindful of who might be listening."},
    ]

    # Select a weather event
    # Mock rationale: The random choice is made deterministic by the seeded random.
    chosen_event = random.choice(weather_events)

    return {
        "date": forecast_date.isoformat(),
        "forecast": chosen_event["name"],
        "impact": chosen_event["impact"]
    }

def main():
    parser = argparse.ArgumentParser(
        description="Predicts the 'weather' for a post-apocalyptic wasteland."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Specify a date for the forecast (YYYY-MM-DD). Defaults to today if not provided."
    )
    args = parser.parse_args()

    forecast_data = get_wasteland_forecast(args.date)

    if forecast_data:
        print("--- Wasteland Weather Oracle ---")
        print(f"Date: {forecast_data['date']}")
        print(f"\nForecast: {forecast_data['forecast']}")
        print(f"Impact: {forecast_data['impact']}")

if __name__ == "__main__":
    main()
