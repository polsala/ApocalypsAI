import argparse
import hashlib
from typing import List

# List of whimsical weather conditions
_WEATHER_CONDITIONS: List[str] = [
    "sunny",
    "cloudy",
    "rainy",
    "stormy",
    "snowy",
    "windy",
    "foggy",
    "hail",
    "sleet",
    "clear night",
]


def _hash(value: str) -> int:
    """Return an integer hash of *value* using SHA‑256.

    This helper is isolated so tests can monkey‑patch it for deterministic
    expectations.
    """
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_forecast(location: str, date: str) -> str:
    """Return a deterministic weather forecast for *location* on *date*.

    Parameters
    ----------
    location: str
        Human‑readable location name (e.g., "Paris").
    date: str
        ISO‑format date string (e.g., "2025-10-31").

    Returns
    -------
    str
        One of the predefined weather condition strings.
    """
    combined = f"{location}|{date}"  # simple delimiter to avoid collisions
    hash_int = _hash(combined)
    index = hash_int % len(_WEATHER_CONDITIONS)
    return _WEATHER_CONDITIONS[index]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic whimsical weather forecast generator"
    )
    parser.add_argument("location", help="Location name, e.g., 'Tokyo'")
    parser.add_argument("date", help="Date in ISO format, e.g., '2025-12-01'")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    forecast = get_forecast(args.location, args.date)
    print(f"Weather forecast for {args.location} on {args.date}: {forecast}")


if __name__ == "__main__":
    main()
