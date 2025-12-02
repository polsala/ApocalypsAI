'''Emoji Weather Forecast utility.

Provides a deterministic three‑emoji forecast based on the given date.
''' 

import datetime
from typing import List

# A small palette of weather‑related emojis
EMOJI_WEATHER: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # overcast
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌫️",  # fog
]


def get_emoji_forecast(date: datetime.date) -> str:
    """Return a deterministic three‑emoji forecast for *date*.

    The algorithm is deliberately simple and fully deterministic:
    1. Convert the date to its ordinal (days since 0001‑01‑01).
    2. Use the ordinal to index into ``EMOJI_WEATHER`` three times.
    3. Concatenate the selected emojis.
    """
    ordinal = date.toordinal()
    n = len(EMOJI_WEATHER)
    idx1 = ordinal % n
    idx2 = (ordinal // n) % n
    idx3 = (ordinal // (n * n)) % n
    return EMOJI_WEATHER[idx1] + EMOJI_WEATHER[idx2] + EMOJI_WEATHER[idx3]


def main() -> None:
    today = datetime.date.today()
    forecast = get_emoji_forecast(today)
    print(f"Today's emoji forecast: {forecast}")


if __name__ == "__main__":
    main()
