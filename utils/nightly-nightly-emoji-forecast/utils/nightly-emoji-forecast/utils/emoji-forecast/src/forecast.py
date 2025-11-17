import datetime
from typing import List

# Deterministic emoji pools – each index corresponds to a day‑of‑year bucket
SUNNY_EMOJIS: List[str] = ["☀️", "🌤️", "🌞", "🌈"]
CLOUDY_EMOJIS: List[str] = ["☁️", "🌥️", "🌫️", "🌁"]
RAINY_EMOJIS: List[str] = ["🌧️", "☔", "🌂", "💧"]
STORMY_EMOJIS: List[str] = ["⛈️", "⚡", "🌪️", "🌀"]
SNOWY_EMOJIS: List[str] = ["❄️", "☃️", "⛄", "🌨️"]

# Simple deterministic selector based on day of year
def _select_emoji_pool(day_of_year: int) -> List[str]:
    # Cycle through the five pools every ~73 days (365/5 ≈ 73)
    index = (day_of_year // 73) % 5
    return [SUNNY_EMOJIS, CLOUDY_EMOJIS, RAINY_EMOJIS, STORMY_EMOJIS, SNOWY_EMOJIS][index]

def get_emoji_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *date*.

    The algorithm:
    1. Compute the day of year (1‑365).
    2. Choose an emoji pool based on the day range.
    3. Pick two emojis from that pool using a simple hash of the date.
    """
    day_of_year = date.timetuple().tm_yday
    pool = _select_emoji_pool(day_of_year)
    # Deterministic pseudo‑random selection using the date's ordinal
    seed = date.toordinal()
    first = pool[seed % len(pool)]
    second = pool[(seed // len(pool)) % len(pool)]
    return f"{first} {second}"

def _parse_cli_arg(arg: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d").date()
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {arg}. Expected YYYY-MM-DD") from exc

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_date = _parse_cli_arg(sys.argv[1])
    else:
        target_date = datetime.date.today()
    print(get_emoji_forecast(target_date))
