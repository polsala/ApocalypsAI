import datetime
from typing import Dict

# Mapping of weekdays to emojis (same emoji for simplicity, can be customized)
WEEKDAY_EMOJIS: Dict[int, str] = {
    0: "📅",  # Monday
    1: "📅",  # Tuesday
    2: "📅",  # Wednesday
    3: "📅",  # Thursday
    4: "📅",  # Friday
    5: "📅",  # Saturday
    6: "📅",  # Sunday
}

# Mapping of month numbers to emojis
MONTH_EMOJIS: Dict[int, str] = {
    1: "❄️",   # January
    2: "🌹",   # February
    3: "🍀",   # March
    4: "🌷",   # April
    5: "🌼",   # May
    6: "🌞",   # June
    7: "🏖️",  # July
    8: "🌻",   # August
    9: "🍁",   # September
    10: "🌰",  # October
    11: "🍂",  # November
    12: "🎄",   # December
}


def get_emoji_date(date: datetime.date) -> str:
    """Return a formatted string with emojis for the given date.

    Example output: "📅 Tue 🌰 Oct 31, 2023"
    """
    weekday_emoji = WEEKDAY_EMOJIS[date.weekday()]
    month_emoji = MONTH_EMOJIS[date.month]
    # Short weekday and month names
    weekday_str = date.strftime("%a")
    month_str = date.strftime("%b")
    return f"{weekday_emoji} {weekday_str} {month_emoji} {month_str} {date.day}, {date.year}"


def main() -> None:
    today = datetime.date.today()
    print(get_emoji_date(today))


if __name__ == "__main__":
    main()
