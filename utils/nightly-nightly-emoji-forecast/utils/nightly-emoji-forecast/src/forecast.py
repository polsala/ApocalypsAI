import datetime
import hashlib
from typing import Optional


def _seed_for_date(date: datetime.date) -> int:
    """Return an integer seed derived from the ISO‑formatted date.

    The seed is the integer value of the SHA‑256 hash of the date string.
    """
    iso = date.isoformat().encode("utf-8")
    return int(hashlib.sha256(iso).hexdigest(), 16)


def _condition_from_random(rand: int) -> str:
    """Map a 0‑99 integer to a base weather condition emoji string."""
    if rand < 20:
        return "☀️ Sunny"
    elif rand < 40:
        return "⛅ Partly Cloudy"
    elif rand < 60:
        return "☁️ Cloudy"
    elif rand < 80:
        return "🌧️ Rainy"
    else:
        return "⛈️ Stormy"


def _precip_extra_from_random(rand: int) -> str:
    """Map a 0‑99 integer to an optional precipitation‑related suffix."""
    if rand < 30:
        return ""
    elif rand < 70:
        return " with a chance of 🌦️"
    else:
        return " with a chance of 🌩️"


def get_forecast(date: Optional[datetime.date] = None) -> str:
    """Return a deterministic emoji weather forecast.

    Parameters
    ----------
    date: datetime.date, optional
        The date for which to generate the forecast. If omitted, uses
        ``datetime.date.today()``.

    Returns
    -------
    str
        A human‑readable string containing emojis.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_for_date(date)
    # Derive two independent pseudo‑random numbers from the seed
    rand_condition = seed % 100
    rand_precip = (seed // 100) % 100
    condition = _condition_from_random(rand_condition)
    extra = _precip_extra_from_random(rand_precip)
    return f"{condition}{extra}"


if __name__ == "__main__":
    # Simple CLI: print today’s forecast
    print(get_forecast())
