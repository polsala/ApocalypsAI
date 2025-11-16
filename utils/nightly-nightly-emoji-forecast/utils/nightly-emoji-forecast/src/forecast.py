import datetime
import hashlib

# List of weather‑related emojis (ordered arbitrarily)
EMOJIS = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloudy
    "🌦️",  # sun behind rain cloud
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",  # snowflake
    "🌪️",  # tornado
    "🌈",  # rainbow
]


def _seed_for_date(date: datetime.date) -> int:
    """Create a deterministic integer seed from a date.

    The seed is derived from the SHA‑256 hash of the ISO‑formatted date string.
    """
    hash_bytes = hashlib.sha256(date.isoformat().encode()).hexdigest()
    return int(hash_bytes, 16)


def get_forecast(date: datetime.date) -> str:
    """Return a three‑emoji weather forecast for *date*.

    The algorithm:
    1. Compute a deterministic integer seed from the date.
    2. For three positions, shift the seed and take modulo ``len(EMOJIS)``.
    3. Concatenate the selected emojis.
    """
    seed = _seed_for_date(date)
    selected = []
    for i in range(3):
        # Shift by 4 bits per step to get a different slice of the seed.
        idx = (seed >> (i * 4)) % len(EMOJIS)
        selected.append(EMOJIS[idx])
    return "".join(selected)


if __name__ == "__main__":
    today = datetime.date.today()
    print(get_forecast(today))
