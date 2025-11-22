import datetime
import random

# List of whimsical weather emojis
EMOJIS = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
]


def get_forecast(date: datetime.date) -> str:
    """Return an emoji representing the weather forecast for *date*.

    The result is deterministic: the same ``date`` always yields the same emoji.
    """
    # Seed a local RNG with the date's ordinal to guarantee repeatability.
    rng = random.Random(date.toordinal())
    return rng.choice(EMOJIS)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            target_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Please provide a date in ISO format: YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = datetime.date.today()
    print(get_forecast(target_date))
